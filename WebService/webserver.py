#!/usr/bin/env python3
import io
import os
import datetime
import sqlite3
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, render_template, request, send_file, make_response
from sense_hat import SenseHat

conn = sqlite3.connect('/home/pi/IOT/a1/sensehat.db')
curs = conn.cursor()

app = Flask(__name__)

#referenced from https://matplotlib.org/ 
#referenced from https://www.instructables.com/id/From-Data-to-Graph-a-Web-Jorney-With-Flask-and-SQL/

#retrieves the latest data recorded
def getLatestData():
    for row in curs.execute("SELECT * FROM SENSEHAT_data ORDER BY timestamp DESC LIMIT 1"):
        time = str(row[0])
        temp = row[1]
        humid = row[2]
        pressure = row[3]

    return time, temp, humid, pressure
#appends all the data recorded over time to a list
def getHistoricalData():
    curs.execute("SELECT * FROM SENSEHAT_data ORDER BY timestamp DESC LIMIT 20")
    data = curs.fetchall()
    timeData = []
    tempData = []
    humData = []
    pressureData = []
    for row in reversed(data):
        timeData.append(datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S"))
        tempData.append(row[1])
        humData.append(row[2])
        pressureData.append(row[3])

    return timeData, tempData, humData, pressureData
        

# main route 
@app.route("/")
def index():	
	time, temp, humid, pressure = getLatestData()
	templateData = {
		'time': time,
		'temp': temp,
        'hum': humid,
        'pressure': pressure
	}
	return render_template('index.html', **templateData)

#plotting all the data
@app.route('/plot/temp')
def plot_temp():
	times, tempData, humidData, pressureData = getHistoricalData()
	ys = tempData
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Temperature [°C]")
	axis.set_xlabel("Time")
	axis.grid(True)
	xs = times
	axis.plot(xs, ys)
	fig.autofmt_xdate()
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

@app.route('/plot/humid')
def plot_humid():
	times, tempData, humidData, pressureData = getHistoricalData()
	ys = humidData
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Humidity")
	axis.set_xlabel("Time")
	axis.grid(True)
	xs = times
	axis.plot(xs, ys)
	fig.autofmt_xdate()
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

@app.route('/plot/pressure')
def plot_pressure():
	times, tempData, humidData, pressureData = getHistoricalData()
	ys = pressureData
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Pressure")
	axis.set_xlabel("Time")
	axis.grid(True)
	xs = times
	axis.plot(xs, ys)
	fig.autofmt_xdate()
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response




if __name__ == "__main__":
    host = os.popen('hostname -I').read()
    app.run(host='0.0.0.0', port=80, debug=False)
    #app.run(host=host, port=80, debug=False)
