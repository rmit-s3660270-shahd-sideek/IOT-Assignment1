#!/usr/bin/env python3
import bluetooth
from sense_hat import SenseHat
import os
import time

#try method incase file couldn't be opened
def main():
    try: 
        nearby_devices = bluetooth.discover_devices(lookup_names = False)

        while True:
            scan(nearby_devices)
            break
    except IOError:
        print("Could not open file")


   
def scan(nearby_devices):
   
    with open('/home/pi/IOT/a1/config_files/device_file.txt','r') as f:
        for line in f:
            address = line.split(", ")[1]
        #splits the strings in the text by a comma
        for addresses in nearby_devices:
                #ignores the MAC address and reads the user name
                if addresses in address:
                    name = line.split(",")[0]
                    message(name)

def message(name):
    #accurate temperature reading
    sense = SenseHat()
    cpu_temp = os.popen("vcgencmd measure_temp").readline()
    cpu_temp = cpu_temp.replace("temp=", "")
    cpu_temp = float(cpu_temp.replace("'C\n",""))

    accurateTemp = round(cpu_temp - sense.get_temperature() , 1)
    
    
    sense.clear()
    sense.show_message("Hi {}! Current Temp is {}*c".format(name, accurateTemp), scroll_speed=0.05)
    sense.clear()

main()
