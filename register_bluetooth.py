#!/usr/bin/env python3
import bluetooth
from sense_hat import SenseHat
import time
import os


# Main function
def main():

        register()
        


# Search for device based on device's name
def search(user_name, device_name):
    while True:
        device_address = None
        dt = time.strftime("%a, %d %b %y %H:%M:%S", time.localtime())
        print("\nCurrently: {}".format(dt))
        time.sleep(3) #Sleep three seconds 
        nearby_devices = bluetooth.discover_devices()

        for mac_address in nearby_devices:
            if device_name == bluetooth.lookup_name(mac_address, timeout=5):
                device_address = mac_address
                break
        if device_address is not None:
            with open("device_file.txt", "w") as device_file:
                device_file.write("{}, {}\r\n".format(user_name, device_address))
                print("Hi {}, Your phone {} with the MAC address: {} has been registered".format(user_name, device_name, device_address))
                smiley_face()
        else:
            print("Could not find target device nearby...")


def register():
    user_name = input("Enter your name: ")
    device_name = input("Enter the name of your phone: ")
    search(user_name, device_name)

def smiley_face():
    #some code interpreted from https://github.com/stw1/sense_hat/blob/master/smile.py#L28

    sense = SenseHat()
  
  # set up the colours (white, green, red, empty)
    g = [0, 255, 0]
    e = [0, 0, 0]

    smile = [
    e,e,e,e,e,e,e,e,
    e,g,g,e,e,g,g,e,
    e,g,g,e,e,g,g,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    g,e,e,e,e,e,e,g,
    g,g,g,g,g,g,g,g,
    e,e,e,e,e,e,e,e
    ]
    
    sense.clear()
    sense.set_pixels(smile)
    time.sleep(10)
    sense.clear()


#Execute program
main()