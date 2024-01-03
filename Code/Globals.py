import pygame
from utils import *

pygame.init()
pygame.display.init()
BG_IMG = scale_image(pygame.image.load("Code/Assets/grass.jpg"), 1)
#WIDTH, HEIGHT = BG_IMG.get_width(), BG_IMG.get_height()
WIDTH, HEIGHT = 1400, 1400
SCRN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HIDDEN)
WIN = pygame.surface.Surface((WIDTH, HEIGHT))
BG_IMG.convert_alpha()

pygame.display.set_caption("Calculating of the fittest")

# Globale Eigenschaften die überall im Programm benutzt werden. 
# Können manuell oder von der GUI überschrieben werden.
class Globals:
    #Frames Per Second Limiter
    FPS = 30
    VEL = 5

    #Range of View
    HUNTER_ROV = 300
    PREY_ROV = 200
    #Field of View
    HUNTER_FOV = 45
    PREY_FOV = 270

    #-----------------------------------------------Amount-Preys-Hunters-----------------------------------------------
    numHunters = 40
    numPreys = 250
    #------------------------------------------------------------------------------------------------------------------
    #Maximaler Winkel, in welchem sie die Tiere in einem Frame drehen können.
    angle_factor = 10
    #Anzahl Neuronen in der Hidden Layer.
    hiddenN = 2
    #Mutations Wahrscheinlichkeit 
    MutProbability = 0.2
    #Mutationsstärke
    MutStrength = 0.1
    #Energie von den hunters und preys nach start oder nach hunters recharge
    hunter_energy = 900
    prey_energy = 400
    #Wie lang die hunters nach einer Jagd nicht jagen dürfen, in Frames
    no_hunt_period = 10
    #Wie oft sich die preys reproduzieren, in Frames
    prey_reproduction = 360
    #Wie viele Kills müssen die Hunters haben um sich zu reproduzieren
    hunter_repro_fitness = 3
    # Range in denen die preys nahe ihre Eltern spawnen
    min_repro_range = 5
    max_repro_range = 15
    #Grösse der Tiere. Je kleiner, desto mehr "Platz" haben sie...
    animal_size = 0.3
    #Wie oft die graph updated wird in Anzahl frames:
    graph_rate = 10
    #Zeigt die Vision rays der Tiere an
    show_ray = False
    #Zeigt an, welche Tiere jedes Tier gerade sieht
    show_target = True
    #Setzt fest, ob die Daten nach einer Simulation gespeichert werden sollen oder nicht
    store_data = True
    #Länge der "Vision ray" (Zeigt die Richtung wo das Tier "schaut")
    vision_ray = 20

