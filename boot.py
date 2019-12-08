## Board preparation:
#
# Load the MicroPython firmware onto the board.
#
# Create file '/wifi_creds' with the wifi ssid on the first line and the
# password on the second line.

# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

import network
import webrepl

## Start webrepl

webrepl.start()


## Connect to wifi

wifi_creds = open('wifi_creds')
ssid, password = [cred.strip() for cred in wifi_creds.readlines()]
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, password)
while not sta_if.isconnected():
    time.sleep_ms(500)
    print("...Retrying wifi connection...")
print('network config:', sta_if.ifconfig())

