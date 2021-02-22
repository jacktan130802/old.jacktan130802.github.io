import spidev #import SPI library
import RPi.GPIO as GPIO #import RPi.GPIO module, rename it as GPIO
from time import sleep


GPIO.setmode(GPIO.BCM) #choose BCM mode, refer to pins as GPIO no.
GPIO.setwarnings(False)
GPIO.setup(24,GPIO.OUT) #set GPIO 24 as output



spi=spidev.SpiDev() #create SPI object
spi.open(0,0) #open SPI port 0, device (CS) 0

def readadc(adcnum):
    #read SPI data from the MCP3008, 8 channels in total
    if adcnum>7 or adcnum<0:
        return -1
    spi.max_speed_hz = 1350000
    r=spi.xfer2([1,8+adcnum<<4,0])
        #construct list of 3 items, before sending to ADC:
        #1(start), (single-ended+channel#) shifted left 4 bits, 0(stop)
        #see MCP3008 datasheet for details
    data=((r[1]&3)<<8)+r[2]
        #ADD first byte with 3 or 0b00000011 - masking operation
        #shift result left by 8 bits
        #OR result with second byte, to get 10-bit ADC result
    return data

while (True):
    LDR_value=readadc(0) #read ADC channel 0 i.e. LDR
    print("LDR = ", LDR_value) #print result
    if(LDR_value<700):
        GPIO.output(24,1) #output logic high/'1'
    else :
       GPIO.output(24,0) #output logic high/'1'

    sleep(1)
