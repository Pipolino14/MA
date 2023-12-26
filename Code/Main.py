import pygame
import pygame.freetype as ft
import matplotlib.pyplot as mpl
import pandas as pd
import datetime

from matplotlib.animation import FuncAnimation

from utils import *
from Animal import *
from Hunter import *
from Prey import *
from NetworkBuilder import *


#Frames Per Second Limiter
FPS = 30
VEL = 5

myNetworkBuilder = NetworkBuilder(0, 0)

GameHunter = pygame.sprite.Group()
GamePrey = pygame.sprite.Group()
hunterRepro = pygame.sprite.Group()
preyRepro = pygame.sprite.Group()
#EatingHunters = pygame.sprite.Group()

def animate(Hpop, Ppop, CurrentTime):
    mpl.cla()
    mpl.plot(CurrentTime, Hpop, CurrentTime, Ppop)
    mpl.legend(["Hunters","Preys"])
    mpl.xlabel('Zeit in Sekunden')
    mpl.ylabel('Anzahl Tiere')
    mpl.title('Populationsgrösse')
    mpl.ion()
    mpl.show()
    mpl.pause(0.001)

def Draw(win, images):
    for img, pos in images:
        win.blit(img, pos)
    
#    Hanimals = HunterAnimalsDictionary.values()
#    Panimals = PreyAnimalsDictionary.values()
    
#    for hunter in Hanimals:
#        hunter.draw(win)
#    for prey in Panimals:
#        prey.draw(win)
    pygame.display.update()

plot_ticks = []
plot_hunter = []
plot_prey = []

def check_collide():
    if pygame.sprite.groupcollide(GameHunter, GamePrey, False, False, None):
        spriteGroup = pygame.sprite.groupcollide(GameHunter, GamePrey, False, True, pygame.sprite.collide_mask)
        for hunter in spriteGroup.keys():
            hunter.recharge()
            hunter.fitness = hunter.fitness + 1
            if hunter.fitness >= 2:
                hunter.fitness = 0
                newhunter = hunter.deepcopy()
                hunterRepro.add(newhunter)

def check_repro():
    Hlist = hunterRepro.sprites()
    Plist = preyRepro.sprites()
    if len(Hlist) >= 2:
        N1weights = Hlist[0].Network.weights
        N2weights = Hlist[1].Network.weights
        N1biases = Hlist[0].Network.biases
        N2biases = Hlist[1].Network.biases
        N1weights[0], N2weights[0], N1weights[1], N2weights[1] = myNetworkBuilder.crossoverWeights(N1weights[0], N2weights[0], N1weights[1], N2weights[1])
        N1biases[0], N2biases[0], N1biases[1], N2biases[1] = myNetworkBuilder.crossoverBiases(N1biases[0], N2biases[0], N1biases[1], N2biases[1])
        for crossHunter in Hlist:
            crossHunter.Network = myNetworkBuilder.mutateNetwork_3(crossHunter.Network)
            GameHunter.add(crossHunter)
        hunterRepro.remove(Hlist)

    if len(Plist) >= 2:
        N1weights = Plist[0].Network.weights
        N2weights = Plist[1].Network.weights
        N1biases = Plist[0].Network.biases
        N2biases = Plist[1].Network.biases
        N1weights[0], N2weights[0], N1weights[1], N2weights[1] = myNetworkBuilder.crossoverWeights(N1weights[0], N2weights[0], N1weights[1], N2weights[1])
        N1biases[0], N2biases[0], N1biases[1], N2biases[1] = myNetworkBuilder.crossoverBiases(N1biases[0], N2biases[0], N1biases[1], N2biases[1])
        for crossPrey in Plist:
            crossPrey.Network = myNetworkBuilder.mutateNetwork_3(crossPrey.Network)
            GamePrey.add(crossPrey)
            print("newprey", len(GamePrey.sprites()))
        preyRepro.remove(Plist[0], Plist[1])

def collided(H, P):
    print(H, P)

run = True
clock = pygame.time.Clock()
#images = [(BG_IMG, (0, 0)), (COLLIDER_IMG, (0,0))]
imgRect = pygame.Rect(0,0,WIDTH,HEIGHT)

#-----------------------------------------------Amount-Preys-Hunters-----------------------------------------------
cords = 0
numHunters = 100
numPreys = 200
#------------------------------------------------------------------------------------------------------------------

for counter in range(numHunters):
    GameHunter.add(HunterAnimal(WIN))

for counter in range(numPreys):
    GamePrey.add(PreyAnimal(WIN))

pygame.init()


font = ft.SysFont('Verdana', 20)

def draw_fps():
    fps = f'{clock.get_fps() :.2f}FPS'
    font.render_to(WIN, (0, 0), text=fps, fgcolor='red', bgcolor='black')

def draw_info(text):
    font.render_to(WIN, (0, 100), text=text, fgcolor='green', bgcolor='black')

def storeData():
    excelData = {"Zeit":plot_ticks, "Anz. Jäger": plot_hunter, "Anz. Beute": plot_prey}

    df = pd.DataFrame(excelData)
    now_time = datetime.datetime.now()
    filename =f"simdata/hunters-preys-{now_time.strftime('%Y%m%d-%H-%M-%S')}.xlsx"
    plotname =f"simdata/hunters-preys-{now_time.strftime('%Y%m%d-%H-%M-%S')}.png"
    df.to_excel(filename, index=False)
    mpl.savefig(plotname)

walker = HunterAnimal(WIN)
walker.Network.empty_Network()

framecount = 0

#-----------------------------------------------GAMELOOP-----------------------------------------------

while run:
    pygame.display.update()
    clock.tick(FPS)
    WIN.blit(BG_IMG,(0, 0)) 
    draw_fps()
    
    GamePrey.update(GameHunter)
    GamePrey.draw(WIN)
    GameHunter.update(GamePrey)
    GameHunter.draw(WIN)

    check_collide()

    for prey in GamePrey:
        prey.fitness += 1
        if prey.fitness >= 155:
            prey.fitness = 0
            newprey = prey.deepcopy()
            preyRepro.add(newprey)

    
    check_repro()

    hunter_pop = len(GameHunter.sprites())
    prey_pop = len(GamePrey.sprites())
    plot_ticks.append(pygame.time.get_ticks() / 1000)
    plot_hunter.append(hunter_pop)
    plot_prey.append(prey_pop)

    framecount += 1
    if ((framecount % 30) == 0):
        framecount = 0
        animate(plot_hunter, plot_prey, plot_ticks)
    
    if ((hunter_pop == 0) or (prey_pop == 0)):
        storeData()
        run = False

    
    #---------------WALKER---------------
    walker.recharge()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        walker.x = 300
        walker.vel = 0
        GameHunter.add(walker)
    
    if keys[pygame.K_a]:
        walker.rotate(turn_right=False, turn_angle=0.5)
    if keys[pygame.K_d]:
        walker.rotate(turn_right=True, turn_angle=0.5)
    if keys[pygame.K_w]:
        walker.increase_speed(0.3)
    if keys[pygame.K_s]:
        walker.reduce_speed(0.3)
    #------------------------------------

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            storeData()
            run = False
            break

pygame.quit()
