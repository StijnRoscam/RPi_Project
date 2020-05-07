import tkinter as tk
from threading import Thread
import time
import os
import paho.mqtt.client as mqtt

#Set start coördinates
wcRol1X, wcRol1Y, wcRol2X, wcRol2Y, wKarX, wKarY, virusX, virusY = 0,100,0,650,750,375,1400,375
canvasWidth, canvasHeight = 1500, 750

wcRol1MoveUp, wcRol2MoveUp, winkelKarMoveUp, virusMoveUp = False
wcRol1MoveDown, wcRol2MoveDown, winkelKarMoveDown, virusMoveDown = False
wcRol1Reset, wcRol2Reset, winkelKarReset, virusReset = False

startGame = False

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
    photoPath = os.path.dirname(os.path.realpath(__file__))+"\wcrol.png"
    Speed = 5
    
class WinkelKar(GameObject):
    photoPath = os.path.dirname(os.path.realpath(__file__))+"\winkelkar.png"
    Score = 0

class Virus(GameObject):
    photoPath = os.path.dirname(os.path.realpath(__file__))+"\\virus.png"
    Speed = -5

#Instantiating different objects
wcRol1 = WcRol(wcRol1X, wcRol1Y, 1)
wcRol2 = WcRol(wcRol2X, wcRol2Y, 2)
winkelKar = WinkelKar(wKarX, wKarY, 3)
virus = Virus(virusX, virusY, 4)

#Startvenster waarin iedereen ziet wat voor gameobject hij/zij is
#Enkele seconden nadat iedereen is verbonden start het spel
#if p1Ready, p2Ready, p3Ready, p4Ready
#   time.sleep(5)
#   start spel


def GUI():
    venster = tk.Tk()

    tekst = tk.Label(venster, text = "Corona Game")
    tekst.pack()

    kader = tk.Canvas(venster, width = canvasWidth, height = canvasHeight)
    kader.pack()

    #Instantiate different photo's
    wcrolFoto = tk.PhotoImage(file = wcRol1.photoPath)
    winkelkarFoto = tk.PhotoImage(file = winkelKar.photoPath)
    virusFoto = tk.PhotoImage(file = virus.photoPath) #Escape character \\virus.png

    #Draw all images
    wcRol1.Image = kader.create_image(wcRol1.XCoord, wcRol1.YCoord, anchor=tk.NW, image = wcrolFoto)
    wcRol2.Image = kader.create_image(wcRol2.XCoord, wcRol2.YCoord, anchor=tk.NW, image = wcrolFoto)
    virus.Image = kader.create_image(virus.XCoord, virus.YCoord, anchor=tk.NW, image = virusFoto)
    winkelKar.Image = kader.create_image(winkelKar.XCoord, winkelKar.YCoord, anchor=tk.NW, image = winkelkarFoto)
    

    #Draw 1 specific image
    def drawImage(width, height, foto):
        image = kader.create_image(width, height, anchor=tk.NW, image = foto)

    #Reset in the middle of the screen atm.
    def resetOnEnd():
        global wcRol1, wcRol2, virus
       
        if wcRol1.XCoord > canvasWidth/2:
            wcRol1.XCoord = 0
            kader.delete(wcRol1.Image)
            wcRol1.Image = kader.create_image(wcRol1.XCoord, wcRol1.YCoord, anchor=tk.NW, image = wcrolFoto)
            
        if wcRol2.XCoord > canvasWidth/2:
            wcRol2.XCoord = 0
            kader.delete(wcRol2.Image)
            wcRol2.Image = kader.create_image(wcRol2.XCoord, wcRol2.YCoord, anchor=tk.NW, image = wcrolFoto)

        if virus.XCoord < canvasWidth/2:
            virus.XCoord = canvasWidth
            kader.delete(virus.Image)
            virus.Image = kader.create_image(virus.XCoord, virus.YCoord, anchor=tk.NW, image = virusFoto)

    #Under development
    def resetWcRol(wcRol, wcRolX, wcRolY, canvas):
        wcRolX = 0
        canvas.delete(wcRol)
       # wcRol = canvas.create_image(wcRolX, wcRolY, anchor=tk.NW, image = wcrolFoto)

    #Method that moves the objects automatically in correct direction
    def moveObjects():
        global wcRol1, wcRol2
        kader.move(wcRol1.Image,wcRol1.Speed,1)
        wcRol1.XCoord += wcRol1.Speed

        kader.move(wcRol2.Image,wcRol2.Speed,-1)
        wcRol2.XCoord += wcRol1.Speed

        kader.move(virus.Image,virus.Speed,0)
        virus.XCoord += virus.Speed

        resetOnEnd()

        venster.after(50,moveObjects) #Every 100 ms, wcrol move 5 to the right, virus 5 to left

    def moveObjectsCoord():
        global wcRol1, wcRol2, winkelKar, virus
        kader.delete(wcRol1.Image)
        kader.delete(wcRol2.Image)
        kader.delete(winkelKar.Image)
        kader.delete(virus.Image)

        wcRol1.Image = kader.create_image(wcRol1.XCoord, wcRol1.YCoord, anchor=tk.NW, image = wcrolFoto)
        wcRol2.Image = kader.create_image(wcRol2.XCoord, wcRol2.YCoord, anchor=tk.NW, image = wcrolFoto)
        winkelKar.Image = kader.create_image(winkelKar.XCoord, winkelKar.YCoord, anchor=tk.NW, image = winkelkarFoto)
        virus.Image = kader.create_image(virus.XCoord, virus.YCoord, anchor=tk.NW, image = virusFoto)

        venster.after(50, moveObjectsCoord)


    moveObjects()

    venster.mainloop()


