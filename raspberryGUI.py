#this library is for the mqtt connection to the argon
import paho.mqtt.client as mqtt
ourClient = mqtt.Client("makerio_mqtt")		# Create a MQTT client object
ourClient.connect("test.mosquitto.org", 1883)	# Connect to the test MQTT broker


#this is for the raspberry to record the temperature 
import Adafruit_DHT
sensor = Adafruit_DHT.DHT11
DHT11_pin = 23

#smbus library is for the connection to the arduino via i2c
from smbus import SMBus
arduino = SMBus(1)
addr = 0x1

#these libraries are for the GUI
from tkinter import *
from tkinter import ttk
import tkinter.font
import RPi.GPIO as GPIO
from gpiozero import LED
GPIO.setmode(GPIO.BCM)


#thisis for the threading
import threading
import time	





idealTemp = 25 #initial value
insideTemp = 22 #initial value
outsideTemp = 20 #initial value
windowOpened = False #window is initially closed
windowStatus = "closed"
moisture = 0 #initial value
moistureThreshold = 20 #initial value
tooWet = False
weather = "dry"




#function to open the physical window
def openWindow():
    global windowOpened
    global windowStatus
    if not windowOpened and not tooWet:
        print("opening window...")
        arduino.write_byte(addr,0x1)
        time.sleep(3)
        print("window opened")
        windowOpened = True
        windowStatus = "open"
    
        
    
    
#function to close the physical window
def closeWindow():
    global windowOpened
    global windowStatus
    if windowOpened:
        print("closing window...")
        arduino.write_byte(addr,0x0)
        time.sleep(3)
        print("window closed")
        windowOpened = False
        windowStatus = "closed"
        
        

#mqtt function
def messageFunction (client, userdata, message):
    global moisture
    global tooWet
    global outsideTemp
    global windowStatus
    global weather
    value = message.payload.decode("utf-8")
    valueFloat = float(value)
    topic = str(message.topic)
    if topic == "MoistureReading":
        
        
        
        
        #moisture = valueFloat
        if moisture >= moistureThreshold:
            tooWet = True
            windowStatus = "closed (rain)"
            weather = "wet"
        else:
            tooWet = False
            weather = "dry"
        print('moisture:',moisture)
    
    else:
        
        outsideTemp = valueFloat
        
        print('outside temperature:',outsideTemp)
        print('inside temperature:',insideTemp)
        print('prefered temperature:',idealTemp)
        if tooWet:
            closeWindow()
            
        elif outsideTemp > insideTemp: 
            if insideTemp < idealTemp:
                openWindow()
            else:
                closeWindow()               
            
        else:
            if insideTemp <= idealTemp:
                openWindow()
            else:
                closeWindow()
    
        


######Threads#############


