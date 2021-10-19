from copy import copy
from random import randint

class RangeStrategie(object):
    """Strategy Pattern: Auswahlpattern"""

    def __init__(self,x0,x1,name, funcs):
        self.x0 = x0
        self.x1 = x1
        self.name = name
        self.function = funcs
        
    def execute(self, y):
        """Ausführungs Funktion"""
        if self.x0 <= y and y <= self.x1:
            print("--> Execute {} Option {}-{} mit {}".format(self.name,self.x0,self.x1,y))
            self.function()
def pse():
   print("Test")

def none():
    pass

if __name__ == '__main__':
    print("OK")        
    Stra = []
    Stra.append(copy(RangeStrategie(1,9,"Einer",pse)))
    Stra.append(copy(RangeStrategie(10,19,"Zehner",none)))
    Stra.append(copy(RangeStrategie(20,29,"Zwanzig",none)))
    Stra.append(copy(RangeStrategie(30,39,"Dreizig",pse)))
    Stra.append(copy(RangeStrategie(40,49,"Vierzig",none)))

    #Stra[0].execute(3)

    anzahl = 5
    print("--- Self Test with {} Random Numbers".format(anzahl))
    for i in range(anzahl):
        y= randint(0,50)
        print(y)
        for a in Stra:
            a.execute(y)


