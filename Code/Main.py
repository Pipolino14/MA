import pygame
import pygame.freetype as ft
import matplotlib.pyplot as mpl
import pandas as pd
import datetime
import json
import sys
from Rotator import *

from matplotlib.animation import FuncAnimation

from utils import *
#from Animal import *
from Hunter import *
from Prey import *
from NetworkBuilder import *
from Globals import *

def spawn_animals(GameHunter, GamePrey):
    Rotator.create_rays(WIN, Globals.HUNTER_ROV, Globals.PREY_ROV)
    for counter in range(Globals.numHunters):
        GameHunter.add(HunterAnimal(WIN))

    for counter in range(Globals.numPreys):
        GamePrey.add(PreyAnimal(WIN))

def check_collide(HungryGameHunter, GamePrey, hunterRepro):
    if pygame.sprite.groupcollide(HungryGameHunter, GamePrey, False, False, None):
        spriteGroup = pygame.sprite.groupcollide(HungryGameHunter, GamePrey, False, True, pygame.sprite.collide_mask)
        for hunter in spriteGroup.keys():
            hunter.recharge()
            hunter.fitness = hunter.fitness + 1
            hunter.no_hunt = Globals.no_hunt_period
            HungryGameHunter.remove(hunter)
            if hunter.fitness >= Globals.hunter_repro_fitness:
                hunter.fitness = 0
                newhunter = hunter.deepcopy()
                hunterRepro.add(newhunter)

def check_repro(hunterRepro, preyRepro, GameHunter, GamePrey):
    myNetworkBuilder = NetworkBuilder(0, 0)
    Hlist = hunterRepro.sprites()
    Plist = preyRepro.sprites()
    while len(Hlist) >= 2:
        N1weights = Hlist[0].Network.weights
        N2weights = Hlist[1].Network.weights
        N1biases = Hlist[0].Network.biases
        N2biases = Hlist[1].Network.biases
        N1weights[0], N2weights[0], N1weights[1], N2weights[1] = myNetworkBuilder.crossoverWeights(N1weights[0], N2weights[0], N1weights[1], N2weights[1])
        N1biases[0], N2biases[0], N1biases[1], N2biases[1] = myNetworkBuilder.crossoverBiases(N1biases[0], N2biases[0], N1biases[1], N2biases[1])
        Hlist[0].Network.weights = N1weights
        Hlist[0].Network.biases = N1biases
        Hlist[1].Network.weights = N2weights
        Hlist[1].Network.biases = N2biases
        Hlist[0].Network = myNetworkBuilder.mutateNetwork_3(Hlist[0].Network)
        Hlist[1].Network = myNetworkBuilder.mutateNetwork_3(Hlist[1].Network)
        GameHunter.add(Hlist[0])
        GameHunter.add(Hlist[1])
        Hlist.pop(0)
        Hlist.pop(0)

    while len(Plist) >= 2:
        N1weights = Plist[0].Network.weights
        N2weights = Plist[1].Network.weights
        N1biases = Plist[0].Network.biases
        N2biases = Plist[1].Network.biases
        N1weights[0], N2weights[0], N1weights[1], N2weights[1] = myNetworkBuilder.crossoverWeights(N1weights[0], N2weights[0], N1weights[1], N2weights[1])
        N1biases[0], N2biases[0], N1biases[1], N2biases[1] = myNetworkBuilder.crossoverBiases(N1biases[0], N2biases[0], N1biases[1], N2biases[1])
        Plist[0].Network.weights = N1weights
        Plist[0].Network.biases = N1biases
        Plist[1].Network.weights = N2weights
        Plist[1].Network.biases = N2biases
        Plist[0].Network = myNetworkBuilder.mutateNetwork_3(Plist[0].Network)
        Plist[1].Network = myNetworkBuilder.mutateNetwork_3(Plist[1].Network)
        GamePrey.add(Plist[0])
        GamePrey.add(Plist[1])
        Plist.pop(0)
        Plist.pop(0)

#Graph Funktion:
def animate(Hpop, Ppop, Gpop, CurrentTime):
    mpl.cla()
    mpl.plot(CurrentTime, Hpop, CurrentTime, Ppop, CurrentTime, Gpop)
    mpl.legend(["Hunters","Preys","Tiere"])
    mpl.xlabel('Zeit in Sekunden')
    mpl.ylabel('Anzahl Tiere')
    mpl.title('Populationsgrössen')
    mpl.ion()
    mpl.show()
    mpl.pause(0.001)


#Info-Funktionen: Schreiben FPS und infos auf der Screen für debuggen

def draw_fps(clock):
    font = ft.SysFont('Verdana', 20)
    fps = f'{clock.get_fps() :.2f}FPS'
    font.render_to(WIN, (0, 0), text=fps, fgcolor='red', bgcolor='black')

def draw_info(text):
    font = ft.SysFont('Verdana', 20)
    font.render_to(WIN, (0, 100), text=text, fgcolor='green', bgcolor='black')

