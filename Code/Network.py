import numpy as np

# Klasse mit dem neuronalen Network von jedem Tier. Die Implementation ist selbsterklärend
class Network:
    def __init__(self, weights, biases):
        self.weights = weights
        self.biases = biases
    
    def forward(self, dist):
        #Input Layer: Inputs mit Gewichten multiplizieren und den Bias addieren
        hidden_layer_input = np.dot(dist, self.weights[0]) + self.biases[0]
        #Aktivierungsmethode tanh anwenden
        hidden_layer_output = np.tanh(hidden_layer_input)
        #Hidden Layer: Hidden Layer mit Gewichten multiplizieren und den Bias addieren
        output_layer_input = np.dot(hidden_layer_output, self.weights[1]) + self.biases[1]
        #Nochmals tanh anwenden
        network_output = np.tanh(output_layer_input)
        return network_output[0]
    
    def empty_Network(self):
        self.weights[0] = np.zeros_like(self.weights[0])
        self.weights[1] = np.zeros_like(self.weights[1])
        self.biases[0] = np.zeros_like(self.biases[0])
        self.biases[1] = np.zeros_like(self.biases[1])
