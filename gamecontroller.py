from threading import Thread
import time
import paho.mqtt.client as mqtt

coordinates = [0,0,0,650,750,375,1400,375] #wcRol1X, wcRol1Y, wcRol2X, wcRol2Y, wKarX, wKarY, virusX, virusY
canvasWidth, canvasHeight = 1500, 750
startGame = False
clientID = 1
moveSpeed = 5
score = 0
collisionMargin = 60


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: "+str(rc))
    #client.subscribe("testtopic/apLab6/raspklas")

def on_message(client, userdata, msg):
    print("Message : "+str(msg.payload))

    #Wanneer een rpi een bericht stuurt met als msg CNCT, voer initialConnection uit
    if str(msg.payload)[1:5] == "CNCT":
        initialConnection(client)

    #moveUp, met als arg het ID
    if str(msg.payload)[7:14] == "MOVE=UP":
        moveUp(str(msg.payload)[5:6])

    #moveDown, met als arg het ID
    elif str(msg.payload)[7:14] == "MOVE=DN":
        moveDown(str(msg.payload)[5:6])
    

client = mqtt.Client("GameController")
client.on_connect=on_connect
client.on_message=on_message
client.connect("ldlcreations.ddns.net", 1883, 60)
client.subscribe("rpiproject/controller")
client.loop_start()

#Elke controller is gesubscribed op het topic "rpirpiproject/"+ zijn eigen client naam
#Naar die topic wordt een string gestuurd met daarin het clientID, zo verkrijgt iedereen een verschillend clientID 
def initialConnection(client):
    client.publish("rpiproject/"+client, str(clientID))
    clientID += 1
    if clientID == 5:
        client.publish("rpiproject/coord","START")


def checkCollision():
    global coordinates
    global score
    #wcRol width:       50px, height 60px
    #winkelKar width:   50px, height 40px
    #virus width:       50px, height 53px

    #Collision winkelKar wcRol1
    if baseCollision(coordinates[0], coordinates[1], coordinates[4], coordinates[5]):
        coordinates[0] = 0
        score += 1
    #Collision winkelKar wcRol2
    if baseCollision(coordinates[2], coordinates[3], coordinates[4], coordinates[5]):
        coordinates[2] = 0
        score += 1
    #Collision winkelKar virus
    if baseCollision(coordinates[6], coordinates[7], coordinates[4], coordinates[5]):
        coordinates[6] = canvasWidth
        score = 0

    #Collision virus wcRol1
    if baseCollision(coordinates[0], coordinates[1], coordinates[6], coordinates[7]):
        coordinates[6] = canvasWidth
        coordinates[0] = 0
    #Collision virus wcRol2
    if baseCollision(coordinates[2], coordinates[3], coordinates[6], coordinates[7]):
        coordinates[6] = canvasWidth
        coordinates[2] = 0
    

def baseCollision(obj1X, obj1Y, obj2X, obj2Y):
    if (obj1Y >= obj2Y and obj1Y <= obj2Y + collisionMargin) or (obj1Y+collisionMargin >= obj2Y and obj1Y+collisionMargin <= obj2Y + collisionMargin):
        if (obj1X >= obj2X and obj1X <= obj2X + collisionMargin) or (obj1X+collisionMargin >= obj2X and obj1X+collisionMargin <= obj2X + collisionMargin):
            return True
        else: 
            return False
    else: 
        return False

def checkBoundaries():

    global coordinates
    #Check coordinates in x direction, reset /stop if necessary
    if coordinates[0] >= canvasWidth:
        coordinates[0] = 0
    if coordinates[2] >= canvasWidth:
        coordinates[2] = 0
    if coordinates[6] <= 0:
        coordinates[6] = canvasWidth
    #Winkelkar between boundaries of 1/3 and 2/3 of canvaswidth
    if coordinates[4] <= 500:
        coordinates[4] = 500
    if coordinates[4] >= 1000-40:
        coordinates[4] = 1000-40

    #Check coordinates in y direction, reset / stop if necessary
    if coordinates[1] <= 0:
        coordinates[1] = 0
    if coordinates[3] <= 0:
        coordinates[3] = 0
    if coordinates [7] <= 0:
        coordinates[7] = 0
    if coordinates [5] <= 0:
        coordinates[5] = 0

    if coordinates[1] >= canvasHeight-60:
        coordinates[1] = canvasHeight-60
    if coordinates[3] >= canvasHeight-60:
        coordinates[3] = canvasHeight-60
    if coordinates [7] >= canvasHeight-60:
        coordinates[7] = canvasHeight-60
    if coordinates [5] >= canvasHeight-60:
        coordinates[5] = canvasHeight-60

def autoMove():
    global coordinates
    coordinates[0] += 5
    coordinates[2] += 5
    coordinates[6] -= 5

    #test vertical movement
    moveDown("1")
    


def moveUp(id): #Or left for winkelkar
    global coordinates
    if id == "1":
        coordinates[1] -= 5
    elif id == "2":
        coordinates[3] -= 5
    elif id == "3":
        coordinates[4] -= 5
    elif id == "4":
        coordinates[7] -= 5

def moveDown(id): #Or right for winkelkar
    global coordinates
    if id == "1":
        coordinates[1] += 5
    elif id == "2":
        coordinates[3] += 5
    elif id == "3":
        coordinates[4] += 5
    elif id == "4":
        coordinates[7] += 5


#Loop
while(True):
    time.sleep(0.1)
    autoMove()
    checkCollision()
    checkBoundaries()
    client.publish("rpiproject/coord",str(coordinates).strip('[]'))

client.disconnect()

