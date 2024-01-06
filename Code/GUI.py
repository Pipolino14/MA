import tkinter as tk
import customtkinter as cti

from PIL import Image
from Main import *
from Globals import *

# Dieses Modul enthält die GUI. Damit kann man komfortabler 
# die globale Settings vor einer Simulation ändern.

cti.set_appearance_mode("dark")
cti.set_default_color_theme("dark-blue")

root = cti.CTk()

MainTitleFont = cti.CTkFont(family="Stencil", size=120, underline=True)
StartFont = cti.CTkFont(family="Arial Black", weight="bold", size=40)
TitleFont = cti.CTkFont(family="Arial Black", size=30, underline=True)
subTitleFont = cti.CTkFont(family="Arial Black", size=20)
comFont = cti.CTkFont(family="Arial", size=16)
comFontIta = cti.CTkFont(family="Arial", size=14, slant="italic")

root.title('Calculation of the Fittest')
root.geometry(f'1920x1080+10+10')


def hp_confirmsettings():
    #Hunter
    Hfov = h_FOV.get() if h_FOV.get()!='' else Globals.HUNTER_FOV
    Globals.HUNTER_FOV = int(Hfov)

    Hrov = h_ROV.get() if h_ROV.get()!='' else Globals.HUNTER_ROV
    Globals.HUNTER_ROV = int(Hrov)

    Hnrg = h_NRG.get() if h_NRG.get()!='' else Globals.hunter_energy
    Globals.hunter_energy = int(Hnrg)

    Hsat = h_SAT.get() if h_SAT.get()!='' else Globals.no_hunt_period
    Globals.no_hunt_period = int(Hsat)

    Hrep = h_REP.get() if h_REP.get()!='' else Globals.hunter_repro_fitness
    Globals.hunter_repro_fitness = int(Hrep)

    #Prey
    Pfov = p_FOV.get() if p_FOV.get()!='' else Globals.PREY_FOV
    Globals.PREY_FOV = int(Pfov)

    Prov = p_ROV.get() if p_ROV.get()!='' else Globals.PREY_ROV
    Globals.PREY_ROV = int(Prov)


    Pnrg = p_NRG.get() if p_NRG.get()!='' else Globals.prey_energy
    Globals.prey_energy = int(Pnrg)

    if ',' in p_NRG.get():
        SpawnRange = tuple(map(int, p_DIS.get().split(',')))
        p_DIS_Tipp.configure(text="(empfohlen: 5-15)", font=comFontIta, text_color="white")
        Globals.min_repro_range = min(SpawnRange[0], SpawnRange[1])
        Globals.max_repro_range = max(SpawnRange[0], SpawnRange[1])

    Prep = p_REP.get() if p_REP.get()!='' else Globals.prey_reproduction
    Globals.prey_reproduction = int(Prep)

def g_confirmsettings():
    numH = g_h_Amount.get() if g_h_Amount.get()!='' else Globals.numHunters
    Globals.numHunters = int(numH)

    numP = g_p_Amount.get() if g_p_Amount.get()!='' else Globals.numPreys
    Globals.numPreys = int(numP)

    print(Globals.numHunters)
    print(Globals.numPreys)

def resizer(index):
    Globals.animal_size = (index/100)
    print(Globals.animal_size)
    g_A_Size_Number.configure(text=f'Size: {index}%')

def turnAngleSlider(angel):
    Globals.angle_factor = (angel)
    g_MAX_Turn_Number.configure(text=f'Maximal: {angel}°')

def vRaySize(size):
    Globals.vision_ray = size
    g_Vray_Number.configure(text=f'Länge: {size}px')

def showrayToggle():
    rayShow = g_show_ray.get()
    if rayShow == 1:
        Globals.show_ray == True
        print("Rays: True")
    else:
        Globals.show_ray == False
        print("Rays: False")

def showtargetToggle():
    tarShow = g_show_target.get()
    if tarShow == 1:
        Globals.show_target == True
        print("Target: True")
    else:
        Globals.show_target == False
        print("Target: False")

def FPSslider(frames):
    Globals.FPS = frames
    r_FPS_Number.configure(text=f'Max: {frames}fps')

def graphupdateSlider(amount):
    Globals.graph_rate = amount
    r_GRA_Number.configure(text=f'Jede {amount} frames')

def numberneuronSlider(Neurons):
    Globals.hiddenN = int(Neurons)
    n_NNE_Number.configure(text=f'Anz.: {Neurons}')

