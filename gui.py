import tkinter as tk
from threading import Thread
import time
import os

#Set start coördinates
wcRol1X, wcRol1Y, wcRol2X, wcRol2Y, wKarX, wKarY, virusX, virusY = 0,100,0,650,750,375,1400,375
canvasWidth, canvasHeight = 1500, 750

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

    moveObjects()

    venster.mainloop()

    
job1 = Thread(target=GUI)
job1.start()
#job2.start()
