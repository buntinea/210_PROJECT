import paho.mqtt.client as mqtt			# Import the MQTT library
import time	# The time library is useful for delays
from smbus import SMBus
 

idealTemp = 25
insideTemp = 18
outsideTemp = 0
windowOpened = False #window is initially closed
moisture = 0
moistureThreshold = 0
tooWet = False


def openWindow():
    global windowOpened
    print("opening window...")
    time.sleep(3)
    print("window opened")
    windowOpened = True
    if tooWet:
        print("it's raining, so opening the window is not a good idea")
    

def closeWindow():
    global windowOpened
    print("closing window...")
    time.sleep(3)
    print("window closed")
    windowOpened = False

# Our "on message" event
def messageFunction (client, userdata, message):
    
    value = message.payload.decode("utf-8")
    valueFloat = float(value)
    topic = str(message.topic)
    if topic == "MoistureReading":
        global moisture
        global tooWet
        moisture = valueFloat
        if moisture == moistureThreshold:
            tooWet = True
        else:
            tooWet = False
    
    else:
        global outsideTemp
        outsideTemp = valueFloat
        #message = str(value)
        if outsideTemp > insideTemp: #if outside is warmer than inside...
            if not windowOpened:
                openWindow()
        else:
            if windowOpened:
                closeWindow()
    #message = str(message.payload.decode("utf-8"))
    print(topic)
    #print(topic)
    #print(type(valueFloat))
        
    
    
        
    
    
 
ourClient = mqtt.Client("makerio_mqtt")		# Create a MQTT client object
ourClient.connect("test.mosquitto.org", 1883)	# Connect to the test MQTT broker

ourClient.subscribe("MoistureReading")
ourClient.on_message = messageFunction

ourClient.subscribe("tempOutside")			# Subscribe to the topic AC_unit
ourClient.on_message = messageFunction		# Attach the messageFunction to subscription
ourClient.loop_start()				# Start the MQTT client
 
 
# Main program loop
while(1):
	time.sleep(1)				# Sleep for a second