# RPi_Project

broker: ID+actie+waarde

bv: 
"ID=1,MOVE=UP"  //Move up
"ID=1,MOVE=DN"  //Move down
"ID=1,CNCT=TR"  //is connected
"START"

"ID=1,ACTI=RE"  //reset image on collision, reset score on collision, reset ....

Classes in gui.py
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
