import random

from Animal import *
from Globals import *

# Beute-Tier. Child-class von Animal mit den Beute-spezifischen
# Eigenschaften und Funktionen
class PreyAnimal(Animal):
    #Initalisiert die Eigenschaften bei der Instanzierung.
    def __init__(self,surface,posX = None,posY = None):
        self.fitness = random.randint(0, 100)
        self.Energy = Globals.prey_energy
        #Initialisierung der parent-class
        Animal.__init__(self, "prey", surface, posX, posY, rays=5,
                        FOV=Globals.PREY_FOV, ROV=Globals.PREY_ROV)

        #Das  Tier sieht niemand im ersten Frame.
        self.distances = [0, 0, 0, 0, 0]

    #Ein Tier kann nicht mit python's "copy" reproduziert werden, da es dort nur 
    #eine neue Referenz kreiert wird. Darum braucht es einen "deepcopy"
    def deepcopy(self):
        newprey = PreyAnimal(self.surface, self.x, self.y)
        newprey.Network = self.Network
        newprey.newgen()
        return newprey

    # Nach einer Pause "tankt" die Beute Energie.
    def recharge(self):
        if self.vel == 0:
            self.Energy += 0.5

    
    # def turningGraph(self, x):
    #     x = (4 * (x - 0.5)**2)**1
    #     return x

    #Sobald das Tier etwas sieht, beginnt er zu "fliehen", heisst: 
    # Die Netzwerk-Outputs haben Einfluss auf sein Verhalten
    def avoid(self):
        if max(self.distances)> 0:
            # macht alle rays sichtbar, falls der hunter etwas sieht
            self.rayGroup.draw(self.surface)
            
            # führt die forward Funktion im Neuralen Netzwerk aus, sobald die Rays etwas sehen.
            netResult = self.Network.forward(self.distances)
            
            #Änderung des Winkels, mit dem Wert des Outputs
            ResultTurn = netResult[0]**2
            if (netResult[0] < 0):
                self.rotate(turn_right=False, turn_angle=ResultTurn)
            elif (netResult[0] > 0):
                self.rotate(turn_right=True, turn_angle=ResultTurn)

            #Änderung der Geschwindigkeit, mit dem Wert des Outputs
            ResultSpeed = netResult[1]**2
            if netResult[1] > 0:
                self.increase_speed(ResultSpeed)
            elif netResult[1] < 0:
                self.reduce_speed(ResultSpeed)

    # Update Funktion vom Beutetier: Aktualisiert die Distanzen-Vektor (input für das neuronale 
    # Netzwerk), und "tankt" Energie falls möglich
    def update(self, hunterGroup):

        self.recharge()

        self.distances = Animal.update(self, hunterGroup)
        self.avoid()