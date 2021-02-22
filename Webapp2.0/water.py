# External module imp
import RPi.GPIO as GPIO
import datetime
from time import sleep


GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme


    

def get_last_watered(): #definition of function
    try:
        f = open("last_watered.txt", "r")  #reads the datetime of last watered 
        return f.readline() #returns the reading
    except:
        return "NEVER!"
      
def get_status(pin = 4): # definition of function get_status with argument pin = 4 for moisture sensor  
    GPIO.setup(pin, GPIO.IN) #makes GPIO27 an input pin 
    return GPIO.input(pin)#returns the reading from GPIO.input(4)


    
#def auto_water(delay = 5, pump_pin = 26, water_sensor_pin = 4):
    #consecutive_water_count = 0
   #print("Here we go! Press CTRL+C to exit")
    #try:
       # while 1 and consecutive_water_count < 10:
           # time.sleep(30)
            #wet = get_status(pin = water_sensor_pin) == 0 
           # if not wet:  #if dry and water count <5, pump_on and water count +=1
            #    if consecutive_water_count < 5: 
            #        pump_on(pump_pin, 1)
             #   consecutive_water_count += 1
           # else: # if dry and water count >5, water_count = 0 
         #       consecutive_water_count = 0
  #  except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
      #  GPIO.cleanup() # cleanup all GPI

def pump_on(pump_pin = 26, delay = 1): #defines function pump_on with two arguments [pump pin = GPIO26 with 1 second delay]
    f = open("last_watered.txt", "w") #opens and writes datetime of last watered
    f.write("Last watered {}".format(datetime.datetime.now())) #writes time  into last_watered.txt file
    f.close()
    GPIO.setup(26,GPIO.OUT) #setup GPIO26 as the output pin 
    GPIO.setwarnings(False)
    PWM=GPIO.PWM(26,50) #set 50Hz PWM output at GPIO26
    while True:
     PWM.start(3) #3% duty cycle
     print('duty cycle:', 3) #3 o'clock position
     sleep(4) #allow time for movement 
     PWM.start(12) #12% duty cycle
     print('duty cycle:', 12) #9 o'clock position
     sleep(4) #allow time for movement
     break #loop is broken after the previous line sleep(4)finishes
