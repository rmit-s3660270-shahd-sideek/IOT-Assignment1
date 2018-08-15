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


#method for recording all 3 types 
def rec_data():
    humid = sense.get_humidity() #recoding humidity
    if humid is not None: #Can I group temp and pressure on this same line?
        humid = round(humid , 1) 
    temp = sense.get_temperature() #recording tempetature 
    if temp is not None:
        temp = round(temp , 1)
    pressure = sense.get_pressure() #recording pressure 
    if pressure is not None:
        pressure = round(pressure, 1)
        logData (humid , temp , pressure)
 

def logData (humid, temp, pressure):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO SENSEHAT_data values(datetime('now'), (?), (?), (?))", (humid, temp, pressure))
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