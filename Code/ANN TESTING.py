#Dies war meine testing-site für das neuronale Netzwerk
#Diese Version generiert random Nummern und hat die Architektur [5, 4, 3]

import numpy as np

#random 5-stelliger Vektor generieren
input_data = np.random.randn(5)

#random weights und Biases kreieren
weights = [np.random.randn(5, 4), np.random.randn(4, 3)]
biases = [np.random.randn(4), np.random.randn(3)]

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

    return network_output

result = forward(input_data, weights, biases)
print("Ausgabe:", result)