def MutstrengthSlider(Strength):
    Globals.MutStrength = (Strength/100)
    n_MUT_STR_Number.configure(text=f'Stärke: {Strength}%')

def MutprobabilitySlider(Probability):
    Globals.MutProbability = (Probability/100)
    n_MUT_PRB_Number.configure(text=f'Wahrscheinlichkeit: {Probability}%')

def fullscreenCheck():
    fullscrn = r_SCN_FULL.get()
    if fullscrn == 1:
        Globals.FULL == True
        print("Full: True")
    else:
        Globals.FULL == False
        print("Full: False")

def goSimulate():
    root.destroy()
    runSimulation()


w_pady = 5
w_padx = 5

pad_x = 5
pad_y = 0

TabFill = "both"

Upper_frame = cti.CTkFrame(root, fg_color="#212121")
Upper_frame.pack(side="top", fill="both", expand=True)
Upper_frame.columnconfigure(0, weight=1)
Upper_frame.rowconfigure(0, weight=1)

Lower_frame = cti.CTkFrame(root, fg_color="#212121")
Lower_frame.pack(side="top", fill="both", expand=True)

bg_image = cti.CTkImage(dark_image=Image.open("Code/Assets/UI_Background.png"), size=(1920, 480))

#---------------------------------------GENERAL-SETTINGS---------------------------------------
GTab = cti.CTkFrame(Lower_frame, fg_color="#2a7a1d")
GTab.pack(side="left", pady=w_pady, padx=w_padx, fill=TabFill, expand=True)
GTab.columnconfigure(0, weight=1)
GTab.columnconfigure(1, weight=1)

g_settings_label = cti.CTkLabel(GTab, text="General Settings", font=TitleFont)
g_settings_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

g_amount_label = cti.CTkLabel(GTab, text="Anzahl Tiere", font=subTitleFont)
g_amount_tipp = cti.CTkLabel(GTab, text="(empfohlen: 1:4 Räuber:Beute)", font=comFontIta)
g_amount_label.grid(row=1, column=0, columnspan=2, padx=pad_x, pady=pad_y)
g_amount_tipp.grid(row=2, column=0, columnspan=2, padx=pad_x, pady=pad_y)


g_h_Amount_label = cti.CTkLabel(GTab, text="Räuber", font=comFont)
g_h_Amount = cti.CTkEntry(GTab, placeholder_text=Globals.numHunters)
g_h_Amount_label.grid(row=3, column=0, padx=pad_x, pady=pad_y)
g_h_Amount.grid(row=4, column=0, padx=pad_x, pady=pad_y, sticky=tk.E+tk.W)

g_p_Amount_label = cti.CTkLabel(GTab, text="Beute", font=comFont)
g_p_Amount = cti.CTkEntry(GTab, placeholder_text=Globals.numPreys)
g_p_Amount_label.grid(row=3, column=1, padx=pad_x, pady=pad_y)
g_p_Amount.grid(row=4, column=1, padx=pad_x, pady=pad_y, sticky=tk.E+tk.W)

g_hp_Amount_btn = cti.CTkButton(GTab, text="Anzahlen Bestätigen", font=comFont, fg_color="#106000", command=g_confirmsettings)
g_hp_Amount_btn.grid(row=5, column=0, columnspan=2, padx=pad_x, pady=pad_y, sticky=tk.E+tk.W)

g_A_Size_label = cti.CTkLabel(GTab, text="Grösse der Tiere", font=subTitleFont)
g_A_Size_tipp = cti.CTkLabel(GTab, text="(max: 64px)(empfohlen: 20-30%)", font=comFontIta)
g_A_Size = cti.CTkSlider(GTab, from_=0, to=100, number_of_steps=20, command=resizer)
g_A_Size.set(Globals.animal_size*100)
g_A_Size_Number = cti.CTkLabel(GTab, text=f'Size: {g_A_Size.get()}%', font=comFont)
g_A_Size_label.grid(row=6, column=0, columnspan=2, padx=pad_x, pady=pad_y)
g_A_Size_tipp.grid(row=7, column=0, columnspan=2, padx=pad_x, pady=pad_y)
g_A_Size.grid(row=8, column=0, columnspan=2, padx=pad_x, pady=pad_y)
g_A_Size_Number.grid(row=9, column=0, columnspan=2, padx=pad_x, pady=pad_y)