def Broker():
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code: "+str(rc))
        #client.subscribe("testtopic/apLab6/raspklas")
    
    def on_message(client, userdata, msg):
        print("Message : "+str(msg.payload))
        if str(msg.payload)[7:14] == "MOVE=UP":
            moveUp(str(msg.payload)[5:6])

        elif str(msg.payload)[7:14] == "MOVE=DN":
            moveDown(str(msg.payload)[5:6])

        elif str(msg.payload)[7:14] == "ACTI=RE":
            resetObject(str(msg.payload)[5:6])

        elif str(msg.payload)[1:6] == "START":
            global startGame
            startGame = True

    def moveUp(id):
        global wcRol1MoveUp, wcRol2MoveUp, winkelKarMoveUp, virusMoveUp
        if id == "1":
            wcRol1MoveUp = True
        elif id == "2":
            wcRol2MoveUp = True
        elif id == "3":
            winkelKarMoveLeft = True
        elif id == "4":
            virusMoveUp = True

    def moveDown(id):
        global wcRol1MoveDown, wcRol2MoveDown, winkelKarMoveDown, virusMoveDown
        if id == "1":
            wcRol1MoveDown = True
        elif id == "2":
            wcRol2MoveDown = True
        elif id == "3":
            winkelKarMoveRight = True
        elif id == "4":
            virusMoveDown = True

    def resetObject(id): #Niet nodig als alles in gamecontroller word geregeld
        global wcRol1Reset, wcRol2Reset, winkelKarReset, virusReset
        if id == "1":
            wcRol1Reset = True
        elif id == "2":
            wcRol2Reset = True
        elif id == "3":
            winkelKarReset = True
        elif id == "4":
            virusMoveReset = True



    client = mqtt.Client("Gui")
    client.on_connect=on_connect
    client.on_message=on_message
    client.connect("ldlcreations.ddns.net", 1883, 60)
    client.subscribe("rpiproject/coord")
    client.loop_start()
    
job1 = Thread(target=GUI)
job2 = Thread(target=Broker)
job1.start()
job2.start()
  

