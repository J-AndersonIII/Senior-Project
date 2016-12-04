import pexpect
import subprocess
import time

def removeSpace(s):
    #  Simple function to clean up the string of mac addresses
    return s[1:]


def pairDev(maddr):
    #  This function uses the subprocess module to call a shell script
    #  This script automates the bluetoothctl command prompt in order to access paired devices
    #  The script stores the output of bluetoothctl in a output.txt file for processing

    device = ('Device ' + maddr)

    subprocess.call(['./btooth_scan.sh'])
    if device in open('output.txt').read():
        paired = True

    else:
        paired = False
        print('\n...Searching...')
    return paired


def scanDev():
    #  Uses the subrocess library to run hcitool's scan function in the background
    #  It uses the communicate() method to wait until the scan process is complete in the OS
    #  The function then parses the data in the "alist" list

    alist = []

    process = subprocess.Popen(['hcitool', 'scan'], stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    alist = stdout.splitlines()
    del alist[0]
    alist = [w.replace('\t', ' ') for w in alist]
    alist = [removeSpace(s) for s in alist]
    return alist



    '''
    print("\nPlease select your device (enter 'r' to rescan):  \n")
    print('\n'.join('\t{}. {}'.format(*line) for line in enumerate(alist)))

    ans = raw_input('\nDevice:  ')

    if ans.isdigit() and int(ans) <= len(alist):
        myMac = alist[int(ans)]
        return myMac
    elif ans.lower() == 'r':
        return scanDev()
    else:
        print("Please select a valid mac address (If yours isn't listed, enter 'r' to re-scan)")
        time.sleep(2)
        return scanDev()
    '''


    
def connDev(maddr):
    #  Uses pexpect to spawn a quick instance of bluetoothctl and send the command to connect

    child = pexpect.spawn('bluetoothctl')
    child.expect('# ')
    child.sendline('connect ' + maddr)
    return


def rssiDev(maddr):
    #  Uses subprocess to run an instance of hcitool using the rssi command
    out = subprocess.Popen(['hcitool', 'rssi', maddr], stdout=subprocess.PIPE)
    line = out.stdout.readline()
    line.strip()
    value = int(filter(str.isdigit, line))
    return value