g_MAX_Turn_label = cti.CTkLabel(GTab, text="Maximaler Drehwinkel in einem Frame", font=subTitleFont)
g_MAX_Turn_tipp = cti.CTkLabel(GTab, text="(empfohlen: 10°-20°)", font=comFontIta)
g_MAX_Turn = cti.CTkSlider(GTab, from_=0, to=50, number_of_steps=10, command=turnAngleSlider)
g_MAX_Turn.set(Globals.angle_factor)
g_MAX_Turn_Number = cti.CTkLabel(GTab, text=f'Maximal: {g_MAX_Turn.get()}°', font=comFont)
g_MAX_Turn_label.grid(row=10, column=0, columnspan=2, padx=pad_x, pady=pad_y)
g_MAX_Turn_tipp.grid(row=11, column=0, columnspan=2, padx=pad_x, pady=pad_y)
g_MAX_Turn.grid(row=12, column=0, columnspan=2, padx=pad_x, pady=pad_y)
g_MAX_Turn_Number.grid(row=13, column=0, columnspan=2, padx=pad_x, pady=pad_y)

g_Vray_label = cti.CTkLabel(GTab, text="Länge des Richtungsvektor in Pixel", font=subTitleFont)
g_Vray_tipp = cti.CTkLabel(GTab, text="(empfohlen: 20-40)", font=comFontIta)
g_Vray = cti.CTkSlider(GTab, from_=0, to=100, number_of_steps=20, command=vRaySize)
g_Vray.set(Globals.vision_ray)
g_Vray_Number = cti.CTkLabel(GTab, text=f'Länge: {g_A_Size.get()}px', font=comFont)
g_Vray_label.grid(row=14, column=0, columnspan=2, padx=pad_x, pady=pad_y)
g_Vray_tipp.grid(row=15, column=0, columnspan=2, padx=pad_x, pady=pad_y)
g_Vray.grid(row=16, column=0, columnspan=2, padx=pad_x, pady=pad_y)
g_Vray_Number.grid(row=17, column=0, columnspan=2, padx=pad_x, pady=pad_y)

g_show_ray = cti.CTkSwitch(GTab, text="show rays", font=subTitleFont, command=showrayToggle)
g_show_ray.grid(row=18, column=0, columnspan=2, padx=pad_x, pady=pad_y)

g_show_target = cti.CTkSwitch(GTab, text="show target", font=subTitleFont, command=showtargetToggle)
g_show_target.grid(row=19, column=0, columnspan=2, padx=pad_x+5, pady=pad_y+5)






#-----------------------------------HUNTER-AND-PREY-SETTINGS-----------------------------------

ATab = cti.CTkFrame(Lower_frame, fg_color="#006569")
ATab.pack(side="left", pady=w_pady, padx=w_padx, fill="x", expand=True)
ATab.columnconfigure(0, weight=1)
ATab.columnconfigure(2, weight=1)

hp_settings_label = cti.CTkLabel(ATab, text="Animal Einstellungen", font=TitleFont)
hp_settings_label.grid(row=0, column=0, columnspan=3, padx=20, pady=20)

hp_confirm = cti.CTkButton(ATab, text="confirm Settings", command=hp_confirmsettings)
hp_confirm.grid(row=21, column=0, columnspan=3, padx=20, pady=20)

middle_column = cti.CTkFrame(ATab, fg_color="#b8fcff", width=5)
middle_column.grid(row=1, column=1, rowspan=20, padx=pad_x, sticky=tk.N+tk.E+tk.S+tk.W)

#-------------HUNTER-------------
h_label = cti.CTkLabel(ATab, text="Jäger Einstellungen", font=subTitleFont)
h_label.grid(row=1, column=0)

#FOV
h_FOV_label = cti.CTkLabel(ATab, text="Sichtfeld in Grad", font=comFont)
h_FOV_Tipp = cti.CTkLabel(ATab, text="(empfohlen: 40°-60°)", font=comFontIta)
h_FOV = cti.CTkEntry(ATab, placeholder_text=Globals.HUNTER_FOV)
h_FOV_label.grid(row=2, column=0, padx=pad_x, pady=pad_y,sticky=tk.W)
h_FOV_Tipp.grid(row=3, column=0, padx=pad_x, pady=pad_y, sticky=tk.W)
h_FOV.grid(row=4, column=0, padx=pad_x, pady=pad_y, sticky=tk.E+tk.W)