def getGui():
    
    
    
    def refreshGui():
        tempOutValue["text"] = outsideTemp
        tempInValue["text"] = insideTemp
        moistureValue["text"] = moisture
        weatherStatus["text"] = weather
        status["text"] = "status:",windowStatus
    
    def updateTemp():
        global idealTemp
        try:
            t = int(temp.get())
        except ValueError:
            #print('prefered temperature remains at:',idealTemp)
            t = 100
        
        if t < 10 or t > 40:
            return
        else:
            idealTemp = t
            yourTempValue["text"] = idealTemp
    
    def updateMoisture():
        
        global moistureThreshold
        try:
            m = int(moist.get())
        except ValueError:
            m = 1000
        
        
        
        if m < 0 or m > 100:
            
            return
        else:
            moistureThreshold = m
            yourRainTolerance["text"] = moistureThreshold
            
        
    
    window = Tk()
    window.title("Window control")
    myFont = tkinter.font.Font(family = 'Helvetica', size=12, weight = "bold")
    
    
    tempIn = tkinter.ttk.Label(window, text = "Inside temperature")
    tempIn.grid(row=1,column=1)
    tempOut = tkinter.ttk.Label(window, text = "Outside temperature")
    tempOut.grid(row=1,column=2)
    moistureValue = tkinter.ttk.Label(window, text = "Outside moisture")
    moistureValue.grid(row=1,column=3)
    weatherTitle = tkinter.ttk.Label(window, text = "weather")
    weatherTitle.grid(row=1,column=4)
    
    tempInValue = tkinter.ttk.Label(window, text = insideTemp)
    tempInValue.grid(row=2,column=1)
    tempOutValue = tkinter.ttk.Label(window, text = outsideTemp)
    tempOutValue.grid(row=2,column=2)
    moistureValue = tkinter.ttk.Label(window, text = moisture)
    moistureValue.grid(row=2,column=3)
    weatherStatus = tkinter.ttk.Label(window, text = weather)
    weatherStatus.grid(row=2,column=4)
    status = tkinter.ttk.Label(window, text = "status: " + windowStatus)
    status.grid(row=4,column=3)
    refreshButton = Button(window, text = 'refresh', font = myFont, command = refreshGui, bg = 'yellow', height = 1, width = 4)
    refreshButton.grid(row=5, column=3)
    
    space1 = ttk.Label(window)
    space1.grid(row=3)
    
    yourTemp = tkinter.ttk.Label(window, text = "your ideal temperature")
    yourTemp.grid(row=4,column=1)
    yourRain= tkinter.ttk.Label(window, text = "your rain tolerance")
    yourRain.grid(row=4,column=2)
    
    yourTempValue = tkinter.ttk.Label(window, text = idealTemp)
    yourTempValue.grid(row=5,column=1)
    yourRainTolerance = tkinter.ttk.Label(window, text = moistureThreshold)
    yourRainTolerance.grid(row=5,column=2)
    
    chooseTemp = ttk.Label(window, text = "choose prefered temperature ")
    chooseTemp.grid(row=6,column=1)
    chooseRainTolerance = ttk.Label(window, text = "choose prefered rain tolerance ")
    chooseRainTolerance.grid(row=6,column=2)
    
    temp = tkinter.StringVar() 
    chooseTempValue = ttk.Entry(window, width = 15, textvariable = temp)
    chooseTempValue.grid(column = 1, row = 7)
    moist = tkinter.StringVar()
    chooseRainToleranceValue = ttk.Entry(window, width = 15, textvariable = moist)
    chooseRainToleranceValue.grid(column = 2, row = 7)
    
    
    tempUpdateButton = Button(window, text = 'update', font = myFont, command = updateTemp, bg = 'red', height = 1, width = 4).grid(row=8, column=1)
    moistureUpdateButton = Button(window, text = 'update', font = myFont, command = updateMoisture, bg = 'red', height = 1, width = 3).grid(row=8, column=2)

    
    window.mainloop()
    
        



def insideTemp():
    global insideTemp
    
    while 1:
        dummy,insideTemp = Adafruit_DHT.read_retry(sensor, DHT11_pin)
        time.sleep(5)
        



def ousideTemp():
    
    ourClient.subscribe("tempOutside")			# Subscribe to the topic AC_unit
    ourClient.on_message = messageFunction		# Attach the messageFunction to subscription
    ourClient.loop_start()				# Start the MQTT client
    time.sleep(5)


def ousideMoisture():
    
    ourClient.subscribe("MoistureReading")
    ourClient.on_message = messageFunction
    ourClient.loop_start()				# Start the MQTT client
    time.sleep(5)



t1 = threading.Thread(target=getGui)
t2 = threading.Thread(target=insideTemp, daemon = True)
t3 = threading.Thread(target=ousideTemp, daemon = True)
t4 = threading.Thread(target=ousideMoisture, daemon = True)


t1.start()
t2.start()
t3.start()
t4.start()

t1.join()



arduino.write_byte(addr,0x0)
print("program terminated")