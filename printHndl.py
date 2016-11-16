import subprocess


def printMain():
    '''This Function simply prints the title and options for the 
    text version of the GUI'''

    subprocess.call('clear', shell=True)

    print("*****************************************" +
    "\nJET Home Monitoring Systems (Alpha Build)" +
    "\n*****************************************")

    print("\nPlease Choose a Command:")
    print("\n(1) Pair Device:")
    print("(2) Connect Device:")
    print("(3) Get RSSI Value:")
    print("(4) Scan for Devices:")

    return
