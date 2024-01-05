import numpy as np

from Network import *
from Globals import *

class NetworkBuilder:
    def __init__(self, weights, biases):
        self.weights = weights
        self.biases = biases
        
    def buildNewNetwork(self):
        weights = [np.random.randn(5, 4), np.random.randn(4, 2)]
        biases = [np.random.randn(4), np.random.randn(2)]
        return weights, biases
    
    def crossoverWeights(self, N1weights, N2weights):
        # spalte die zwei Weight Layers von den Netzwerken auseinander
        N1weights_1 = N1weights[0]
        N1weights_2 = N1weights[1]
        N2weights_1 = N2weights[0]
        N2weights_2 = N2weights[1]

        # .shape findet unterschiedliche formen der Layers.
        # -->(Anz. Reihen, Anz. Spalten)
        weightsLane_1 = N1weights_1.shape
        weightsLane_2 = N1weights_2.shape

        # zufällig crossoverpoint auswählen in Anz.Reihen
        point_layer_1 = np.random.randint(1, weightsLane_1[1])
        point_layer_2 = np.random.randint(1, weightsLane_2[1])

        # crossover beider Matrizen der hidden Layer
        newWeightsN1_1 = np.hstack((N1weights_1[:, :point_layer_1], N2weights_1[:, point_layer_1:]))
        newWeightsN2_1 = np.hstack((N2weights_1[:, :point_layer_1], N1weights_1[:, point_layer_1:]))

        # crossover beider Matrizen der Output Layer
        newWeightsN1_2 = np.hstack((N1weights_2[:, :point_layer_2], N2weights_2[:, point_layer_2:]))
        newWeightsN2_2 = np.hstack((N2weights_2[:, :point_layer_2], N1weights_2[:, point_layer_2:]))

        newWeightsN1 = [newWeightsN1_1, newWeightsN1_2]
        newWeightsN2 = [newWeightsN2_1, newWeightsN2_2]

        return newWeightsN1, newWeightsN2
    
    def crossoverBiases(self, BiasesN1, BiasesN2):
        # das Gleiche Prinzip, wie bei crossoverWeights mit dem Unterschied, dass für Vektoren die funktion .concentrate() anstatt .hstackverwendet() werden muss.
        N1biases_1 = BiasesN1[0]
        N1biases_2 = BiasesN1[1]
        N2biases_1 = BiasesN2[0]
        N2biases_2 = BiasesN2[1]

        biasesLane_1 = N1biases_1.shape
        biasesLane_2 = N1biases_2.shape

        point_layer_1 = np.random.randint(1, biasesLane_1[1])
        point_layer_2 = np.random.randint(1, biasesLane_2[1])

        newBiasesN1_1 = np.concatenate((N1biases_1[:point_layer_1], N2biases_1[point_layer_1:]))
        newBiasesN2_1 = np.concatenate((N2biases_1[:point_layer_1], N1biases_1[point_layer_1:]))
        newBiasesN1_2 = np.concatenate((N1biases_2[:point_layer_2], N2biases_2[point_layer_2:]))
        newBiasesN2_2 = np.concatenate((N2biases_2[:point_layer_2], N1biases_2[point_layer_2:]))

        newBiasesN1 = [newBiasesN1_1, newBiasesN1_2]
        newBiasesN2 = [newBiasesN2_1, newBiasesN2_2]
            
        return newBiasesN1, newBiasesN2

    # Diese Mutation macht eine random Matrix und addiert diese zur vorherigen Matrix.
    # Problem: Diese Funktion addiert nur und mit der Zeit werden alle Weights/Biases in Richtung 1 gehen.
    # Diese verwende ich auch nicht in der Simulation, man kann dies aber auch ändern --> Main.py
    def mutateNetwork_1(self, inputNetwork):
        rngweights = [np.random.randn(5, 4), np.random.randn(4, 2)]
        rngbiases = [np.random.randn(4), np.random.randn(2)]
        newweights = [np.add(inputNetwork.weights[0] , rngweights[0]) , np.add(inputNetwork.weights[1] , rngweights[1])]
        newbiases = [np.add(inputNetwork.biases[0] , rngbiases[0]) , np.add(inputNetwork.biases[1] , rngbiases[1])]
        outputNetwork = Network(newweights, newbiases)
        return outputNetwork
    
    # Diese Mutation nimmt alle Elemente der Matrix und shuffelt sich ganz wirr durcheinander.
    # Problem: es shuffelt alle nummern (wie in mutateNetwork_1) und nicht nur einzelne.
    # Diese verwende ich auch nicht in der Simulation, man kann dies aber auch ändern --> Main.py
    def mutateNetwork_2(self, inputNetwork):
        newweights = [np.random.permutation(inputNetwork.weights[0]) , np.random.permutation(inputNetwork.weights[1])]
        newbiases = [np.random.permutation(inputNetwork.biases[0]) , np.random.permutation(inputNetwork.biases[1])]
        outputNetwork = Network(newweights, newbiases)
        return outputNetwork
    
    
    #Diese Mutation wirkt ähnlich, wie die erste Mutationsfunktion mit einem kleinem unterschied.
    # 1.Sie kreiert eine Matrix mit dem Wert 0 oder 1 mir der globalen Wahrscheinlichkeit, dass 1 Gewählt wird --> einsen Definieren den Ort der Mutation
    # 2.Sie kreiert eine Neue Matrix mit random Werten von -0.1 bis 0.1 --> Definiert die stärke der Mutation und ob  sie positiv oder negativ ist
    # 3.Sie multipliziert diese beiden Matrizen und addiert sie schlussendlich zur Inputmatrix
    # Der Grund warum ich diese Funktion verwende ist, dass hier die Wahrscheinlichkeit einer Mutation eingestellt werden kann im gegensatz zu den anderen
    # und weil sie ausserdem nur kleine Teile der Matrix ändert, anstatt die Komplette Matrix zu ändern
    def mutateNetwork(self, inputNetwork):
        input_Weights_1 = inputNetwork.weights[0]
        input_Weights_2 = inputNetwork.weights[1]
        input_Biases_1 = inputNetwork.biases[0]
        input_Biases_2 = inputNetwork.biases[1]

        WeightSize_1 = input_Weights_1.shape
        WeightSize_2 = input_Weights_2.shape
        BiasSize_1 = input_Biases_1.shape
        BiasSize_2 = input_Biases_2.shape

        # Übernehme die Wahrscheinlichkeit und Stärke einer Mutation von den Globals
        mutProb = [1 - Globals.MutProbability, Globals.MutProbability]
        Strength = Globals.MutStrength

        # 1.Generiere gleichgrosse Matrizen mit Werten 0 oder 1, wobei die
        # Wahrscheinlichkeit mutProb die Wahrscheinlichkeit für die Nummern beschreibt
        Weights_1_rng = np.random.choice((0, 1), p=mutProb, size=WeightSize_1)
        Weights_2_rng = np.random.choice((0, 1), p=mutProb, size=WeightSize_2)
        Biases_1_rng = np.random.choice((0, 1), p=mutProb, size=BiasSize_1)
        Biases_2_rng = np.random.choice((0, 1), p=mutProb, size=BiasSize_2)

        # 2.Generiere neue gleichgrosse Matrizen mit zufälligen Werten zwischen -0.1 und 0.1
        mutWeights_1 = np.random.uniform(low=-Strength, high=Strength, size=WeightSize_1) 
        mutWeights_2 = np.random.uniform(low=-Strength, high=Strength, size=WeightSize_2)
        mutBiases_1 = np.random.uniform(low=-Strength, high=Strength, size=BiasSize_1)
        mutBiases_2 = np.random.uniform(low=-Strength, high=Strength, size=BiasSize_2)

        # 3.Multipliziere die beiden vorherigen Matrizen miteinander
        selWeights1 = mutWeights_1 * Weights_1_rng
        selWeights2 = mutWeights_2 * Weights_2_rng
        selBiases1 = mutBiases_1 * Biases_1_rng
        selBiases2 = mutBiases_2 * Biases_2_rng
        
        # 4.Addiere diese neuen Matrizen zu den weights und biases des input-Netzwerks
        newweights = [np.add(input_Weights_1 , selWeights1) , np.add(input_Weights_2 , selWeights2)]
        newbiases = [np.add(input_Biases_1, selBiases1) , np.add(input_Biases_2, selBiases2)]

        outputNetwork = Network(newweights, newbiases)
        return outputNetwork
    
