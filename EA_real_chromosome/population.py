import numpy as np

from EA_real_chromosome.individual import Individual


class Population:
    def __init__(self, number_of_population):
        self.number_of_population = number_of_population
        self.individuals = []
        self.elitist_strategy_individuals = []

    def generate_individuals(self):
        self.individuals = []
        [self.individuals.append(Individual()) for _ in range(self.number_of_population)]

    def show_population(self):
        print('--------------------------')
        print('|Chromosomes|')
        print('--------------------------')
        [print(individual.chromosomes) for individual in self.individuals]
        print('--------------------------')
        print('|Fitness Function|')
        print('--------------------------')
        [print(individual.fitness_function()) for individual in self.individuals]

    def add_individuals(self, individuals):
        for individual in individuals:
            new_individual = Individual()
            new_individual.chromosomes = np.copy(individual.chromosomes)
            self.individuals.append(new_individual)

    def cross_arithmetic(self, ind1, ind2, k):
        individual1 = Individual()
        individual2 = Individual()
        individual1.chromosomes = np.copy(np.array([k * ind1.chromosomes[0] + (1 - k) * ind2.chromosomes[0],
                                                    k * ind1.chromosomes[1] + (1 - k) * ind2.chromosomes[1]]))
        individual2.chromosomes = np.copy(np.array([(1 - k) * ind1.chromosomes[0] + k * ind2.chromosomes[0],
                                                    (1 - k) * ind1.chromosomes[1] + k * ind2.chromosomes[1]]))
        self.individuals.append(individual1)
        if len(self.individuals) < self.number_of_population:
            self.individuals.append(individual2)

    def cross_linear(self, ind1, ind2):
        individuals = []
        [individuals.append(Individual()) for _ in range(3)]
        individuals[0].chromosomes = np.copy(np.array([0.5 * ind1.chromosomes[0] + 0.5 * ind2.chromosomes[0],
                                                       0.5 * ind1.chromosomes[1] + 0.5 * ind2.chromosomes[1]]))
        individuals[1].chromosomes = np.copy(np.array([1.5 * ind1.chromosomes[0] - 0.5 * ind2.chromosomes[0],
                                                       1.5 * ind1.chromosomes[1] - 0.5 * ind2.chromosomes[1]]))
        individuals[2].chromosomes = np.copy(np.array([-0.5 * ind1.chromosomes[0] + 1.5 * ind2.chromosomes[0],
                                                       -0.5 * ind1.chromosomes[1] + 1.5 * ind2.chromosomes[1]]))
        individuals.sort(key=lambda ind: ind.fitness_function())
        self.individuals.append(individuals[0])
        if len(self.individuals) < self.number_of_population:
            self.individuals.append(individuals[1])
