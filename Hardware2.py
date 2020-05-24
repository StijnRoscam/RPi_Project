#!/usr/bin/python3
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

up=6
down=13
LedRoodWC=8
LedGeelKar=25
LedGroenVirus=24
clientName="stijn"
clientID = ""
GPIO.setmode(GPIO.BCM)
segments =  (17,27,22,9,11,0,5,10)
digits = (14,15,18,23)
VAR = "empty"

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    global VAR
    print(str(msg.payload))
    VAR = str(msg.payload)

client = mqtt.Client(clientName)
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish
client.connect("ldlcreations.ddns.net", 1883, 60)

subscriptionName = "rpiproject/"+str(clientName)
#subscribe on own topic
client.subscribe(subscriptionName)
client.loop_start()

while VAR == "empty":
    #Every second you dont get a message from gamecontroller, you publish your name again
    client.publish("rpiproject/initialize", clientName, qos=0)
    time.sleep(1)


#clientID equals the payload of the message received
clientID = VAR.strip("b'").replace(" ","")
print("Your is is: "+clientID)

for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)
    print("segment setup "+ str(segment))

for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)
    print("digit setup "+ str(digit))

num = {' ':(0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,0,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,1,0,1,1)}

def publishUp(channel):
    client.publish("rpiproject/up",str(clientID), qos=0)

def publishDown(channel):
    client.publish("rpiproject/down",str(clientID), qos=0)

#Setup pins
GPIO.setup(up, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(down, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(LedRoodWC, GPIO.OUT)
GPIO.setup(LedGeelKar, GPIO.OUT)
GPIO.setup(LedGroenVirus, GPIO.OUT)
GPIO.output(LedGeelKar,False)
GPIO.output(LedGroenVirus,False)
GPIO.output(LedRoodWC,False)

GPIO.add_event_detect( up, GPIO.RISING, callback=publishUp, bouncetime=20 )
GPIO.add_event_detect( down, GPIO.RISING, callback=publishDown, bouncetime=20 )

if clientID == "1" or clientID =="2":
    GPIO.output(LedRoodWC, True)
elif clientID == "3":
    GPIO.output(LedGeelKar, True)
elif clientID == "4":
    GPIO.output(LedGroenVirus, True)

#Show 
#for digit in range(1):
    #for loop in range(0,7):
    #    GPIO.output(segments[loop], num[clientID][loop])
GPIO.output(22, True)
GPIO.output(27, True)
GPIO.output(14, True)
        

input("Wait for input to end game..")
        
GPIO.cleanup()

    