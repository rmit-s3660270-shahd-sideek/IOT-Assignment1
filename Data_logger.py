#!/usr/bin/env python3
# The spec sheet states to measure Temperature, Humidity and anthing else relevant. Ive chosent pressure as the
# other thing relevant  

#Main code logic taken from week 4 lab code archive

import time
import sqlite3
from sense_hat import SenseHat
dbname='sensehat.db'

#making this global as I am recording data 3 ways 
sense = SenseHat()


#method for recording temperature 
def rec_temp():
    temp = sense.get_temperature()
    if temp is not None:
        temp = round(temp , 1)
        #ask why this doesnt work
        logData(temp)
    return temp

#method for recording humidty
def rec_humid():
    humid = sense.get_humidity()
    if humid is not None:
        humid = round(humid , 1)
        #ask why not working
        logData (humid)
    return humid

#method for recording pressure 
def rec_pressure():
    pressure = sense.get_pressure()
    if pressure is not None:
        pressure = round(pressure, 1)
        #ask why not working
        logData (pressure)
    return pressure

def getAllData():
    temp = rec_temp()
    humid = rec_humid()
    pressure = rec_pressure()
    logData(temp, humid, pressure) 


def logData (temp, humid, pressure):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO SENSEHAT_data values(datetime('now'), (?), (?), (?))", (temp, humid, pressure))
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
    for i in range (0,3):
        getAllData()
    displayData()

# Execute the main function
main()