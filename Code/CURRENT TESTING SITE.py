import pygame
import numpy as np

class Matrix:
    def __init__(self):
        self.weights = [np.arange(20).reshape(5, 4), np.arange(8).reshape(4, 2)]
        self.biases = [np.arange(4), np.arange(2)]

g = np.random.uniform(low=-0.1, high=0.1, size=4)

rng = np.random.randint(low=-1, high=2, size=(5, 4))
rng2 = np.random.randint(2, size=(5, 4))

y = rng * rng2


#print(rng)
#print(res)

def mutateNetwork_3(inputNetwork):
        #Mache random Matrizen, welcher von -0.1 bis 0.1 gehen kann
        mutWeights_1 = np.random.uniform(low=-0.1, high=0.1, size=(5, 4)) 
        mutWeights_2 = np.random.uniform(low=-0.1, high=0.1, size=(4, 2))
        mutBiases_1 = np.random.uniform(low=-0.1, high=0.1, size=4)
        mutBiases_2 = np.random.uniform(low=-0.1, high=0.1, size=2)

        #Hier kreiere ich eine Matrix, welche entweder -1, 0, 1 enthalten kann. Dies mache ich für alle Matrizen.
        Weights_1_rng = np.random.randint(low=-1, high=2, size=(5, 4))
        Weights_2_rng = np.random.randint(low=-1, high=2, size=(4, 2))
        Biases_1_rng = np.random.randint(low=-1, high=2, size=4)
        Biases_2_rng = np.random.randint(low=-1, high=2, size=2)

        #Da bei der vorherigen immernoch ein grossteil der Nummern geändert werden, kreiere ich hier Matrizen mit nur 1 oder 0 und multipliziere diese mit der vorherigen Matrix.
        Weights_1_rng = Weights_1_rng * np.random.randint(2, size=(5, 4))
        Weights_2_rng = Weights_2_rng * np.random.randint(2, size=(4, 2))
        Biases_1_rng = Biases_1_rng * np.random.randint(2, size=4)
        Biases_2_rng = Biases_2_rng * np.random.randint(2, size=2)

        #Jetzt multipliziere ich die rng matrizen mit den random Matrizen, dass nun nur in spezifischen orten ein wechsel stattgefunden hat und dieser Positiv, sowie auch negativ sein kann.
        selWeights1 = mutWeights_1 * Weights_1_rng
        selWeights2 = mutWeights_2 * Weights_2_rng
        selBiases1 = mutBiases_1 * Biases_1_rng
        selBiases2 = mutBiases_2 * Biases_2_rng
        
        newweights = [np.add(inputNetwork.weights[0] , selWeights1) , np.add(inputNetwork.weights[1] , selWeights2)]
        newbiases = [np.add(inputNetwork.biases[0] , selBiases1) , np.add(inputNetwork.biases[1] , selBiases2)]

        outputNetwork = [newweights, newbiases]
        return outputNetwork

x = Matrix()

x = mutateNetwork_3(x)
print(x)