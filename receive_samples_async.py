#! /usr/bin/python

"""
receive_samples_async.py

This reads the serial port and asynchronously processes IO data
received from a remote XBee.
"""

from xbee import XBee
import time
import serial


def getStatus():
    PORT = '/dev/ttyUSB0'
    BAUD_RATE = 9600
    eric = 3

    # Open serial port
    ser = serial.Serial(PORT, BAUD_RATE)

    # Create API object, which spawns a new thread
    xbee = XBee(ser)

    # Do other stuff in the main thread
    packet = xbee.wait_read_frame(100)
    time.sleep(.5)
    wait=1
    while wait: 
        wait= packet['samples'][0]['dio-0']

     #  if packet['samples'][0]['dio-0'] == False:
     #       eric=0;
     #   if packet['samples'][0]['dio-0'] == True:
     #       eric=1;
    print('\n Xbee status is!!!')
    print wait 
    
    # halt() must be called before closing the serial
    # port in order to ensure proper thread shutdown
    xbee.halt()
    ser.close()
    time.sleep(2)
    return
