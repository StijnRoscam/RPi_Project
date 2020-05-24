#!/usr/bin/python3
from threading import Thread
import time
import paho.mqtt.client as mqtt

score = 0
coordinates = [0,0,0,550,750,375,1300,375,score] #wcRol1X, wcRol1Y, wcRol2X, wcRol2Y, wKarX, wKarY, virusX, virusY
canvasWidth, canvasHeight = 1500, 750
clientID = 1
collisionMargin = 120
maxScore = 15

class GameObject:
    X = 0
    Y = 0
    def __init__(self, XCoord, YCoord):
        self.X = XCoord
        self.Y = YCoord

class WcRol(GameObject):
    Xspeed = 5
    Yspeed = 10
    
class WinkelKar(GameObject):
    Xspeed = 10
    Yspeed = 0

class Virus(GameObject):
    Xspeed = -10
    Yspeed = 10

wcRol1 = WcRol(coordinates[0], coordinates[1])
wcRol2 = WcRol(coordinates[2], coordinates[3])
winkelKar = WinkelKar(coordinates[4], coordinates[5])
virus = Virus(coordinates[6], coordinates[7])

#update coordinates with correct values
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

def on_message(client, userdata, msg):
    #When a message is received on rpiproject/initialize, do initialConnection()
    if str(msg.topic) == "rpiproject/initialize":
        initialConnection(str(msg.payload))

    #moveUp, with arg the given ID
    elif str(msg.topic) == "rpiproject/up":
        moveUp(str(msg.payload).strip("b' ").replace(" ", ""))

    #moveDown, with arg the given ID
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

# Every rpi is subscribed on his own topic 'rpiproject/' + his own client name
# The gamecontroller wil send the clientID to this topic, this way everyone has a different clientID 
def initialConnection(msg):
    global clientID
    msgClient = msg[2:].strip("'").replace(" ", "")
    print(msgClient+" is joining the game")
    publishName = "rpiproject/"+str(msgClient)
    client.publish(publishName, str(clientID))
    clientID += 1

def checkCollision():
    global wcRol1, wcRol2, winkelKar, virus
    global score

    #Collision winkelKar wcRol1
    if baseCollision(wcRol1, winkelKar):
        wcRol1.X = 0
        score += 1
    #Collision winkelKar wcRol2
    if baseCollision(wcRol2, winkelKar):
        wcRol2.X = 0
        score += 1
    #Collision winkelKar virus
    if baseCollision(virus, winkelKar):
        virus.X = canvasWidth
        #score = 0

    #Collision virus wcRol1
    if baseCollision(wcRol1, virus):
        virus.X = canvasWidth
        wcRol1.X = 0
    #Collision virus wcRol2
    if baseCollision(wcRol2, virus):
        virus.X = canvasWidth
        wcRol2.X = 0

#Based on the x & y coordinates of 2 objects, determines if there is a collision or not    
def baseCollision(obj1, obj2):
    if (obj1.Y >= obj2.Y and obj1.Y <= obj2.Y + collisionMargin) or (obj1.Y+collisionMargin >= obj2.Y and obj1.Y+collisionMargin <= obj2.Y + collisionMargin):
        if (obj1.X >= obj2.X and obj1.X <= obj2.X + collisionMargin) or (obj1.X+collisionMargin >= obj2.X and obj1.X+collisionMargin <= obj2.X + collisionMargin):
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

# Only if 4 id's have been handed out the game wil start (coordinates will be send to GUI)
while clientID < 5:
    pass

#Loop as long as score is lower than the maximum score
while score < maxScore:
    time.sleep(0.1)
    autoMove()
    checkCollision()
    checkBoundaries()
    coordUpdate()
    client.publish("rpiproject/coord",str(coordinates).strip('[]'))

client.disconnect()

