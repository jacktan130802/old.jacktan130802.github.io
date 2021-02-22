from flask import Flask, render_template, redirect, url_for
import psutil
import datetime
import os
import water
import RPi.GPIO as GPIO
from time import sleep

app = Flask(__name__)

def template(title = "HELLO!", text = ""):  #defines template function with 2 arguments, title = "string" and text = empty string)
    now = datetime.datetime.now() #defines now variable as datetime.datetime.now() which will show the time and date at current time.
    timeString = now #defines timeString variable as now 
    templateDate = {   #dictionary
        'title' : title,
        'time' : timeString,
        'text' : text
        }
    return templateDate #returns dictionary list 

@app.route("/") #home page of the web server
def hello(): 
    templateData = template() 
    return render_template('main.html', **templateData)  #renders template file main.html and templateData takes template() to show the title,time and text 

@app.route("/last_watered") 
def check_last_watered():
    templateData = template(text = water.get_last_watered()) #text shows the reading of last watered timing, which is written into the txt file when the pump_on function is executed
    return render_template('main.html', **templateData) #renders template file main.html and templateData takes template() to show title, time and text. In this case,
#text = water.get_last_watered()) in a datetime format 

@app.route("/sensor") 
def action():
    status = water.get_status() #defining status variable as execution of get_status function 
    message = "" #variable message defined as string 
    if (status == 0): # status == 0 dry = high resistance = low output
        message = "Water me please!" #message printed on the web if moisture sensor has a low output 
    else: #wet = low resistance = high output 
        message = "I'm a watered plant" #message printed on the web if moisture sensor has a high output

    templateData = template(text = message) 
    return render_template('main.html', **templateData)

@app.route("/water")
def action2():
    water.pump_on() #executes pump_on function 
    templateData = template(text = "Watered Once")
    return render_template('main.html', **templateData) 

@app.route("/auto/water/<toggle>")
def auto_water(toggle):
    running = False 
    GPIO.setup(24,GPIO.OUT) #set GPIO24 as output 
    status = water.get_status() #returns moisture sensor input 
    if toggle == "ON": #if Auto watering on button is pressed, brings to /auto/water/ON/, the @app.route code runs and the if side of the code runs
        templateData = template(text = "Auto Watering On") #text = Auto watering on
        while(status==0):   #while moisture sensor senses dry 
            GPIO.output(24,1)
            sleep(1000)
            water.get_status()
            #on LED
     #returns moisture sensor input if status = dry, and loop continues if status == 0 (dry)
        else: #if wet
            GPIO.output(24,0) #off LED 
            templateData = template(text = "Auto Watering Off") #text changes to auto watering off on the webserver
            os.system("pkill -f water.py") #kills the program
    else: #in the case when Auto watering off button is pressed, brings to /auto/water/OFF/, the @app.route code runs and the else side of the code runs
        GPIO.output(24,0) #off LED
        templateData = template(text = "Auto Watering Off")  #text changes to auto watering off on the webserver
        os.system("pkill -f water.py") #kills the program
    
    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
