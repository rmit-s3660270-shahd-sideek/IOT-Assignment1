#!/usr/bin/env python3
# The spec sheet states to measure Temperature, Humidity and anthing else relevant. Ive chosent pressure as the
# other thing relevant  

import time
import sqlite3
import os
import json
from sense_hat import SenseHat
dbname='/home/pi/IOT/a1/sensehat.db'

#making this global as I am recording data 3 ways 
sense = SenseHat()

sense.show_message("Working", scroll_speed = 0.05)


#method for recording all 3 types 
def rec_data():
    #logic taken from: http://yaab-arduino.blogspot.com/2016/08/accurate-temperature-reading-sensehat.html
    cpu_temp = os.popen("vcgencmd measure_temp").readline()
    cpu_temp = cpu_temp.replace("temp=", "")
    cpu_temp = float(cpu_temp.replace("'C\n",""))

    accurateTemp = round(cpu_temp - sense.get_temperature() , 1) #recording temp minus cpu heat
    
    
    humid = sense.get_humidity() #recoding humidity
    if humid is not None: 
        humid = round(humid , 1) 
    pressure = sense.get_pressure() #recording pressure 
    if pressure is not None:
        pressure = round(pressure, 1)
        logData (accurateTemp , humid, pressure)
 

def logData (accurateTemp, humid, pressure):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO SENSEHAT_data values(datetime('now'), (?), (?), (?))", (accurateTemp, humid, pressure))
    conn.commit()
    conn.close()


# display entire database contents
def displayData():
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    print ("\nEntire database contents:\n")
    for row in curs.execute("SELECT * FROM SenseHat_data"):
        print (row)
    conn.close()

    # main function
def main():
    
    rec_data()
    displayData()

# Execute the main function
main()