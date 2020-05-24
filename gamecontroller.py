#!/usr/bin/python3
from threading import Thread
import time
import paho.mqtt.client as mqtt

score = 0
coordinates = [0,0,0,550,750,375,1300,375,score] #wcRol1X, wcRol1Y, wcRol2X, wcRol2Y, wKarX, wKarY, virusX, virusY
canvasWidth, canvasHeight = 1500, 750
clientID = 1
collisionMargin = 150
maxScore = 5

class GameObject:
    X = 0
    Y = 0
    def __init__(self, XCoord, YCoord):
        self.X = XCoord
        self.Y = YCoord

class WcRol(GameObject):
    Xspeed = 10
    Yspeed = 10
    
class WinkelKar(GameObject):
    Xspeed = 10
    Yspeed = 0

class Virus(GameObject):
    Xspeed = -15
    Yspeed = 10

wcRol1 = WcRol(coordinates[0], coordinates[1])
wcRol2 = WcRol(coordinates[2], coordinates[3])
winkelKar = WinkelKar(coordinates[4], coordinates[5])
virus = Virus(coordinates[6], coordinates[7])

def coordUpdate():
    global coordinates
    coordinates[0] = wcRol1.X
    coordinates[1] = wcRol1.Y
    coordinates[2] = wcRol2.X
    coordinates[3] = wcRol2.Y
    coordinates[4] = winkelKar.X
    coordinates[5] = winkelKar.Y
    coordinates[6] = virus.X
    coordinates[7] = virus.Y
    coordinates[8] = score

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: "+str(rc))
    #client.subscribe("testtopic/apLab6/raspklas")

def on_message(client, userdata, msg):
    print("Message : "+str(msg.payload))

    #Wanneer een rpi een bericht stuurt met als msg CNCT, voer initialConnection uit
    if str(msg.topic) == "rpiproject/initialize":
        initialConnection(str(msg.payload))

    #moveUp, met als arg het ID
    elif str(msg.topic) == "rpiproject/up":
        moveUp(str(msg.payload).strip("b' ").replace(" ", ""))

    #moveDown, met als arg het ID
    if str(msg.topic) == "rpiproject/down":
        moveDown(str(msg.payload).strip("b' ").replace(" ", ""))
    

client = mqtt.Client(client_id="GameController",userdata="GameControllerUserdata")
client.on_connect=on_connect
client.on_message=on_message
client.connect("ldlcreations.ddns.net", 1883, 60)
client.subscribe("rpiproject/initialize")
client.subscribe("rpiproject/up")
client.subscribe("rpiproject/down")
client.loop_start()

#Elke controller is gesubscribed op het topic "rpirpiproject/"+ zijn eigen client naam
#Naar die topic wordt een string gestuurd met daarin het clientID, zo verkrijgt iedereen een verschillend clientID 
def initialConnection(msg):
    global clientID
    msgClient = msg.strip("b' ").replace(" ", "")
    print(msgClient)
    publishName = "rpiproject/"+str(msgClient)
    client.publish(publishName, str(clientID))
    clientID += 1
    if clientID == 5:
        client.publish("rpiproject/start","START")


def checkCollision():
    global wcRol1, wcRol2, winkelKar, virus
    global score

    #Collision winkelKar wcRol1
    if baseCollision(wcRol1.X, wcRol1.Y, winkelKar.X, winkelKar.Y):
        wcRol1.X = 0
        score += 1
    #Collision winkelKar wcRol2
    if baseCollision(wcRol2.X, wcRol2.Y, winkelKar.X, winkelKar.Y):
        wcRol2.X = 0
        score += 1
    #Collision winkelKar virus
    if baseCollision(virus.X, virus.Y, winkelKar.X, winkelKar.Y):
        virus.X = canvasWidth
        #score = 0

    #Collision virus wcRol1
    if baseCollision(wcRol1.X, wcRol1.Y, virus.X, virus.Y):
        virus.X = canvasWidth
        wcRol1.X = 0
    #Collision virus wcRol2
    if baseCollision(wcRol2.X, wcRol2.Y, virus.X, virus.Y):
        virus.X = canvasWidth
        wcRol2.X = 0
    
def baseCollision(obj1X, obj1Y, obj2X, obj2Y):
    if (obj1Y >= obj2Y and obj1Y <= obj2Y + collisionMargin) or (obj1Y+collisionMargin >= obj2Y and obj1Y+collisionMargin <= obj2Y + collisionMargin):
        if (obj1X >= obj2X and obj1X <= obj2X + collisionMargin) or (obj1X+collisionMargin >= obj2X and obj1X+collisionMargin <= obj2X + collisionMargin):
            return True
        else: 
            return False
    else: 
        return False

def checkBoundaries():
    global wcRol1, wcRol2, winkelKar, virus
    #Check coordinates in x direction, reset /stop if necessary
    if wcRol1.X >= canvasWidth:
        wcRol1.X = 0
    if wcRol2.X >= canvasWidth:
        wcRol2.X = 0
    if virus.X <= 0:
        virus.X = canvasWidth
    #Winkelkar between boundaries of 1/3 and 2/3 of canvaswidth
    if winkelKar.X <= 500:
        winkelKar.X = 500
    if winkelKar.X >= 1000-collisionMargin:
        winkelKar.X = 1000-collisionMargin

    #Check coordinates in y direction, reset / stop if necessary
    if wcRol1.Y <= 0:
        wcRol1.Y = 0
    if wcRol2.Y <= 0:
        wcRol2.Y = 0
    if virus.Y <= 0:
        virus.Y = 0
    if winkelKar.Y <= 0:
        winkelKar.Y = 0

    if wcRol1.Y >= canvasHeight-collisionMargin:
        wcRol1.Y = canvasHeight-collisionMargin
    if wcRol2.Y >= canvasHeight-collisionMargin:
        wcRol2.Y = canvasHeight-collisionMargin
    if virus.Y >= canvasHeight-collisionMargin:
        virus.Y = canvasHeight-collisionMargin
    if winkelKar.Y >= canvasHeight-collisionMargin:
        winkelKar.Y = canvasHeight-collisionMargin

def autoMove():
    global coordinates
    wcRol1.X += wcRol1.Xspeed
    wcRol2.X += wcRol1.Xspeed
    virus.X += virus.Xspeed
    
def moveUp(id): #Or left for winkelkar
    global coordinates
    if id == "1":
        wcRol1.Y -= wcRol1.Yspeed
    elif id == "2":
        wcRol2.Y -= wcRol2.Yspeed
    elif id == "3":
        winkelKar.X -= winkelKar.Xspeed
    elif id == "4":
        virus.Y -= virus.Yspeed

def moveDown(id): #Or right for winkelkar
    global coordinates
    if id == "1":
        wcRol1.Y += wcRol1.Yspeed
    elif id == "2":
        wcRol2.Y += wcRol2.Yspeed
    elif id == "3":
        winkelKar.X += winkelKar.Xspeed
    elif id == "4":
        virus.Y += virus.Yspeed

#Alleen als alle 4 de deelnemers een id hebben gekregen zal het spel starten
while clientID < 5:
    pass

#Loop
while score < maxScore:
    time.sleep(0.1)
    autoMove()
    checkCollision()
    checkBoundaries()
    coordUpdate()
    client.publish("rpiproject/coord",str(coordinates).strip('[]'))

coordUpdate()
client.publish("rpiproject/coord",str(coordinates).strip('[]'))

client.publish("rpiproject/gameover", "Gameover")
client.disconnect()

