# from functools import cache
# import time

# @cache
# def fibonacci(n):
#     if n == 1 or n == 2:
#         return 1
#     else:
#         return fibonacci(n-1) + fibonacci(n-2)

# start = time.time()
# print(fibonacci(500))
# end = time.time()

# print(end-start)

import numpy as np

a = [np.arange(20).reshape((5, 4)), np.arange(8).reshape((4, 2))]
b = [np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]), np.array([[0, 0], [0, 0], [0, 0], [0, 0]])]
# b = np.array([1, 1, 1, 1, 1])

# print(a)
# print(b)

# print(np.dot(b, a))

def crossoverWeights(N1weights, N2weights):
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

a, b = crossoverWeights(a, b)

print(a)