#ROV
h_ROV_label = cti.CTkLabel(ATab, text="Sichtweite in Pixel", font=comFont)
h_ROV_Tipp = cti.CTkLabel(ATab, text="(empfohlen: 300-400)", font=comFontIta)
h_ROV = cti.CTkEntry(ATab, placeholder_text=Globals.HUNTER_ROV)
h_ROV_label.grid(row=6, column=0, padx=pad_x, pady=pad_y,sticky=tk.W)
h_ROV_Tipp.grid(row=7, column=0, padx=pad_x, pady=pad_y, sticky=tk.W)
h_ROV.grid(row=8, column=0, padx=pad_x, pady=pad_y, sticky=tk.E+tk.W)

#Energy
h_NRG_label = cti.CTkLabel(ATab, text="Energie in Frames", font=comFont)
h_NRG_Tipp = cti.CTkLabel(ATab, text="(empfohlen: 700-1200)", font=comFontIta)
h_NRG = cti.CTkEntry(ATab, placeholder_text=Globals.hunter_energy)
h_NRG_label.grid(row=10, column=0, padx=pad_x, pady=pad_y,sticky=tk.W)
h_NRG_Tipp.grid(row=11, column=0, padx=pad_x, pady=pad_y, sticky=tk.W)
h_NRG.grid(row=12, column=0, padx=pad_x, pady=pad_y, sticky=tk.E+tk.W)

#Saturation
h_SAT_label = cti.CTkLabel(ATab, text="Sättigungszeit in Frames", font=comFont)
h_SAT_Tipp = cti.CTkLabel(ATab, text="(empfohlen: 5-10)", font=comFontIta)
h_SAT = cti.CTkEntry(ATab, placeholder_text=Globals.no_hunt_period)
h_SAT_label.grid(row=14, column=0, padx=pad_x, pady=pad_y,sticky=tk.W)
h_SAT_Tipp.grid(row=15, column=0, padx=pad_x, pady=pad_y, sticky=tk.W)
h_SAT.grid(row=16, column=0, padx=pad_x, pady=pad_y, sticky=tk.E+tk.W)

#Reproduction
h_REP_label = cti.CTkLabel(ATab, text="Reproduktion in Anzahl geferssener Beute", font=comFont)
h_REP_Tipp = cti.CTkLabel(ATab, text="(empfohlen: 2-3)", font=comFontIta)
h_REP = cti.CTkEntry(ATab, placeholder_text=Globals.hunter_repro_fitness)
h_REP_label.grid(row=18, column=0, padx=pad_x, pady=pad_y,sticky=tk.W)
h_REP_Tipp.grid(row=19, column=0, padx=pad_x, pady=pad_y, sticky=tk.W)
h_REP.grid(row=20, column=0, padx=pad_x, pady=pad_y, sticky=tk.E+tk.W)

#-------------PREY-------------
p_label = cti.CTkLabel(ATab, text="Beute Einstellungen", font=subTitleFont)
p_label.grid(row=1, column=2)

#FOV
p_FOV_label = cti.CTkLabel(ATab, text="Sichtfeld in Grad", font=comFont)
p_FOV_Tipp = cti.CTkLabel(ATab, text="(empfohlen: 180°-270°)", font=comFontIta)
p_FOV = cti.CTkEntry(ATab, placeholder_text=Globals.PREY_FOV)
p_FOV_label.grid(row=2, column=2, padx=pad_x, pady=pad_y,sticky=tk.W)
p_FOV_Tipp.grid(row=3, column=2, padx=pad_x, pady=pad_y, sticky=tk.W)
p_FOV.grid(row=4, column=2, padx=pad_x, pady=pad_y, sticky=tk.E+tk.W)

#ROV
p_ROV_label = cti.CTkLabel(ATab, text="Sichtweite in Pixel", font=comFont)
p_ROV_Tipp = cti.CTkLabel(ATab, text="(empfohlen: 150-250)", font=comFontIta)
p_ROV = cti.CTkEntry(ATab, placeholder_text=Globals.PREY_ROV)
p_ROV_label.grid(row=6, column=2, padx=pad_x, pady=pad_y,sticky=tk.W)
p_ROV_Tipp.grid(row=7, column=2, padx=pad_x, pady=pad_y, sticky=tk.W)
p_ROV.grid(row=8, column=2, padx=pad_x, pady=pad_y, sticky=tk.E+tk.W)

