import numpy as np

class YourGeneticAlgorithm:
    def crossover(self, N1weights, N2weights, N3weights, N4weights):
        # mit .shape finde ich die Formen heraus [5] und [5]
        weightsCol = N1weights.shape[0]

        # hier wählt es zufällig einen Punkt aus, um das Crossover zu machen
        crossoverPoint = np.random.randint(1, weightsCol)

        # hier addiert es den ersten Teil der ersten Matrix mit dem anderen der 2. und das gleiche auch noch umgekehrt --> Crossover wird hier durchgeführt
        newWeightsN1 = np.concatenate((N1weights[:crossoverPoint], N2weights[crossoverPoint:]))
        newWeightsN2 = np.concatenate((N2weights[:crossoverPoint], N1weights[crossoverPoint:]))
        newWeightsN3 = np.concatenate((N3weights[:crossoverPoint], N4weights[crossoverPoint:]))
        newWeightsN4 = np.concatenate((N4weights[:crossoverPoint], N3weights[crossoverPoint:]))

        return newWeightsN1, newWeightsN2, newWeightsN3, newWeightsN4

# Beispielaufruf
genetic_algo = YourGeneticAlgorithm()

# Beispielvektoren mit Float-Nummern
N1weights = np.random.rand(5)
N2weights = np.random.rand(5)
N3weights = np.random.rand(5)
N4weights = np.random.rand(5)

# Führe das Crossover durch
newWeightsN1, newWeightsN2, newWeightsN3, newWeightsN4 = genetic_algo.crossover(N1weights, N2weights, N3weights, N4weights)

# Ausgabe der neuen Vektoren nach dem Crossover
print("Neue Weights für Vektor 1:")
print(N1weights)
print(newWeightsN1)

print("\nNeue Weights für Vektor 2:")
print(newWeightsN2)

print("\nNeue Weights für Vektor 3:")
print(newWeightsN3)

print("\nNeue Weights für Vektor 4:")
print(newWeightsN4)
