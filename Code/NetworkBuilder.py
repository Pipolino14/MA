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

    #Diese Mutation macht eine random Matrix und addiert diese zur vorherigen Matrix.
    #Problem: Diese Funktion addiert nur und mit der Zeit werden alle Weights/Biases in Richtung 1 gehen.
    def mutateNetwork_1(self, inputNetwork):
        rngweights = [np.random.randn(5, 4), np.random.randn(4, 2)]
        rngbiases = [np.random.randn(4), np.random.randn(2)]
        newweights = [np.add(inputNetwork.weights[0] , rngweights[0]) , np.add(inputNetwork.weights[1] , rngweights[1])]
        newbiases = [np.add(inputNetwork.biases[0] , rngbiases[0]) , np.add(inputNetwork.biases[1] , rngbiases[1])]
        outputNetwork = Network(newweights, newbiases)
        return outputNetwork
    
    #Diese Mutation nimmt alle Elemente der Matrix und shuffelt sich ganz wirr durcheinander.
    #Problem: es shuffelt alle nummern (wie in mutateNetwork_1) und nicht nur einzelne.
    def mutateNetwork_2(self, inputNetwork):
        newweights = [np.random.permutation(inputNetwork.weights[0]) , np.random.permutation(inputNetwork.weights[1])]
        newbiases = [np.random.permutation(inputNetwork.biases[0]) , np.random.permutation(inputNetwork.biases[1])]
        outputNetwork = Network(newweights, newbiases)
        return outputNetwork
    
    
    #Diese Mutation wirkt ähnlich, wie die erste Mutationsfunktion mit einem kleinem unterschied.
    # 1. Sie kreiert zuerst eine Matrix mit Elementen von -0.1 bis 0.1.
    # 2. Dann Kreiert sie eine Matrix mit Elementen -1, 0 und 1
    # 3. Sie Kreiert dann nochmals eine Matrix mit nur 0 und 1 und Multipliziert diese mit der Matrix in Schritt 2.
    # 4. Die Multipliziert diese Matrix nun mit der ersten matrix, sodass nur wenige Werte mit der schlussendlichen Matrix multipliziert werden.
    # Der Grund warum ich Schritt 3 gemacht habe ist, dass die wahrscheinlichkeit einer Änderung der Zahl bei 2/3 liegt. Das finde ich zu hoch.
    # Mit Schritt 3 ist diese Wahrscheinlichkeit der Änderung 1/3 und ich kann diese auch wiederholen.
    def mutateNetwork_3(self, inputNetwork):
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

        #Jetzt multipliziere ich die rng matrizen mit den random Matrizen, dass nun nur in spezifischen orten ein wechsel stattgefunden hat und dieser nur leicht Positiv, sowie auch nur leicht negativ sein kann.
        selWeights1 = mutWeights_1 * Weights_1_rng
        selWeights2 = mutWeights_2 * Weights_2_rng
        selBiases1 = mutBiases_1 * Biases_1_rng
        selBiases2 = mutBiases_2 * Biases_2_rng
        
        #Jetzt adiere ich diese leiche Änderungen zur inputMatrix und returne diese danach. 
        newweights = [np.add(inputNetwork.weights[0] , selWeights1) , np.add(inputNetwork.weights[1] , selWeights2)]
        newbiases = [np.add(inputNetwork.biases[0] , selBiases1) , np.add(inputNetwork.biases[1] , selBiases2)]

        outputNetwork = Network(newweights, newbiases)
        return outputNetwork
    