#Energy
p_NRG_label = cti.CTkLabel(ATab, text="Energie in Frames", font=comFont)
p_NRG_Tipp = cti.CTkLabel(ATab, text="(empfohlen: 200-500)", font=comFontIta)
p_NRG = cti.CTkEntry(ATab, placeholder_text=Globals.prey_energy)
p_NRG_label.grid(row=10, column=2, padx=pad_x, pady=pad_y,sticky=tk.W)
p_NRG_Tipp.grid(row=11, column=2, padx=pad_x, pady=pad_y, sticky=tk.W)
p_NRG.grid(row=12, column=2, padx=pad_x, pady=pad_y, sticky=tk.E+tk.W)

#Distance in child
p_DIS_label = cti.CTkLabel(ATab, text="Distanz neues Kind", font=comFont)
p_DIS_Tipp = cti.CTkLabel(ATab, text="(empfohlen: 5-15) [bitte zwei Zahlen angeben]", font=comFontIta)
p_DIS = cti.CTkEntry(ATab, placeholder_text=f"{Globals.min_repro_range},{Globals.max_repro_range}")
p_DIS_label.grid(row=14, column=2, padx=pad_x, pady=pad_y,sticky=tk.W)
p_DIS_Tipp.grid(row=15, column=2, padx=pad_x, pady=pad_y, sticky=tk.W)
p_DIS.grid(row=16, column=2, padx=pad_x, pady=pad_y, sticky=tk.E+tk.W)

#Reproduction
p_REP_label = cti.CTkLabel(ATab, text="Reproduktion in Anzahl frames", font=comFont)
p_REP_Tipp = cti.CTkLabel(ATab, text="(empfohlen: 200-400)", font=comFontIta)
p_REP = cti.CTkEntry(ATab, placeholder_text=Globals.prey_reproduction)
p_REP_label.grid(row=18, column=2, padx=pad_x, pady=pad_y,sticky=tk.W)
p_REP_Tipp.grid(row=19, column=2, padx=pad_x, pady=pad_y, sticky=tk.W)
p_REP.grid(row=20, column=2, padx=pad_x, pady=pad_y, sticky=tk.E+tk.W)


Bottom_Right_frame = cti.CTkFrame(Lower_frame, fg_color="#212121")
Bottom_Right_frame.pack(side="left", fill=TabFill, expand=True)
#-----------------------------------------RUN_SETTINGS-----------------------------------------
RTab = cti.CTkFrame(Bottom_Right_frame, fg_color="#bd8339")
RTab.pack(side="top", pady=w_pady, padx=w_padx, fill=TabFill, expand=True)
RTab.columnconfigure(0, weight=1)

r_settings_label = cti.CTkLabel(RTab, text="Simulations Einstellungen", font=TitleFont)
r_settings_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

r_FPS_label = cti.CTkLabel(RTab, text="Frames per seconds Limit", font=subTitleFont)
r_FPS_tipp = cti.CTkLabel(RTab, text="(Simulation wird meist unter 5 FPS laufen)", font=comFontIta)
r_FPS = cti.CTkSlider(RTab, from_=5, to=60, number_of_steps=55, command=FPSslider)
r_FPS.set(Globals.FPS)
r_FPS_Number = cti.CTkLabel(RTab, text=f'Max: {r_FPS.get()}fps', font=comFont)
r_FPS_label.grid(row=1, column=0, padx=pad_x, pady=pad_y/2)
r_FPS_tipp.grid(row=2, column=0, padx=pad_x, pady=pad_y/2)
r_FPS.grid(row=3, column=0, padx=pad_x, pady=pad_y/2)
r_FPS_Number.grid(row=4, column=0, padx=pad_x, pady=pad_y/2)

r_GRA_label = cti.CTkLabel(RTab, text="Graph update in frames", font=subTitleFont)
r_GRA_tipp = cti.CTkLabel(RTab, text="(empfohlen: 30)", font=comFontIta)
r_GRA = cti.CTkSlider(RTab, from_=10, to=60, number_of_steps=5, command=graphupdateSlider)
r_GRA.set(Globals.graph_rate)
r_GRA_Number = cti.CTkLabel(RTab, text=f'Jede {r_GRA.get()} frames', font=comFont)
r_GRA_label.grid(row=1, column=1, padx=pad_x, pady=pad_y/2)
r_GRA_tipp.grid(row=2, column=1, padx=pad_x, pady=pad_y/2)
r_GRA.grid(row=3, column=1, padx=pad_x, pady=pad_y/2)
r_GRA_Number.grid(row=4, column=1, padx=pad_x, pady=pad_y/2)

