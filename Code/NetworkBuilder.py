import numpy as np
from Network import *

class NetworkBuilder:
    def __init__(self, weights, biases):
        self.weights = weights
        self.biases = biases
        
    def buildNewNetwork(self):
        weights = [np.random.randn(5, 4), np.random.randn(4, 2)]
        biases = [np.random.randn(4), np.random.randn(2)]
        return weights, biases
    
    def crossoverWeights(self, N1weights_1, N2weights_1, N1weights_2, N2weights_2):
        #mit .shape finde ich for formen heraus [5, 4] und [4, 2] ich verwende hier nur die Zeilen, da die Reihen immer einen Bias haben und danach die nachfolgenden Weights
        weightsLane_1 = N1weights_1.shape
        weightsLane_2 = N1weights_2.shape

        #hier wählt es zufällig zwei Zeilen aus, um das Crossover zu machen
        crossoverWeights_1 = np.random.randint(1, weightsLane_1[0])
        crossoverWeights_2 = np.random.randint(1, weightsLane_2[0])

        #hier addiert es den ersten Teil der ersten Matrix mit dem anderen der 2. und das gleiche auch noch umgekehrt --> Crossover wird hier durchgeführt
        newWeightsN1_1 = np.hstack((N1weights_1[:, :crossoverWeights_1], N2weights_1[:, crossoverWeights_1:]))
        newWeightsN2_1 = np.hstack((N2weights_1[:, :crossoverWeights_1], N1weights_1[:, crossoverWeights_1:]))
        newWeightsN1_2 = np.hstack((N1weights_2[:, :crossoverWeights_2], N2weights_2[:, crossoverWeights_2:]))
        newWeightsN2_2 = np.hstack((N2weights_2[:, :crossoverWeights_2], N1weights_2[:, crossoverWeights_2:]))

        return newWeightsN1_1, newWeightsN2_1, newWeightsN1_2, newWeightsN2_2
    
    def crossoverBiases(self, N1biases_1, N2biases_1, N1biases_2, N2biases_2):
        #das Gleiche Prinzip, wie bei crossoverWeights mit dem Unterschied, dass für Vektoren die funktion concentrate verwendet werden muss.
        biasesLane_1 = N1biases_1.shape
        biasesLane_2 = N1biases_2.shape

        crossoverBiases_1 = np.random.randint(1, biasesLane_1[1])
        crossoverBiases_2 = np.random.randint(1, biasesLane_2[1])

        newBiasesN1_1 = np.concatenate((N1biases_1[:crossoverBiases_1], N2biases_1[crossoverBiases_1:]))
        newBiasesN2_1 = np.concatenate((N2biases_1[:crossoverBiases_1], N1biases_1[crossoverBiases_1:]))
        newBiasesN1_2 = np.concatenate((N1biases_2[:crossoverBiases_2], N2biases_2[crossoverBiases_2:]))
        newBiasesN2_2 = np.concatenate((N2biases_2[:crossoverBiases_2], N1biases_2[crossoverBiases_2:]))
            
        return newBiasesN1_1, newBiasesN2_1, newBiasesN1_2, newBiasesN2_2

    def mutateNetwork(self, parentNetwork):
        rngweights = [np.random.randn(5, 4), np.random.randn(4, 2)]
        rngbiases = [np.random.randn(4), np.random.randn(2)]
        newweights = [np.add(parentNetwork.weights[0] , rngweights[0]) , np.add(parentNetwork.weights[1] , rngweights[1])]
        newbiases = [np.add(parentNetwork.biases[0] , rngbiases[0]) , np.add(parentNetwork.biases[1] , rngbiases[1])]
        childNetwork = Network(newweights, newbiases)
        return childNetwork
    
