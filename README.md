# Calculation of the fittest
Github Repository für meine Maturarbeit.
Abgabedatum: 8.1.2024

## Anleitung für Installation
Zip-datei herunterladen und Ordner extrahieren.
[Module](###Module) herunterladen, falls noch nicht vorhanden.

### Windows
- mit Interface:   auf Win_Start_GUI.bat klicken.
- [ohne](##Variabeln) Interface:  auf Win_Start_normal.bat klicken.

### Mac
1. ein Terminal Fenster öffnen.
2. (Falls noch nicht schon dort): Zum Ordner der Installation navigieren.
3. den command ins Terminal eingeben: chmod 755 Mac_Start_normal.sh

#### Probleme(Mac)
- Das Interface Funktioniert nicht.
- Fullscreenmodus kann nicht akriviert werden.

### Module
Folgende Module sind normalerweise nicht in python Vorhanden.
| Modul name | Installation mit pip |
| ---------- | ---------------------|
| [pygame](https://www.pygame.org/docs/) | python -m pip install pygame |
| [NumPy](https://numpy.org/doc/stable/reference/index.html) | python -m pip install numpy |
| [pandas](https://pandas.pydata.org/docs/) | python -m pip install pandas |
| (für interface) [CustomTkinter](https://customtkinter.tomschimansky.com/documentation/) | python -m pip install customtkinter |

## Variabeln
Folgende Variabeln können auch manuell in der Datei Globals.py geändert werden.
| Variabelname | Funktion |
| ------------ | -------- |
| FPS | maximale Anzahl FPS |
| FULL | Fullscreen oder nicht |
| HUNTER_ROV | Sichweite der Räuber (in px) |
| PREY_ROV | Sichweite der Beutetiere (in px) |
| HUNTER_FOV | Sichtfeld der Räuber (in °) |
| PREY_FOV | Sichtfeld der Beutetiere (in °) |
| numHunters | Anzahl Räuber bei Start der Simulation |
| numPreys | Anzahl Beutetiere bei Start der Simulation |
| angle_factor | Maximaler Drehwinkel eines Tieres (in °) |
| hiddenN | Anzahl Neuronen in der Hidden Layer |
| MutProbability | Wahrscheinlichkeit der Mutation in einem Weight/Bias (1 = 100%)|
| MutStrength | Stärke der Mutation eines Weight/Bias |
| hunter_energy | Startenergie eines Räubers (in frames)|
| prey_energy | Startenergie eines Beutetieres (in frames)|
| no_hunt_period | Sättigungszeitspanne eines Räubers nach dem Fressen eines Beutetieres  (in frames) |
| prey_reproduction | Reproduktionszeitspanne eines Beutetieres (in frames) | 
| hunter_repro_fitness | Anzahl gefressener Beute bis zur Replikation |
| min_repro_range, max_repro_range | Region, in welcher die Kinder von Beutetieren von ihren Eltern spawnen (in px)|
| animal_size | Grösse aller Tiere der Simulation (1 = 100% = 64px*64px)|
| graph_rate | Zeitintervall in welchem der Populationsgraph geupdated wird (in frames)|
| show_ray | Zeigt die Sichtstrahlen der Tiere an |
| show_target | Zeichnet eine Linie zu allen gesehenen Tiere |
| store_data | ob die Simulationsdaten gespeichert werden sollen |
| vision_ray | Länge des Richtungsvektors der Tiere (in px) |