#Data-Speicherfunktion. Speichert alle relevante Daten einer Simulation
def storeData(plot_ticks, plot_hunter, plot_prey):
    if Globals.store_data:
        excelData = {"Zeit":plot_ticks, "Anz. Jäger": plot_hunter, "Anz. Beute": plot_prey}
        configData = {"numHunters":Globals.numHunters, 
                      "numPreys": Globals.numPreys,
                      "hunter_energy":Globals.hunter_energy,
                      "prey_energy":Globals.prey_energy,
                      "Hunter FOV":Globals.HUNTER_FOV,
                      "Prey FOV":Globals.PREY_FOV,
                      "Hunter ROV":Globals.HUNTER_ROV,
                      "Prey ROV":Globals.PREY_ROV,
                      "Hunter repro":Globals.hunter_repro_fitness,
                      "Prey repro":Globals.prey_reproduction,
                      "Hunter Saturation":Globals.no_hunt_period,
                      "Min Prey repro dis":Globals.min_repro_range,
                      "Max Prey repro dis":Globals.max_repro_range,
                      "Angle_factor":Globals.angle_factor,
                      "Animal Size":Globals.animal_size
                      }

        dc = pd.DataFrame(configData, index=[0])
        df = pd.DataFrame(excelData)
        now_time = datetime.datetime.now()
        filename =f"simdata/hunters-preys-{now_time.strftime('%Y%m%d-%H-%M-%S')}.xlsx"
        configname = f"simdata/config-{now_time.strftime('%Y%m%d-%H-%M-%S')}.txt"
        plotname =f"simdata/hunters-preys-{now_time.strftime('%Y%m%d-%H-%M-%S')}.png"
        df.to_excel(filename, index=False)
        mpl.savefig(plotname)
        json_object = json.dumps(configData, indent=4)
        with open(configname, "w") as outfile:
            outfile.write(json_object)


#-----------------------------------------------GAMELOOP-----------------------------------------------
def runSimulation():
    # Initialisierung
    #pygame.init()
    run = True
    clock = pygame.time.Clock()
    #imgRect = pygame.Rect(0,0,WIDTH,HEIGHT)

    #debug for globals
    # print(Globals.numHunters)
    # print(Globals.numPreys)
    # print(Globals.animal_size)

    print(pygame.display.Info())
    print(pygame.display.get_driver())

    framecount = 0
    
    GameHunter = pygame.sprite.Group()
    GamePrey = pygame.sprite.Group()
    HungryGameHunter = pygame.sprite.Group()
    hunterRepro = pygame.sprite.Group()
    preyRepro = pygame.sprite.Group()
    plot_ticks = []
    plot_hunter = []
    plot_prey = []
    plot_general = []
    
    spawn_animals(GameHunter, GamePrey)
    walker = HunterAnimal(WIN)
    walker.Network.empty_Network()
    
    while run:
        clock.tick(Globals.FPS)
        #WIN.blit(BG_IMG,(0, 0))
        WIN.fill((0, 0, 0))
        draw_fps(clock)

        GamePrey.update(GameHunter)
        GamePrey.draw(WIN)
        GameHunter.update(GamePrey)
        GameHunter.draw(WIN)

        for hungry in GameHunter:
            if hungry.no_hunt == 0:
                HungryGameHunter.add(hungry)

        check_collide(HungryGameHunter, GamePrey, hunterRepro)

        for prey in GamePrey:
            prey.fitness += 1
            if prey.fitness >= Globals.prey_reproduction:
                prey.fitness = 0
                newprey = prey.deepcopy()
                #Position sollte um der Vatertier sein aber möglichst nicht die gleiche
                range_x = random.randint(Globals.min_repro_range, Globals.max_repro_range)
                range_y = random.randint(Globals.min_repro_range, Globals.max_repro_range)
                shift_x = random.randint(-1, 1)
                if shift_x == 0: shift_x = -1
                shift_y = random.randint(-1, 1)
                if shift_y == 0: shift_y = -1
                newprey.x += shift_x * range_x
                newprey.y += shift_y * range_y
                # Verhindern dass sie aus der Spielfläche gespawnt werden:
                newprey.x = min(newprey.x, WIDTH)
                newprey.x = max(newprey.x, 0)
                newprey.y = min(newprey.y, HEIGHT)
                newprey.y = max(newprey.y, 0)
                preyRepro.add(newprey)

        check_repro(hunterRepro, preyRepro, GameHunter, GamePrey)

        hunter_pop = len(GameHunter.sprites())
        prey_pop = len(GamePrey.sprites())
        general_pop = hunter_pop + prey_pop
        plot_ticks.append(pygame.time.get_ticks() / 1000)
        plot_hunter.append(hunter_pop)
        plot_prey.append(prey_pop)
        plot_general.append(general_pop)

        framecount += 1
        if ((framecount % Globals.graph_rate) == 0):
            framecount = 0
            animate(plot_hunter, plot_prey, plot_general, plot_ticks)
        
        if ((hunter_pop == 0) or (prey_pop == 0)):
            storeData(plot_ticks, plot_hunter, plot_prey)
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
        
        SCRN.blit(WIN, (0, 0))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                storeData(plot_ticks, plot_hunter, plot_prey)
                run = False
                break
    pygame.quit()
    sys.exit()

if __name__== "__main__":
    runSimulation()