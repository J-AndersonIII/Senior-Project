import pexpect
import subprocess
import time

def pairDev(maddr):
    child = pexpect.spawn('bluetoothctl')
    child.expect('# ')
    time.sleep(15)
    child.sendline('pair ' + maddr)
    return

def scanDev():
    #  Uses the subrocess library to run hcitool's scan function in the background
    #  It gives hcitool 20 seconds (time.sleep..) to perform a full scan
    #  Lastly, the function stores all of the available bluetooth mac addresses in the mac_list list

    available_devices = []

    child = pexpect.spawn('bluetoothctl')
    child.expect('# ')
    child.sendline('scan on\r')
    time.sleep(15)
    child.expect('# ')
    child.sendline('scan off\r')

    child.expect('# ')
    child.sendline('devices\r')
    child.expect('# ')
    out = child.before

    print out
    print 'hello bill'
    print out

    '''filename = 'maddrs.txt'
    a_list = []

    with open(filename, 'w') as addrFile:
        subprocess.Popen(['hcitool', 'scan'], stdout=addrFile)
        time.sleep(15)

    with open(filename, 'r') as txt:
        a_list = txt.readlines()

    mac_list = map(str.strip, a_list)
    mac_list = [w.replace('\t', ' ') for w in mac_list]
    del mac_list[0]
    print mac_list
    return'''

def connDev(maddr):
    child = pexpect.spawn('bluetoothctl')
    child.expect('# ')
    child.sendline('connect ' + maddr)
    return

def rssiDev(maddr):
    out = subprocess.Popen(['hcitool', 'rssi', maddr], stdout=subprocess.PIPE)
    print out.stdout.read()
    return
