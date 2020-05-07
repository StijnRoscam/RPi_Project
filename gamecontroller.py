from threading import Thread
import time
import paho.mqtt.client as mqtt

coordinates = [0,100,0,650,750,375,1400,375] #wcRol1X, wcRol1Y, wcRol2X, wcRol2Y, wKarX, wKarY, virusX, virusY
canvasWidth, canvasHeight = 1500, 750
startGame = False
clientID = 1

def Broker():
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code: "+str(rc))
        #client.subscribe("testtopic/apLab6/raspklas")

    def on_message(client, userdata, msg):
        print("Message : "+str(msg.payload))

        #Wanneer een rpi een bericht stuurt met als msg CNCT, voer initialConnection uit
        if str(msg.payload)[1:5] == "CNCT":
            initialConnection(client)
    

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

