from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen

import btoothHndl as bh


class jetGUIRoot(BoxLayout):
    ''' The Root of all Widgets
    '''
    def __init__(self, **kwargs):
        super(jetGUIRoot, self).__init__(**kwargs)
        # List of Previous Screens.
        self.screen_list = []
        self.mac_list = []
        self.device_list = []
        self.current_number = ""
        self.phone_popup = PhonePopup()

    def changeScreen(self, next_screen):
        operations = ["add a device", "remove a device", "monitor mode"]
        auto_screens = None

        # Adds screens to screen_list if they aren't already there.
        if self.ids.kivy_screen_manager.current not in self.screen_list:
            self.screen_list.append(self.ids.kivy_screen_manager.current)

        if next_screen == "about this app":
            self.ids.kivy_screen_manager.current = "about_screen"
        else:
            if next_screen == "add a device":
                self.ids.kivy_screen_manager.current = "phone_screen"

    def onBackBtn(self):
        # If there's any screen in this list currently...
        if self.screen_list:
            # If there's a screen to go back to, go back to it.
            self.ids.kivy_screen_manager.current = self.screen_list.pop()

    def scanDevices(self):
        self.mac_list = bh.scanDev()
        print self.mac_list


class PhonePopup(Popup):
    ''' Popup for when the user needs to confirm their phone number is correct.
    '''
    message = ObjectProperty()
    yes_button = ObjectProperty()
    no_button = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(PhonePopup, self).__init__(*args, **kwargs)

    def moveOn(self):
        phone_screen = App.get_running_app().root.ids.phone_screen
        phone_number = phone_screen.phone_number
        root = App.get_running_app().root

        root.device_list.append(Device(phone_number.text))
        self.dismiss()

    def stayHere(self):
        phone_screen = App.get_running_app().root.ids.phone_screen
        phone_number = phone_screen.phone_number
        root = App.get_running_app().root

        phone_number.text = ""
        self.dismiss()


class KeyPad(GridLayout):
    ''' Documentation for KeyPad
    '''
    def __init__(self, *args, **kwargs):
        super(KeyPad, self).__init__(*args, **kwargs)
        self.pos_hint = {'x': 0.3, 'top': 0.5}
        self.cols = 3
        self.row_force_default = True
        self.row_default_height = 50
        self.col_force_default = True
        self.col_default_width = 100
        self.spacing = 5
        self.createButtons()

    def createButtons(self):
        numList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "Done", "Clear"]
        for num in numList:
            self.add_widget(Button(text=str(num), on_release=self.onBtnPress))

    def onBtnPress(self, btn):
        phone_screen = App.get_running_app().root.ids.phone_screen
        phone_number = phone_screen.phone_number
        root = App.get_running_app().root

        if btn.text.isdigit() and len(phone_number.text) < 10:
            phone_number.text += btn.text
        if btn.text == "Done" and len(phone_number.text) == 10:
            root.current_number = phone_number.text
            root.phone_popup.open()
            root.phone_popup.message.text = phone_number.text
            print len(root.device_list)
        if btn.text == "Clear" and len(phone_number.text) != 0:
            phone_number.text = ""


class Device(object):
    def __init__(self, number):
        self.pNum = number

    def setMac(address):
        self.mAdd = adress

    def setName(name):
        self.devName = name


class jetGUIApp(App):
    ''' The App Object
    '''
    def __init__(self, **kwargs):
        super(jetGUIApp, self).__init__(**kwargs)

    def build(self):
        return jetGUIRoot()

    def getText(self):
        return ("Hey there!\nThis app was built using"
                " Kivy, a Python framework.\n It was created"
                " for academic purposes and is free for"
                " anyone to use and modify! Enjoy! :)"
                "\n~Jerome, Eric & Tsu")

if __name__ == "__main__":
    jetGUIApp().run()
