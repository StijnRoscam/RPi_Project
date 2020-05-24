#!/usr/bin/python3
import tkinter as tk
from threading import Thread
import time
import os
import paho.mqtt.client as mqtt

#Set start coördinates
wcRol1X, wcRol1Y, wcRol2X, wcRol2Y, wKarX, wKarY, virusX, virusY = 0,100,0,550,750,375,1300,375
canvasWidth, canvasHeight = 1500, 750
endGame = False
score=0

#Global variables
class GameObject:
    XCoord = 0
    YCoord = 0
    photoPath = 0
    Image = 0
    def __init__(self, XCoord, YCoord, ID):
        self.XCoord = XCoord
        self.YCoord = YCoord

class WcRol(GameObject):
    photoPath = os.path.dirname(os.path.realpath(__file__))+"\wcrol1.png"
    photoPath2 = os.path.dirname(os.path.realpath(__file__))+"\wcrol2.png"
    
class WinkelKar(GameObject):
    photoPath = os.path.dirname(os.path.realpath(__file__))+"\winkelkar3.png"

class Virus(GameObject):
    photoPath = os.path.dirname(os.path.realpath(__file__))+"\\virus4.png"

#Instantiating different objects
wcRol1 = WcRol(wcRol1X, wcRol1Y)
wcRol2 = WcRol(wcRol2X, wcRol2Y)
winkelKar = WinkelKar(wKarX, wKarY)
virus = Virus(virusX, virusY)
scoreText = 0

backgroundImageSource = file=os.path.dirname(os.path.realpath(__file__))+"\\background.png"

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
    backgroundImage = tk.PhotoImage(file = backgroundImageSource)
    background = kader.create_image(0,0,anchor=tk.NW, image=backgroundImage)

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
        scoreText = kader.create_text(canvasWidth*3/4, 10, anchor=tk.NW, text="Score: "+str(score),font="Arial 30 bold")
        if not endGame:
            venster.after(10, draw)

        else:
            time.sleep(1)
            GameOver = kader.create_text(canvasWidth/2, canvasHeight/2, anchor=tk.NW, text="Game over, max score reached.", font="Arial 40 bold")
            print("Gameover")

    draw()

    venster.mainloop()


def Broker():
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code: "+str(rc))
        #client.subscribe("testtopic/apLab6/raspklas")
    
    def on_message(client, userdata, msg):
        if str(msg.topic) == "rpiproject/coord":
            updateCoords(str(msg.payload))

        if str(msg.topic) == "rpiproject/gameover":
            global endGame
            endGame = True
            print("Gameover received")
            client.disconnect()

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