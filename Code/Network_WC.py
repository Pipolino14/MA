import numpy as np

class Network:
    @classmethod

    def reproduceNetwork(cls):
        newweights = weights * [np.random.randn(5, 4), np.random.randn(4, 2)]
        newbiases = biases * [np.random.randn(4), np.random.randn(2)]
        return newweights, newbiases
    
    @staticmethod

    def __init__(self, weights, biases):
        self.weights = weights
        self.biases = biases
    
    def forward(self, x, weights, biases):
        #Input Layer: Inputs mit Gewichten multiplizieren und den Bias addieren
        hidden_layer_input = np.dot(x, weights[0]) + biases[0]
        #Aktivierungsmethode(Sigmoid anwenden)
        hidden_layer_output = sigmoid(hidden_layer_input)
        #Hidden Layer: Hidden Layer mit Gewichten multiplizieren und den Bias addieren
        output_layer_input = np.dot(hidden_layer_output, weights[1]) + biases[1]
        #Nochmals Sigmoid anwenden
        network_output = sigmoid(output_layer_input)

        return network_output

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))