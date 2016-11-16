#!/bin/bash

# run bluez
echo -e 'devices\nquit' | bluetoothctl > output.txt
