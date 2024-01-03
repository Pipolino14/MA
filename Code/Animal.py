import pygame
import math
import random
from utils import *
from Ray import *
from Network import *
from Globals import *

MatrixLimit = 0

# Animal Basis-Klasse. Enthält alle Eigenschaften und Funktionen 
# die Jäger und Beute gemeinsam haben.
class Animal(pygame.sprite.Sprite):
    def __init__(self, animal, surface, posX, posY, rays, FOV, ROV):
        pygame.sprite.Sprite.__init__(self)
        if animal == "hunter":
            self.image = scale_image(pygame.image.load(
                "Code/Assets/hunter.png"),Globals.animal_size).convert_alpha()
        elif animal == "prey":
            self.image = scale_image(pygame.image.load(
                "Code/Assets/prey.png"), Globals.animal_size).convert_alpha()
        
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.vel = random.randint(0, 3)
        self.angle = random.randint(0, 360)  # Richtung wo das Tier "schaut"

        #Position wird randomisiert, wenn nicht angegeben.
        if posX == None:
            posX = random.randint(0, WIDTH)
        if posY == None:
            posY = random.randint(0, HEIGHT)
        self.x = posX
        self.y = posY

        self.surface = surface
        self.generation = 0

        #Netzwerk-initialisierung
        self.weights = [np.random.uniform(-MatrixLimit, MatrixLimit, size=(5, Globals.hiddenN)),
                        np.random.uniform(-MatrixLimit, MatrixLimit, size=(Globals.hiddenN, 2))]
        self.biases = [np.random.uniform(-MatrixLimit, MatrixLimit, size=(1, Globals.hiddenN)),
                       np.random.uniform(-MatrixLimit, MatrixLimit, size=(1, 2))]
        self.Network = Network(self.weights, self.biases)

        # Die 5 "Rays" sind die "sicht-Strahlen" des Tiers
        self.rayGroup = pygame.sprite.Group()
        for ray in range(rays):
            rayAngle = ray * (FOV / rays) - round(FOV / 2, 0) + ((FOV / rays) / 2)
            ray = Ray(animal, surface, ROV, rayAngle)
            self.rayGroup.add(ray)

    # Generationen-counter
    def newgen(self):
        self.generation += 1

    # Tier-rotation. Wird vom ersten Output des Netzwerks getriggert
    def rotate(self, turn_right, turn_angle):
        if turn_right:
            self.angle += Globals.angle_factor * turn_angle
        else:
            self.angle -= Globals.angle_factor * turn_angle

    # Tier-Bewegung. Aktualisiert die Tierkoordinaten bei jedem update
    def move(self):
        #Konvertieren des aktuellen Blickwinkels in RAD
        radians = math.radians(self.angle)
        #cos(RichtungsWinkel) * Hypothenuse{velocity vector} = Gegenkatethe --> Y movement
        vertical = math.cos(radians) * self.vel
        #sin(RichtungsWinkel) * Hypothenuse{velocity vector} = Ankatethe --> X movement
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

        #berechnet die verbrauchte Energie bei der immomentigen Geschwindigkeit
        self.Energy = self.Energy - self.vel

    def increase_speed(self, inc):
        self.vel = min(self.vel + inc, 5)

    def reduce_speed(self, red):
        self.vel = max(self.vel - red, 0)

    # Bewirkt dass das Tier bei den Ränder zurückprallt.
    def check_border(self):
        HEI = (self.image.get_height()/2)
        WID = (self.image.get_width()/2)
        #bottom
        if self.y > HEIGHT - HEI:
            self.angle = (360 - self.angle) + 180
            self.y = HEIGHT - HEI - 1
        #top
        if self.y < HEI:
            self.angle = (360 - self.angle) + 180
            self.y = HEI + 1
        #right
        if self.x > WIDTH - WID:
            self.angle = (360 - self.angle) 
            self.x = WIDTH - WID - 1
        #left
        if self.x < WID:
            self.angle = (360 - self.angle) 
            self.x = WID + 1

    # Rote anzeige wo das Tier gerade "schaut"
    def visionray(self):
        faceangle =- math.radians(self.angle)
        pygame.draw.line(self.surface, (255, 0, 0), (self.x, self.y), (self.x + math.sin(faceangle) * Globals.vision_ray, self.y - math.cos(faceangle) * Globals.vision_ray), 2)

    # Update funktion,wird bei jedem frame aufgerufen und liefert ein array von 
    # Distanzen wo das Tier andere Tiere sieht
    def update(self, target_group):
        if self.vel < 0:
            self.vel = 0
        self.move()
        self.check_border()

        self.rect.center=(self.x, self.y)

        self.rayGroup.update((self.x, self.y), self.angle, target_group)
        distances = []
        for ray in self.rayGroup.sprites():
            distances.append(ray.distance)
        self.visionray()
        return distances
    