#!/usr/bin/python3
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time


Knop1=6
Knop2=13
LedRoodWC=8
LedGeelKar=25
LedGroenVirus=24
ID = "2"
GPIO.setmode(GPIO.BCM)
segments =  (17,27,22,9,11,0,5,10)
i=0
VAR = ""
def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    global VAR
    #print(str(msg.payload))
    VAR = str(msg.payload)

client = mqtt.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish
client.connect("ldlcreations.ddns.net", 1883, 60)
client.subscribe("rpiproject/coord")

client.loop_start()

for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)
    print("segment setup "+ str(segment))

digits = (14,15,18,23)

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

def icKnopChange(channel):
    global Knop1
    global Knop2
    if channel == Knop1:
        if GPIO.input(channel) == GPIO.LOW:
            print("Knop1 pressed")
    elif channel == Knop2:
        if GPIO.input(channel) == GPIO.LOW:
            print("Knop2 pressed")






while i<1:
    global ID
    GPIO.setup(Knop1, GPIO.IN)
    GPIO.setup(Knop2, GPIO.IN)

    GPIO.setup(LedRoodWC, GPIO.OUT)
    GPIO.setup(LedGeelKar, GPIO.OUT)
    GPIO.setup(LedGroenVirus, GPIO.OUT)
    GPIO.add_event_detect( Knop1, GPIO.FALLING, callback=icKnopChange, bouncetime=1 )
    GPIO.add_event_detect( Knop2, GPIO.FALLING, callback=icKnopChange, bouncetime=1 )
    if ID == "1":
        GPIO.output(LedRoodWC, True)
        GPIO.output(LedGeelKar, False)
        GPIO.output(LedGroenVirus, False)
    elif ID == "2":
        GPIO.output(LedRoodWC, False)
        GPIO.output(LedGeelKar, True)
        GPIO.output(LedGroenVirus, False)
    elif ID == "3":
        GPIO.output(LedRoodWC, False)
        GPIO.output(LedGeelKar, False)
        GPIO.output(LedGroenVirus, True)
    else:
        GPIO.output(LedRoodWC, False)
        GPIO.output(LedGeelKar, False)
        GPIO.output(LedGroenVirus, False)
    i = i+1
    print("Setup complete")

try:
    while True:
        #n = time.ctime()[11:13]+time.ctime()[14:16]
        s = ID
        for digit in range(4):
            for loop in range(0,7):
                GPIO.output(segments[loop], num[s[digit]][loop])
                print(str(segments[loop]))
                print(str(num[s[digit]]))
                if (int(time.ctime()[18:19])%2 == 0) and (digit == 1):
                    GPIO.output(10, 1)
                else:
                    GPIO.output(10, 0)
            #print("nummer "+str(digits[digit]))
            GPIO.output(digits[digit], 0)
            time.sleep(0.001)
            GPIO.output(digits[digit], 1)
        
finally:
    GPIO.cleanup()

    
