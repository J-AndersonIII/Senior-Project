from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from functools import partial
from kivy.clock import Clock

import btoothHndl as bh
import time
import subprocess
import serial
from xbee import XBee
import RPi.GPIO as GPIO


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
        self.pair_popup = PairPopup()

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
            if next_screen == "scanningscreen":
                self.ids.kivy_screen_manager.current = "scanning_screen"
            if next_screen == "availabledevscreen":
                self.ids.kivy_screen_manager.current = "available_dev_screen"
            if next_screen == "startscreen":
                del self.screen_list[:]
                self.ids.kivy_screen_manager.current = "start_screen"
            if next_screen == "monitor mode":
                self.ids.kivy_screen_manager.current = "monitor_screen"

    def onBackBtn(self):
        # If there's any screen in this list currently...
        if self.screen_list:
            # If there's a screen to go back to, go back to it.
            self.ids.kivy_screen_manager.current = self.screen_list.pop()

    def scanDevices(self):
        App.get_running_app().data = bh.scanDev()
        print "scan devices run succesful"
        return App.get_running_app().data


class Test(FloatLayout):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.door_email_counter = 0
        self.low_battery_counter = 0
        self.temp_counter = 0
        self.timer1 = 0
        self.timer2 = 0
        self.timer3 = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        #ser = serial.Serial('/dev/ttyUSB0', 9600)
        #xbee = XBee(ser, callback=msgDump())
        self.button_status = False


    def runMode(self):
        Clock.schedule_interval(self.monMode, 0.5)

    def exitMode(self):
        Clock.unschedule(self.monMode)
        App.get_running_app().root.changeScreen("startscreen")

    def monMode(self, dt):
        maintimer = time.time()
        reset1 = self.timer1 - maintimer
        reset2 = self.timer2 - maintimer
        reset3 = self.timer3 - maintimer

        if reset1 >= 15:
            self.timer1 = time.time()
            self.door_email_counter = 0

        if reset2 >= 15:
            self.timer2 = time.time()
            self.low_battery_counter = 0

        if reset3 >= 15:
            self.timer3 = time.time()
            self.temp_counter = 0

        if GPIO.input(17):
            #SEND EMAIL HERE FOR BACKUP BATTERY
            print "Who the fuck unplugged me!"

        if self.button_status == True:
            print "exception successfully raised!"
            xbee.halt()
            ser.close()
            GPIO.cleanup()

    def msgDump(self, packet):
        print "MSG DUMP RUN"




class PairPopup(Popup):
    ''' Popup for the user to add their phone for pairing and ultimately
        connecting.
    '''
    def __init__(self, *args, **kwargs):
        super(PairPopup, self).__init__(*args, **kwargs)
        self.timeout = 0

    def pairDevices(self):
        myDevice = App.get_running_app().root.device_list[-1]
        myAdd = myDevice.mAdd
        self.timeout = 30

        while True:
            if bh.pairDev(myAdd) == False and self.timeout != 0:
                self.timeout = self.timeout - 1
                time.sleep(1)
                continue
            if bh.pairDev(myAdd) == False and self.timeout == 0:
                print "Pair function timed out!"
                #status_label.text = "Timed out! No Device Found!"
                self.dismiss()
                time.sleep(3)
                break
            if bh.pairDev(myAdd) == True:
                self.dismiss()
                print "Pair successful! Attempting to connect."
                #status.label.text = "Success! You're all set!"
                time.sleep(3)
                break

    def connDevices(self):
        myDevice = App.get_running_app().root.device_list[-1]
        myAdd = myDevice.mAdd

        bh.connDev(myAdd)

        App.get_running_app().root.changeScreen("startscreen")


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
        phone_number.text = ""
        self.dismiss()
        root.changeScreen("scanningscreen")

    def stayHere(self):
        phone_screen = App.get_running_app().root.ids.phone_screen
        phone_number = phone_screen.phone_number
        root = App.get_running_app().root

        phone_number.text = ""
        self.dismiss()


class ScanningScreen(Screen):
    someList = ListProperty([])
    def __init__(self, *args, **kwargs):
        super(ScanningScreen, self).__init__(*args, **kwargs)

    def scanTransition(self):
        root = App.get_running_app().root
        print "Hell Yeah boi"
        App.get_running_app().root.mac_list = root.scanDevices()
        root.changeScreen("availabledevscreen")


class AvailableDevices(GridLayout):
    ''' This screen needs to operate a bluetooth scan
        and then recieve the list of devices (from scanDev)
        and display them.
    '''
    def __init__(self, *args, **kwargs):
        super(AvailableDevices, self).__init__(*args, **kwargs)
        self.cols = 2
        self.row_force_default = True
        self.col_force_default = True
        self.row_default_height = 50
        self.col_default_width = 350

    def generateStack(self):
        print "Were gererating BABY"
        mac_list = App.get_running_app().root.mac_list
        #myList = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
        print mac_list
        #for device in myList:
        for device in mac_list:
            self.add_widget(Button(text=device, font_size=20, on_release=self.onBtnPress))

    def noDevFound(self):
        self.clear_widgets()
        del App.get_running_app().root.mac_list[:]
        print App.get_running_app().root.mac_list
        App.get_running_app().root.onBackBtn()

    def onBtnPress(self, btn):
        root = App.get_running_app().root
        mac_address = btn.text[0:17]
        device_name = btn.text[18:]

        root.device_list[-1].setMac(mac_address)
        root.device_list[-1].setName(device_name)
        root.device_list[-1].printDevice()
        del App.get_running_app().root.mac_list[:]
        root.pair_popup.open()



class KeyPad(GridLayout):
    ''' This generates a basic numpad and allows
        the user to input their phone number. It
        also builds a "done" and "clear" button
        for convenience.
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
        self.mAdd = ""
        self.devName = ""

    def setMac(self, address):
        self.mAdd = address

    def setName(self, name):
        self.devName = name

    def printDevice(self):
        print ("The device name is %s, its mac address is %s, and its phone number is %s"%(self.devName, self.mAdd, self.pNum))


class jetGUIApp(App):
    ''' The App Object
    '''
    def __init__(self, **kwargs):
        super(jetGUIApp, self).__init__(**kwargs)

    def build(self):
        subprocess.call(['pulseaudio', '--kill'])
        time.sleep(.2)
        subprocess.call(['pulseaudio', '--start'])
        return jetGUIRoot()

    def getText(self):
        return ("Hey there!\nThis app was built using"
                " Kivy, a Python framework.\n It was created"
                " for academic purposes and is free for"
                " anyone to use and modify! Enjoy! :)"
                "\n~Jerome, Eric & Tsue")

    def scanText(self):
        return ("[b][u]IMPORTANT:[/b][/u] Before selecting the scanning button, please be"
                "\nsure to enable your device's bluetooth setting and make sure"
                "\nthat it is visible to other bluetooth devices!")

    def getLabel(self):
        return ("\nPlease select\n'Jet Monitoring Systems'\nfrom your list"
                " of available bluetooth devices. After that you're"
                " all set!")


if __name__ == "__main__":
    jetGUIApp().run()