r_SCN_label = cti.CTkLabel(RTab, text="Screen Einstellungen", font=subTitleFont)
r_SCN_label.grid(row=5, column=0, columnspan=2, padx=pad_x, pady=pad_y/2)
r_SCN_FULL = cti.CTkSwitch(RTab, text="Fullscreen", font=subTitleFont, command=fullscreenCheck)
r_SCN_FULL.grid(row=6, column=0, columnspan=2, padx=pad_x, pady=pad_y/2)


NTab = cti.CTkFrame(Bottom_Right_frame, fg_color="#163432")
NTab.pack(side="top", pady=w_pady, padx=w_padx, fill=TabFill, expand=True)
NTab.columnconfigure(0, weight=1)

n_settings_label = cti.CTkLabel(NTab, text="Netzwerk Einstellungen", font=TitleFont)
n_settings_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

n_NNE_label = cti.CTkLabel(NTab, text="Anzahl Neuronen", font=subTitleFont)
n_NNE_tipp = cti.CTkLabel(NTab, text="(empfohlen: 2)", font=comFontIta)
n_NNE = cti.CTkSlider(NTab, from_=2, to=10, number_of_steps=8, command=numberneuronSlider)
n_NNE.set(Globals.hiddenN)
n_NNE_Number = cti.CTkLabel(NTab, text=f'Anz.: {n_NNE.get()}', font=comFont)
n_NNE_label.grid(row=9, column=0, columnspan=2, padx=pad_x, pady=pad_y/2)
n_NNE_tipp.grid(row=10, column=0, columnspan=2, padx=pad_x, pady=pad_y/2)
n_NNE.grid(row=11, column=0, columnspan=2, padx=pad_x, pady=pad_y/2)
n_NNE_Number.grid(row=12, column=0, columnspan=2, padx=pad_x, pady=pad_y/2)

n_MUT_label = cti.CTkLabel(NTab, text="Mutationswahrscheinlichkeit & Stärke", font=subTitleFont)
n_MUT_tipp = cti.CTkLabel(NTab, text="(empfohlen: 20% & 0.1)", font=comFontIta)
n_MUT_STR = cti.CTkSlider(NTab, from_=0, to=100, number_of_steps=20, command=MutstrengthSlider)
n_MUT_STR.set((Globals.MutStrength*100))
n_MUT_STR_Number = cti.CTkLabel(NTab, text=f'Stärke: {n_MUT_STR.get()}%', font=comFont)
n_MUT_PRB = cti.CTkSlider(NTab, from_=0, to=100, number_of_steps=20, command=MutprobabilitySlider)
n_MUT_PRB.set((Globals.MutProbability*100))
n_MUT_PRB_Number = cti.CTkLabel(NTab, text=f'Wahrscheinlichkeit{n_MUT_PRB.get()}%', font=comFont)
n_MUT_label.grid(row=13, column=0, columnspan=2, padx=pad_x, pady=pad_y/2)
n_MUT_tipp.grid(row=14, column=0, columnspan=2, padx=pad_x, pady=pad_y/2)
n_MUT_STR.grid(row=15, column=1, padx=pad_x, pady=pad_y/2)
n_MUT_STR_Number.grid(row=16, column=1, padx=pad_x, pady=pad_y/2)
n_MUT_PRB.grid(row=15, column=0, padx=pad_x, pady=pad_y/2)
n_MUT_PRB_Number.grid(row=16, column=0, padx=pad_x, pady=pad_y/2)

#-----------------------------------------START-FRAME------------------------------------------
StartTab = cti.CTkFrame(Bottom_Right_frame, fg_color="#bf564e", height=100)
StartTab.pack(side="top", pady=w_pady, padx=w_padx, fill="both")
StartTab.columnconfigure(0, weight=1)
StartTab.rowconfigure(0, weight=1)

run_btn = cti.CTkButton(StartTab, text="Simulation Starten", height=StartTab.cget("height"), width=StartTab.cget("width"), command=goSimulate, font=StartFont, fg_color="#FF1616")
run_btn.grid(padx=10, pady=10, sticky=tk.E+tk.W)

#------------------------------------------TITLE-----------------------------------------------

Title_label = cti.CTkLabel(Upper_frame, text="Calculation of the fittest", font=MainTitleFont, image=bg_image)
Title_label.grid()

root.mainloop()
