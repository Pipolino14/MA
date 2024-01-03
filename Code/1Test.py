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

# Define the two numbers and their respective probabilities
numbers = [0, 1]  # Replace these with your desired numbers
probabilities = [0.9, 0.1]  # Replace these with your desired probabilities

# Generate a random matrix with specified probabilities
matrix_size = (4, 5)  # Replace this with your desired matrix size
random_matrix = np.random.choice(numbers, size=matrix_size, p=probabilities)

print(random_matrix)

