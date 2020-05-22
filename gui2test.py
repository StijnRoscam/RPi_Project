#!/usr/bin/python3
import tkinter as tk
from threading import Thread
import time
import os
import paho.mqtt.client as mqtt

#Set start coördinates
wcRol1X, wcRol1Y, wcRol2X, wcRol2Y, wKarX, wKarY, virusX, virusY = 0,100,0,650,750,375,1400,375
canvasWidth, canvasHeight = 1500, 750
startGame = False
score=0

#Global variables
class GameObject:
    XCoord = 0
    YCoord = 0
    ID = 0
    photoPath = 0
    Image = 0
    def __init__(self, XCoord, YCoord, ID):
        self.XCoord = XCoord
        self.YCoord = YCoord
        self.ID = ID

class WcRol(GameObject):
    photoPath = os.path.dirname(os.path.realpath(__file__))+"\wcrolid1.png"
    photoPath2 = os.path.dirname(os.path.realpath(__file__))+"\wcrolid2.png"
    
class WinkelKar(GameObject):
    photoPath = os.path.dirname(os.path.realpath(__file__))+"\winkelkarid3.png"

class Virus(GameObject):
    photoPath = os.path.dirname(os.path.realpath(__file__))+"\\virusid4.png"

#Instantiating different objects
wcRol1 = WcRol(wcRol1X, wcRol1Y, 1)
wcRol2 = WcRol(wcRol2X, wcRol2Y, 2)
winkelKar = WinkelKar(wKarX, wKarY, 3)
virus = Virus(virusX, virusY, 4)
scoreText = 0

def GUI():
    venster = tk.Tk()

    tekst = tk.Label(venster, text = "Corona Game")
    tekst.pack()

    kader = tk.Canvas(venster, width = canvasWidth, height = canvasHeight)
    kader.pack()

    #Instantiate different photo's
    wcrolFoto1 = tk.PhotoImage(file = wcRol1.photoPath)
    wcrolFoto2 = tk.PhotoImage(file = wcRol2.photoPath2)
    winkelkarFoto = tk.PhotoImage(file = winkelKar.photoPath)
    virusFoto = tk.PhotoImage(file = virus.photoPath) #Escape character \\virus.png

    #Draw all images
    def draw():
        global wcRol1, wcRol2, winkelKar, virus, scoreText
        kader.delete(wcRol1.Image)
        kader.delete(wcRol2.Image)
        kader.delete(winkelKar.Image)
        kader.delete(virus.Image)
        kader.delete(scoreText)

        wcRol1.Image = kader.create_image(wcRol1.XCoord, wcRol1.YCoord, anchor=tk.NW, image = wcrolFoto1)
        wcRol2.Image = kader.create_image(wcRol2.XCoord, wcRol2.YCoord, anchor=tk.NW, image = wcrolFoto2)
        winkelKar.Image = kader.create_image(winkelKar.XCoord, winkelKar.YCoord, anchor=tk.NW, image = winkelkarFoto)
        virus.Image = kader.create_image(virus.XCoord, virus.YCoord, anchor=tk.NW, image = virusFoto)
        scoreText = kader.create_text(canvasWidth/2, 10, anchor=tk.NW, text="Score: "+str(score))
        venster.after(10, draw)

    draw()

    venster.mainloop()


def Broker():
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code: "+str(rc))
        #client.subscribe("testtopic/apLab6/raspklas")
    
    def on_message(client, userdata, msg):
        if str(msg.topic) == "rpiproject/score":
            updateScore(str(msg.payload))
        if str(msg.topic) == "rpiproject/coord":
            updateCoords(str(msg.payload))

        #print(msg.payload)
        

    def updateScore(msg):
        print(msg)
        pass

    def updateCoords(msg):
        global wcRol1, wcRol2, winkelKar, virus, score
        coordinates = msg.strip("b' ").replace(" ", "").split(',')
        wcRol1.XCoord=int(coordinates[0])
        wcRol1.YCoord=int(coordinates[1])
        wcRol2.XCoord=int(coordinates[2])
        wcRol2.YCoord=int(coordinates[3])
        winkelKar.XCoord=int(coordinates[4])
        winkelKar.YCoord=int(coordinates[5])
        virus.XCoord=int(coordinates[6])
        virus.YCoord=int(coordinates[7])
        score=int(coordinates[8])
        #print(coordinates[8])
        #print(client)

    client = mqtt.Client(client_id="Gui")
    client.on_connect=on_connect
    client.on_message=on_message
    client.connect("ldlcreations.ddns.net", 1883, 60)
    client.subscribe("rpiproject/coord")
    client.subscribe("rpiproject/score")
    client.loop_start()
    
job1 = Thread(target=GUI)
job2 = Thread(target=Broker)
job1.start()
job2.start()