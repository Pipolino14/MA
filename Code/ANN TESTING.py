#Dies war meine testing-site für das neuronale Netzwerk
#Diese Version generiert random Nummern und hat die Architektur [5, 4, 3]

import numpy as np

#random 5-stelliger Vektor generieren
#input_data = np.random.randn(5)

#random weights und Biases kreieren
#weights = [np.random.randn(5, 4), np.random.randn(4, 2)]
#biases = [np.random.randn(4), np.random.randn(2)]

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def forward(x, weights, biases):
    #Input Layer: Inputs mit Gewichten multiplizieren und den Bias addieren
    hidden_layer_input = np.dot(x, weights[0]) + biases[0]
    #Aktivierungsmethode(Sigmoid anwenden)
    hidden_layer_output = sigmoid(hidden_layer_input)
    
    #Hidden Layer: Hidden Layer mit Gewichten multiplizieren und den Bias addieren
    output_layer_input = np.dot(hidden_layer_output, weights[1]) + biases[1]
    #Nochmals Sigmoid anwenden
    network_output = sigmoid(output_layer_input)

    walk = round(network_output[0])
    if walk == 0:
        print("Rückwärts")
    else:
        print("Vorwärts")

    turn = round(network_output[1])
    if turn == 0:
        print("Links")
    else:
        print("Rechts")
        


Rweights = [np.random.randn(5, 4), np.random.randn(4, 2)]
Rbiases = [np.random.randn(4), np.random.randn(2)]

forward(np.random.randn(5), Rweights, Rbiases)
forward(np.random.randn(5), Rweights, Rbiases)
forward(np.random.randn(5), Rweights, Rbiases)
forward(np.random.randn(5), Rweights, Rbiases)
forward(np.random.randn(5), Rweights, Rbiases)
forward(np.random.randn(5), Rweights, Rbiases)
forward(np.random.randn(5), Rweights, Rbiases)
forward(np.random.randn(5), Rweights, Rbiases)