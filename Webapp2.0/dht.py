
import Adafruit_DHT
import time
import requests
from time import sleep

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 21
myUploadAPI = "VF5MDPJ1HCI9N03W" #modify this to yours
baseURL = 'https://api.thingspeak.com/update?api_key=%s' %myUploadAPI

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
        resp = requests.get ("https://api.thingspeak.com/update?api_key=VF5MDPJ1HCI9N03W&field1=%s&field2=%s" %(temperature, humidity)) #not really sure about this part 
    else:
        print("Sensor failure. Check wiring.");
    time.sleep(15);
    
GPIO.setmode(GPIO.BCM) #choose BCM mode
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.IN) #set GPIO 4 as input

def get_status(pin = 4):
    GPIO.setup(4,GPIO.IN) 
    return GPIO.input(pin)
