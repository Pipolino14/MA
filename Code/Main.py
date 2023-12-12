import pygame
import matplotlib.pyplot as mpl
from matplotlib.animation import FuncAnimation
import multiprocessing as mp
from multiprocessing import Pool
#from multiprocessing.pool import ThreadPool
from utils import *
from Animal import *
from Environment import *
from Hunter import *
from Prey import *
from NetworkBuilder import *





#Window dimensions 
WIDTH, HEIGHT = BG_IMG.get_width(), BG_IMG.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Hunters")

#Assets loading
BG_IMG = scale_image(pygame.image.load("Code/Assets/grass.jpg").convert_alpha(), 1)
COLLIDER_IMG = scale_image(pygame.image.load("Code/Assets/collideTEST.PNG").convert_alpha(), 1)
COLLIDER_TEST_MASK = pygame.mask.from_surface(COLLIDER_IMG)

#Frames Per Second Limiter
FPS = 30
VEL = 5

myNetworkBuilder = NetworkBuilder(0, 0)

GameHunter = pygame.sprite.Group()
GamePrey = pygame.sprite.Group()
HunterRepro = pygame.sprite.Group()
#EatingHunters = pygame.sprite.Group()

def animate(Hpop, Ppop, CurrentTime):
    mpl.cla()
    mpl.plot(CurrentTime, Hpop)
    mpl.xlabel('Time')
    mpl.ylabel('Hunter Population')
    mpl.title('Population Graphs')
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

myTicks = []
myHunterPop = []

def check_collide():
    if pygame.sprite.groupcollide(GameHunter, GamePrey, False, False, None):
        spriteGroup = pygame.sprite.groupcollide(GameHunter, GamePrey, False, True, pygame.sprite.collide_mask)
        for hunter in spriteGroup.keys():
            hunter.recharge()
            hunter.fitness = hunter.fitness + 1
            if hunter.fitness >= 2:
                hunter.fitness = 0
                newhunter = hunter.deepcopy()
                HunterRepro.add(newhunter)
                Reprolist = HunterRepro.sprites()
                if len(Reprolist) == 2:
                    N1weights = Reprolist[0].Network.weights
                    N2weights = Reprolist[1].Network.weights
                    N1biases = Reprolist[0].Network.biases
                    N2biases = Reprolist[1].Network.biases
                    N1weights[0], N2weights[0], N1weights[1], N2weights[1] = myNetworkBuilder.crossoverWeights(N1weights[0], N2weights[0], N1weights[1], N2weights[1])
                    N1biases[0], N2biases[0], N1biases[1], N2biases[1] = myNetworkBuilder.crossoverBiases(N1biases[0], N2biases[0], N1biases[1], N2biases[1])
                    for puppy in Reprolist:
                        GameHunter.add(puppy)
                    HunterRepro.empty()
#

        #print("Recharged")
    #print(EatingList[0])
    #Here is where we stopped.
    #We want to recharge the Energy of the Hunter who has eaten a animal.
    #Solution 1: extract Hunter from List and "feed" it



def collided(H, P):
    print(H, P)

run = True
clock = pygame.time.Clock()
images = [(BG_IMG, (0, 0)), (COLLIDER_IMG, (0,0))]
imgRect = pygame.Rect(0,0,WIDTH,HEIGHT)
MyEnvironment = Environment()



walker = HunterAnimal(WIN)



cords = 0

#MyEnvironment.Hanimals, MyEnvironment.Panimals
while run:
    clock.tick(FPS)
    WIN.blit(BG_IMG,(0, 0)) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    keys = pygame.key.get_pressed()
        
    if keys[pygame.K_1]:
        walker.x = 300
        walker.vel = 0
        GameHunter.add(walker)
    if keys[pygame.K_2]:
        GamePrey.add(PreyAnimal(WIN))
    if keys[pygame.K_3]:
        GameHunter.add(HunterAnimal(WIN))
    if keys[pygame.K_4]:
        newprey = GamePrey.sprites()[0]
        preyCopy = newprey.deepcopy()
        GamePrey.add(preyCopy)


        
    if keys[pygame.K_a]:
        walker.rotate(left=True)
    if keys[pygame.K_d]:
        walker.rotate(right=True)
    if keys[pygame.K_w]:
        walker.increase_speed(0.3)
    if keys[pygame.K_s]:
        walker.reduce_speed(0.3)

    
    #off window bounce prototype
    #collision checker for the walker
        
    
    #collision checker for the walker
    #print(pygame.sprite.Group.sprites(GameHunter))
    
    
    #pygame.display.update([imgRect])

    #---------TESTING_WITH_MULTIPROCESSING-------------
    #with Pool(processes=10) as pool:
    #    pool.imap_unordered(GameHunter.update, GameHunter)
    #mp.Process(target=GameHunter.update(), args=GameHunter)
    #mp.Process(target=GamePrey.update(), args=GamePrey)
    #---------------------------------------------------

    GamePrey.update(GameHunter)
    GamePrey.draw(WIN)
    GameHunter.update(GamePrey)
    GameHunter.draw(WIN)
    pygame.display.flip()
    check_collide()


    for prey in GamePrey:
        prey.fitness += 1
        if prey.fitness >= 300:
            prey.fitness = 0
            newprey = prey.deepcopy()
            newprey.Network = myNetworkBuilder.mutateNetwork(prey.Network)
            GamePrey.add(newprey)

    
    #für Testing lasse ich den walker unsterblich sein.
    walker.recharge()


    HuntPop = len(GameHunter.sprites())
    PreyPop = len(GamePrey.sprites())
    myTicks.append(pygame.time.get_ticks())
    myHunterPop.append(HuntPop)
    animate(myHunterPop, PreyPop, myTicks)
    



pygame.quit()
