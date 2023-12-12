import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Initialisierung der Daten
x_data = []
y_data = []


# Funktion zum Aktualisieren der Daten
def update_data(counter):
    # Füge aktuelle Zeitpunkt auf der X-Achse hinzu
    now = counter
    x_data.append(now)
    
    # Erhalte zufällige Nummer als Y-Wert
    y_data.append(len(GameHunter.sprites()))

    # Begrenze die Anzahl der angezeigten Datenpunkte
    max_datapoints = 10
    if len(x_data) > max_datapoints:
        x_data.pop(0)
        y_data.pop(0)

    # Aktualisiere den Graphen
    ax.clear()
    ax.plot(x_data, y_data)
    ax.set_title('Echtzeit-Liniengrafik')
    ax.set_xlabel('Vergangene Zeit')
    ax.set_ylabel('Nummer')

# Erstelle Matplotlib-Figur und Achse
fig, ax = plt.subplots()

# Erstelle die Animation mit einer Aktualisierungsrate von 500 Millisekunden (0.5 Sekunden)
ani = animation.FuncAnimation(fig, update_data, interval=1000)

# Zeige den Graphen an
plt.show()
