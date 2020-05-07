#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

#Knop1=1
#Knop2=2
#LedRoodWC=3
#LedGeelKar=4
#LedGroenVirus=5
ID = ""
GPIO.setmode(GPIO.BCM)
segments =  (27,22,9,11,0,5,6,10)
i=0
for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)
    print("segment setup "+ str(segment))

digits = (14,15,18,17)

for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)
    print("digit setup "+ str(digit))

num = {' ':(0,0,0,0,0,0,0),
    '0':(1,1,1,0,1,1,1),
    '1':(0,0,1,0,1,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(0,1,1,1,1,0,1),
    '4':(0,0,1,1,1,1,0),
    '5':(0,1,1,1,0,1,1),
    '6':(1,1,1,0,0,1,0),
    '7':(1,0,0,0,0,1,1),
    '8':(1,1,1,1,1,1,1),
    '9':(0,0,1,1,1,1,1)}

#while i<1:
#    GPIO.setup(Knop1, GPIO.IN)
#    GPIO.setup(Knop2, GPIO.IN)
#
#    GPIO.setup(LedRoodWC, GPIO.OUT)
#    GPIO.setup(LedGeelKar, GPIO.OUT)
#    GPIO.setup(LedGroenVirus, GPIO.OUT)
#
#    GPIO.output(LedRoodWC, True)
#    GPIO.output(LedGeelKar, True)
#    GPIO.output(LedGroenVirus, True)
#    i = i+1
#    print("Setup complete")

try:
    while True:
        n = time.ctime()[11:13]+time.ctime()[14:16]
        s = str(n).rjust(4)
        for digit in range(4):
            for loop in range(0,7):
                GPIO.output(segments[loop], num[s[digit]][loop])
                print(str(num[s[digit]]))
                time.sleep(1)
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

    
