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

def send_message(send_notification_via_pushbullet):
    cpu_temp = os.popen("vcgencmd measure_temp").readline()
    cpu_temp = cpu_temp.replace("temp=", "")
    cpu_temp = float(cpu_temp.replace("'C\n",""))

    accurateTemp = round(cpu_temp - sense.get_temperature() , 1)
    
    

    sense.show_message('Temp: {0:0.1f} *c'.format(accurateTemp), scroll_speed=0.05)
    sense.clear()


    with open('setTemp.config', 'r') as f:
        set_temp = f.read()
            
    if int(set_temp) < accurateTemp:
            send_notification_via_pushbullet("The temperature is " + str(accurateTemp), "a sweater is not needed")
    else:
            send_notification_via_pushbullet("The temperature is " + str(accurateTemp), "you should bring a sweater!")






#main function
def main():
    send_message(send_notification_via_pushbullet)

#Execute
main()