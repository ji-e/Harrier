
import blescan
import sys
import math

import bluetooth._bluetooth as bluez

dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
    print "ble thread started"

except:
    print "error accessing bluetooth device..."
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

def find_words(text, search):
    dText = str(text[18:50])
    if(dText == search):
	return True
    else:
	return False

def calculateDistance(txPower, rssi):
    if(rssi == 0):
        return -1.0 # we cannot determine distance
    else:
	ratio = rssi * 1.0 / txPower
        if(ratio < 1.0):
            return math.pow(ratio, 10)
        else:
            accuracy = (0.89976) * math.pow(ratio, 7.7095) + 0.111
  	    return accuracy

txPower = 0
rssi = 0

while True:
    returnedList = blescan.parse_events(sock, 10)
    for i in range(0, len(returnedList)):
        if(find_words(returnedList[i], "e2c56db5dffb48d2b060d0f5a71096e0")):
		print(returnedList[i])
		txPower = int(returnedList[i][56:59])
		rssi = int(returnedList[i][60:63])
		print(str(calculateDistance(txPower, rssi)) + " m")

