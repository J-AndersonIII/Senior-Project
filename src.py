import btoothHndl as bt #  Handles all bluetooth functionality
import printHndl as ptr #  Handles text based GUI printing and screen clearing
import receive_samples_async as zigbee
import subprocess
import time

def main():

    subprocess.call(['pulseaudio', '--kill'])
    time.sleep(.2)
    subprocess.call(['pulseaudio', '--start'])

    cStatus = False
    pStatus = False

    while True:

        ptr.printMain()
        
        ans = raw_input("\nEnter Command:  ")

        if ans.isdigit():
            if int(ans) == 1:
                print("\nPlease pair with 'raspberrypi' FROM your device.")
                print('\n...Waiting...')
                time.sleep(5)
                pStatus = bt.pairDev(mac_addr)
                if pStatus: 
                    print('\nPairing successful!')
                    time.sleep(1.5)
                    print('\n...Loading...')
                    time.sleep(1.5)
                else:
                    print('\nERROR: Pair unsuccessful!')
                    time.sleep(3)

            elif int(ans) == 2:
                bt.connDev(mac_addr)

            elif int(ans) == 3: #  THIS NEEDS TO BE ADJUSTED, TRY USING THE STATUS FLAGS!!
                try:
                    bt.rssiDev(mac_addr)
                except UnboundLocalError:
                    print('\nNO MAC ADDRESS DETECTED:  Please SCAN, SELECT and CONNECT a device to continue.')
                    time.sleep(3)
            
            elif int(ans) == 4:
                mac_addr = bt.scanDev()
                print('\n...Loading...')
                time.sleep(1.5)
                print('\nMac Address successfully loaded!')
                time.sleep(1.5)

            elif int(ans) == 5:
                print('\nMonitor Mode Enabled!')
                warn = 15
                count = 0
                clr = 0

                while True:
                    rssi = bt.rssiDev(mac_addr)
                    print('\nrssi = ' + str(rssi))

                    if rssi >= warn:
                        count+=1
                        print count

                    elif rssi <= warn:
                        clr+=1
                        print clr

                    if count >= 3:
                        print('\nSending Email...')
                        break

                    elif clr >= 3:
                        clr = 0
                        count = 0
                        print('\nAll good...')


            else:
                print("Please use one of the Available Commands!")
        else:
            print("Please enter a NUMBER corresponding to one of the provided commands!")

if __name__ == "__main__":
    main()
