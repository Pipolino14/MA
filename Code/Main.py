import pygame
import pygame.freetype as ft
import matplotlib.pyplot as mpl
import pandas as pd
import datetime
import json
import time

from Hunter import *
from Prey import *
from NetworkBuilder import *
from Globals import *

# Das ist das Hauptmodul und ist deswegen nicht in einer Klasse verpackt. 
# Es enthält der Loop der die ganze Simulation ausführt.

# Generiert die erste Tiere und deren "seh-rays" mit Hilfe von der Rotator-Klasse.
def spawn_animals(GameHunter, GamePrey):
    Rotator.create_rays(WIN, Globals.HUNTER_ROV, Globals.PREY_ROV)
    for counter in range(Globals.numHunters):
        GameHunter.add(HunterAnimal(WIN))

    for counter in range(Globals.numPreys):
        GamePrey.add(PreyAnimal(WIN))

# Checkt ob die Gruppe von "hungrige Jäger" mit Beute kollidiert sind, heisst: gejagt haben
def check_collide(HungryGameHunter, GamePrey, hunterRepro):
    #Doppelter check mit und ohne Mask ist nötig, um die Performance zu erhöhen
    if pygame.sprite.groupcollide(HungryGameHunter, GamePrey, False, False, None):
        spriteGroup = pygame.sprite.groupcollide(HungryGameHunter, GamePrey,
                                                 False, True, pygame.sprite.collide_mask)
        for hunter in spriteGroup.keys():
            hunter.recharge()
            hunter.fitness = hunter.fitness + 1
            hunter.no_hunt = Globals.no_hunt_period
            HungryGameHunter.remove(hunter) #Hunter hat gejagt: ist also nicht mehr "hungrig"

            #Darf sich der Jäger reproduzieren?
            if hunter.fitness >= Globals.hunter_repro_fitness:
                hunter.fitness = 0
                newhunter = hunter.deepcopy()
                #Jäger wird dupliziert und in einen "reproduktion-Pool" reingeworfen
                hunterRepro.add(newhunter)

# Checkt ob der "reproduktion-Pool" von Jäger und Beute genug Elemente hat (mind. 2) 
# und löst eine Rekombination aus
def check_repro(hunterRepro, preyRepro, GameHunter, GamePrey):
    myNetworkBuilder = NetworkBuilder(0, 0)
    Hlist = hunterRepro.sprites()
    Plist = preyRepro.sprites()
    while len(Hlist) >= 2:
        #Die ersten zwei Jäger von der Liste werden selektiert...
        N1weights = Hlist[0].Network.weights
        N2weights = Hlist[1].Network.weights
        N1biases = Hlist[0].Network.biases
        N2biases = Hlist[1].Network.biases
        #Die Werte gehen durch einen Crossover-Prozess...
        N1weights, N2weights = myNetworkBuilder.crossoverWeights(N1weights, N2weights)
        N1biases, N2biases = myNetworkBuilder.crossoverBiases(N1biases, N2biases)
        Hlist[0].Network.weights = N1weights
        Hlist[0].Network.biases = N1biases
        Hlist[1].Network.weights = N2weights
        Hlist[1].Network.biases = N2biases
        #Zusätzlich wird eine kleine random-Mutation durchgeführt
        Hlist[0].Network = myNetworkBuilder.mutateNetwork(Hlist[0].Network)
        Hlist[1].Network = myNetworkBuilder.mutateNetwork(Hlist[1].Network)
        #Die zwei Tiere werden zu den Jäger-Gruppe addiert
        GameHunter.add(Hlist[0])
        GameHunter.add(Hlist[1])
        #Die zwei Tiere werden vom Reproduktion-Pool gelöscht
        Hlist.pop(0)
        Hlist.pop(0)

    #Die gleiche Prozedur, nun aber mit der Beute...
    while len(Plist) >= 2:
        N1weights = Plist[0].Network.weights
        N2weights = Plist[1].Network.weights
        N1biases = Plist[0].Network.biases
        N2biases = Plist[1].Network.biases
        N1weights, N2weights = myNetworkBuilder.crossoverWeights(N1weights, N2weights)
        N1biases, N2biases = myNetworkBuilder.crossoverBiases(N1biases, N2biases)
        Plist[0].Network.weights = N1weights
        Plist[0].Network.biases = N1biases
        Plist[1].Network.weights = N2weights
        Plist[1].Network.biases = N2biases
        Plist[0].Network = myNetworkBuilder.mutateNetwork(Plist[0].Network)
        Plist[1].Network = myNetworkBuilder.mutateNetwork(Plist[1].Network)
        GamePrey.add(Plist[0])
        GamePrey.add(Plist[1])
        Plist.pop(0)
        Plist.pop(0)

#Graph Funktion.
def animate(Hpop, Ppop, Gpop, CurrentTime):
    mpl.cla()
    mpl.plot(CurrentTime, Hpop, CurrentTime, Ppop, CurrentTime, Gpop)
    mpl.legend(["Räuber","Beute","Gesamt"])
    mpl.xlabel('Zeit in Sekunden')
    mpl.ylabel('Anzahl Tiere')
    mpl.title('Populationsgrössen')
    mpl.ion()
    mpl.show()
    mpl.pause(0.001)


