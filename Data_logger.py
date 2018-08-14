import sys
import sqlite3 as lite
from sense_hat import SenseHat
from datetime import datetime

sense = SenseHat()

def get_sense_data():
    sense_data = []
    sense.get_humidity()
    datetime.now()

while True:
    print(get_sense_data())