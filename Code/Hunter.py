from Animal import *
from Globals import *

# Jäger-Tier. Child-class von Animal mit den Jäger-spezifischen
# Eigenschaften und Funktionen
class HunterAnimal(Animal):
    #Initalisiert die Eigenschaften bei der Instanzierung.
    def __init__(self, surface, posX = None,posY = None):
        self.fitness = 0
        self.Energy = Globals.hunter_energy
        self.no_hunt = 0
        #Initialisierung der parent-class
        Animal.__init__(self, "hunter", surface, posX, posY, rays=5,
                        FOV=Globals.HUNTER_FOV, ROV=Globals.HUNTER_ROV)
        
        #Das  Tier sieht niemand im ersten Frame.
        self.distances = [0, 0, 0, 0, 0]

    #Ein Tier kann nicht mit python's "copy" reproduziert werden, da es dort nur 
    #eine neue Referenz kreiert wird. Darum braucht es einen "deepcopy"
    def deepcopy(self):
        newhunter = HunterAnimal(self.surface, self.x, self.y)
        newhunter.Network = self.Network
        newhunter.newgen()
        return newhunter
    
    #Sobald das Tier etwas sieht, beginnt er zu "jagen", heisst: 
    # Die Netzwerk-Outputs haben Einfluss auf sein Verhalten
    def hunt(self):
        if max(self.distances)> 0:
            
            # führt die forward Funktion im Neuralem Netzwerk aus, sobald die Rays etwas sehen.
            netResult = self.Network.forward(self.distances)
            
            #Änderung des Winkels (abhängig vom ersten output vom Netzwerk)
            ResultTurn = netResult[0]**2
            if (netResult[0] < 0):
                self.rotate(turn_right=False, turn_angle=ResultTurn)
            elif (netResult[0] > 0):
                self.rotate(turn_right=True, turn_angle=ResultTurn)

            #Änderung der Geschwindigkeit (abhängig vom zweiten output vom Netzwerk)
            ResultSpeed = netResult[1]**2
            if netResult[1] > 0:
                self.increase_speed(ResultSpeed)
            elif netResult[1] < 0:
                self.reduce_speed(ResultSpeed)

    # Nach erfolgreicher Jagd "tankt" der Jäger Energie.
    def recharge(self):
        self.Energy = Globals.hunter_energy

    # Update Funktion vom Jäger: Aktualisiert die Distanzen-Vektor (input für das neuronale 
    # Netzwerk), checkt ob der Jäger noch leben darf und aktualisiert die "nicht-jagen" Periode.
    def update(self, preyGroup):
        if self.vel <= 3:
            self.vel = 3

        if self.Energy <= 0:
            pygame.sprite.Sprite.kill(self)

        self.distances = Animal.update(self, preyGroup)
        self.hunt()
        if self.no_hunt > 0:
            self.no_hunt -= 1
    