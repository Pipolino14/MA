import numpy as np

# Fitness-Funktion, die evaluiert werden soll (kann je nach Modell angepasst werden)
def fitness_function(parameters):
    # Hier sollte das Räuber-Beute-Modell simuliert und die Fitness bewertet werden
    # Zum Beispiel: Rückgabe der Anzahl der Überlebenden Beutetiere nach einer bestimmten Anzahl von Schritten
    pass

# Genetischer Algorithmus
def genetic_algorithm(population_size, num_generations, mutation_rate):
    # Initialisierung der Population mit zufälligen Parametern
    population = np.random.rand(population_size, num_parameters)

    for generation in range(num_generations):
        # Bewertung der Fitness für jeden Satz von Parametern in der Population
        fitness_scores = np.array([fitness_function(params) for params in population])

        # Selektion basierend auf Fitness
        selected_indices = np.argsort(fitness_scores)[-int(0.5 * population_size):]
        selected_population = population[selected_indices]

        # Kreuzung (Crossover) - Erzeugung neuer Individuen durch Kombination von Parametern der ausgewählten Individuen
        crossover_indices = np.random.choice(selected_population.shape[0], size=population_size - selected_population.shape[0])
        crossover_population = np.array([selected_population[np.random.choice(selected_population.shape[0], size=2)] for _ in range(crossover_indices.size)])

        # Mutation - Zufällige Veränderung von Parametern
        mutation_mask = np.random.rand(*crossover_population.shape) < mutation_rate
        mutation_values = np.random.rand(*crossover_population.shape)
        crossover_population[mutation_mask] = mutation_values[mutation_mask]

        # Neue Population zusammenstellen
        population[:selected_population.shape[0]] = selected_population
        population[selected_population.shape[0]:] = crossover_population

    # Die besten Parameter auswählen
    best_params = population[np.argmax(fitness_scores)]
    
    return best_params

# Beispielaufruf des genetischen Algorithmus
num_parameters = 3  # Anzahl der zu optimierenden Parameter
best_parameters = genetic_algorithm(population_size=100, num_generations=50, mutation_rate=0.1)

print("Beste Parameter:", best_parameters)
print("Beste Fitness:", fitness_function(best_parameters))
