import paho.mqtt.client as mqtt			# Import the MQTT library
import time	# The time library is useful for delays




from tkinter import *
from tkinter import ttk
import tkinter.font
from gpiozero import LED
import RPi.GPIO
import time
RPi.GPIO.setmode(RPi.GPIO.BCM)


import threading


ourClient = mqtt.Client("makerio_mqtt")		# Create a MQTT client object
ourClient.connect("test.mosquitto.org", 1883)	# Connect to the test MQTT broker


idealTemp = 25
insideTemp = 22
outsideTemp = 20
windowOpened = False #window is initially closed
moisture = 0
moistureThreshold = 20
tooWet = False

weatherStatus = "dry"

windowStatus = "window opened"

def getOutsideTemp():
    return outsideTemp

def closeGUI():
    RPi.GPIO.cleanup()
    window.destroy()


def openWindow():
    global windowOpened
    if not windowOpened:
        print("opening window...")
        #arduino.write_byte(addr,0x1)
        time.sleep(3)
        print("window opened")
        windowOpened = True
    
        
    
    

def closeWindow():
    global windowOpened
    if windowOpened:
        print("closing window...")
        #arduino.write_byte(addr,0x0)
        time.sleep(3)
        print("window closed")
        windowOpened = False
        
        

def messageFunction (client, userdata, message):
    global moisture
    global tooWet
    global outsideTemp
    value = message.payload.decode("utf-8")
    valueFloat = float(value)
    topic = str(message.topic)
    if topic == "MoistureReading":
        #print(topic)
        
        
        moisture = valueFloat
        if moisture >= moistureThreshold:
            tooWet = True
        else:
            tooWet = False
            #print(moisture)
        #print("Moisture: " + moisture + " (" + tooWet + ")")
        print(topic)
        print(moisture)
    
    else:
        
        i = insideTemp
        outsideTemp = valueFloat
        print(topic)
        print(outsideTemp)
        #print("Outside temperature: " + outsideTemp + ", Inside temperature: " + i)
        #message = str(value)
        if tooWet:
            closeWindow()
            
        elif outsideTemp > i: #if outside is warmer than inside...
            if i < idealTemp:
                openWindow()
            else:
                closeWindow()               
            
        else:
            if i <= idealTemp:
                closeWindow()
            else:
                openWindow()
    #message = str(message.payload.decode("utf-8"))
    #print(topic)
    #print(topic)
    #print(type(valueFloat))
        


######Threads#############


def getGui():
    window = Tk()
    window.title("Window control")
    myFont = tkinter.font.Font(family = 'Helvetica', size=12, weight = "bold")
    yourTemp = tkinter.ttk.Label(window, text = "your ideal temperature").grid(row=1,column=1)
    yourTempValue = tkinter.ttk.Label(window, text = idealTemp).grid(row=2,column=1)
    tempOut = tkinter.ttk.Label(window, text = "Outside temperature").grid(row=1,column=2)
    tempOutValue = tkinter.ttk.Label(window, text = outsideTemp).grid(row=2,column=2)
    tempIn = tkinter.ttk.Label(window, text = "Inside temperature").grid(row=1,column=3)
    tempInValue = tkinter.ttk.Label(window, text = insideTemp).grid(row=2,column=3)
    weather = tkinter.ttk.Label(window, text = "weather").grid(row=1,column=4)
    weatherStatus = tkinter.ttk.Label(window, text = "dry").grid(row=2,column=4)
    chooseTemp = tkinter.ttk.Label(window, text = "choose prefered temperature").grid(row=4,column=1)
    chooseTempValue = tkinter.ttk.Label(window, text = "<your temp>").grid(row=5,column=1)
    chooseRainTolerance = tkinter.ttk.Label(window, text = "choose rain tolerance").grid(row=4,column=2)
    chooseRainToleranceValue = tkinter.ttk.Label(window, text = "<rain>").grid(row=5,column=2)
    updateButton = Button(window, text = 'update', font = myFont, command = closeGUI, bg = 'red', height = 1, width = 3).grid(row=5, column=3)

    status = tkinter.ttk.Label(window, text = "status: " + windowStatus).grid(row=7,column=1)
    
    while 1:
        window.mainloop()
        time.sleep(3)
        tempOut["text"] = getOutsideTemp() 


def insideTemp():
    global insideTemp
    while 1:
        insideTemp = 17
        print(insideTemp)
        time.sleep(5)




def ousideTemp():
    #ourClient.subscribe("MoistureReading")
    #ourClient.on_message = messageFunction

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
t2 = threading.Thread(target=insideTemp)
t3 = threading.Thread(target=ousideTemp)
t4 = threading.Thread(target=ousideMoisture)


t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()
