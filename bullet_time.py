#!/usr/bin/env python3
import requests
import json
import os
import time
from sense_hat import SenseHat

sense = SenseHat()

ACCESS_TOKEN="o.Nj1Zp70ZxuwLL0DyNOLD5OOqOed3rpHJ"

def send_notification_via_pushbullet(title, body):
    """ Sending notification via pushbullet.
        Args:
            title (str) : title of text.
            body (str) : Body of text.
    """
    data_send = {"type": "note", "title": title, "body": body}
 
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 
                         'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something wrong')
    else:
        print('complete sending')

#not sure if I have to make a seperate file to record accurate temperature 
def too_cool():
    cpu_temp = os.popen("vcgencmd measure_temp").readline()
    temp = float(cpu_temp.replace("temp=","").replace("'C\n",""))
    return(temp)

def send_message():
    humid = sense.get_temperature_from_humidity()
    pressure = sense.get_temperature_from_pressure()
    t_cpu = too_cool()

    # calculates the real temperature compesating CPU heating
    t = (humid + pressure)/2
    t_corrected = t - ((t_cpu - t)/1.5)

    title = "It is less than 20 degrees!"
    note = "You should bring a sweater"

    if t_corrected < 20:
         send_notification_via_pushbullet(title, note)  #is there a better way of doing this?
         time.sleep(300) #set to 5 minutes so phone doesn't get spammed




#main function
def main():
    send_message()

#Execute
main()