#Info-Funktionen: Schreiben FPS und infos auf der Screen für debuggen
def draw_fps(clock):
    font = ft.SysFont('Consolas', 20)
    fps = f'FPS: {clock.get_fps() :.2f}'
    font.render_to(WIN, (0, 17), text=fps, fgcolor='red', bgcolor='black')

def draw_info(text):
    font = ft.SysFont('Consolas', 20)
    font.render_to(WIN, (0, 0), text=text, fgcolor='green', bgcolor='black')

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

#Simulation ausführen
def runSimulation():
    start = time.time()

    run = True
    clock = pygame.time.Clock()

    framecount = 0
    
    GameHunter = pygame.sprite.Group()       #Jägertiere die auf dem Simulationsfeld sichtbar sind
    GamePrey = pygame.sprite.Group()         #Beutetiere die auf dem Simulationsfeld sichtbar sind
    HungryGameHunter = pygame.sprite.Group() #Jagende Tiere
    hunterRepro = pygame.sprite.Group()      #reproduktion-Pool für Jäger
    preyRepro = pygame.sprite.Group()        #reproduktion-Pool für Beute

    #Arrays für den Graph
    plot_ticks = []
    plot_hunter = []
    plot_prey = []
    plot_general = []
    
    spawn_animals(GameHunter, GamePrey)
    walker = HunterAnimal(WIN)          #Steuerbares Jägertier für debugging
    walker.Network.empty_Network()
    walker.angle = 270
    hider = PreyAnimal(WIN)             #Steuerbares Beutetier für debugging
    hider.Network.empty_Network()
    hider.angle = 270
    
    #lässt das Fenster in welches Pygame läuft erscheinen
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.SHOWN)
    
    #-----------------------------------------------GAMELOOP-----------------------------------------------

    while run:
        clock.tick(Globals.FPS)
        
        WIN.fill((0, 150, 0))

        GamePrey.update(GameHunter)
        GamePrey.draw(WIN)
        GameHunter.update(GamePrey)
        GameHunter.draw(WIN)

        #Hungrige jäger aktualisieren
        for hungry in GameHunter:
            if hungry.no_hunt == 0:
                HungryGameHunter.add(hungry)

        #Kollisionen zwischen den Hunters und der Prey detektieren
        check_collide(HungryGameHunter, GamePrey, hunterRepro)

        #Reproduktion von Beutetiere: Nach eine gewisse Fitness 
        # (Anzahl Frames die sie überlebt haben)
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

        #Graph-Berechnungen
        hunter_pop = len(GameHunter.sprites())
        prey_pop = len(GamePrey.sprites())
        general_pop = hunter_pop + prey_pop
        plot_ticks.append(pygame.time.get_ticks() / 1000)
        plot_hunter.append(hunter_pop)
        plot_prey.append(prey_pop)
        plot_general.append(general_pop)

        #Graph wird nicht bei jedem Frame aktualisiert (optimierung)
        framecount += 1
        if ((framecount % Globals.graph_rate) == 0):
            framecount = 0
            animate(plot_hunter, plot_prey, plot_general, plot_ticks)
        
        # if ((hunter_pop == 0) or (prey_pop == 0)):
        #     storeData(plot_ticks, plot_hunter, plot_prey)
        #     run = False


        #---------------WALKER&HIDER---------------
        walker.recharge()
        hider.recharge()
        hider.fitness = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            walker.x = 300
            walker.y = 300
            walker.vel = 0
            GameHunter.add(walker)
        if keys[pygame.K_2]:
            hider.x = 600
            hider.y = 600
            hider.vel = 0
            GamePrey.add(hider)
        
        if keys[pygame.K_a]:
            walker.rotate(turn_right=False, turn_angle=0.5)
        if keys[pygame.K_d]:
            walker.rotate(turn_right=True, turn_angle=0.5)
        if keys[pygame.K_w]:
            walker.increase_speed(0.3)
        if keys[pygame.K_s]:
            walker.reduce_speed(0.3)
        
        if keys[pygame.K_LEFT]:
            hider.rotate(turn_right=False, turn_angle=0.5)
        if keys[pygame.K_RIGHT]:
            hider.rotate(turn_right=True, turn_angle=0.5)
        if keys[pygame.K_UP]:
            hider.increase_speed(0.3)
        if keys[pygame.K_DOWN]:
            hider.reduce_speed(0.3) 
        #------------------------------------------

        if keys[pygame.K_ESCAPE]:
            storeData(plot_ticks, plot_hunter, plot_prey)
            end = time.time()
            timespan = end - start
            print(f'This simulation lasted for {timespan} seconds.')
            run = False
            break
        
        draw_fps(clock)
        pop_info = f"Hunters:{len(GameHunter.sprites())} - Preys: {len(GamePrey.sprites())} - Total: {len(GamePrey.sprites()) + len(GameHunter.sprites())}"
        draw_info(pop_info)
        SCRN.blit(WIN, (0, 0))

        pygame.display.flip()

        #Speichern der Daten nach Ende der Simulation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                storeData(plot_ticks, plot_hunter, plot_prey)
                end = time.time()
                timespan = end - start
                print(f'This simulation lasted for {timespan} seconds.')
                run = False
                break


    pygame.quit()

#Um die Simulation ohne GUI laufen zu lassen.
if __name__== "__main__":
    runSimulation()