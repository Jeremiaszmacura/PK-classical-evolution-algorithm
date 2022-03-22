from random import randint, random

import numpy as np

from classic_EA.population import Population


class ClassicEA:
    def __init__(self, a, b, number_of_population, length_of_chromosome, epochs, cross_probability,
                 mutation_probability, inversion_probability, selection_best_percent, elitist_strategy_percent):
        self.a = a
        self.b = b
        self.number_of_population = number_of_population
        self.length_of_chromosome = length_of_chromosome
        self.epochs = epochs
        self.cross_probability = cross_probability
        self.mutation_probability = mutation_probability
        self.inversion_probability = inversion_probability
        self.selection_best_percent = selection_best_percent
        self.elitist_strategy_percent = elitist_strategy_percent
        self.population = Population(self.a, self.b, self.number_of_population, self.length_of_chromosome)

    def elitist_strategy(self):
        self.population.individuals += self.population.elitist_strategy_individuals
        self.population.individuals.sort(key=lambda x: x.fitness_function())
        new_population = Population(self.a, self.b, self.number_of_population, self.length_of_chromosome)
        new_population.elitist_strategy_individuals = self.population.individuals[
                                                      :int(self.elitist_strategy_percent * self.number_of_population)]
        new_population.individuals = self.population.individuals[
                                     :int(self.elitist_strategy_percent * self.number_of_population)]
        return new_population

    def selection_best(self, new_population):
        self.population.individuals.sort(key=lambda x: x.fitness_function())
        if new_population.individuals:
            new_population.individuals += self.population.individuals[
                                          :int(self.selection_best_percent * self.number_of_population)]
        else:
            new_population.individuals = self.population.individuals[
                                         :int(self.selection_best_percent * self.number_of_population)]
        return new_population

    def selection_roulette(self):
        # TODO
        1

    def selection_tournament(self):
        # TODO
        1

    def crossover_one_point(self, new_population):
        self.population.individuals = new_population.individuals[:]
        while len(self.population.individuals) < self.number_of_population:
            i = randint(0, len(new_population.individuals) - 1)
            rand = random()
            if rand < self.cross_probability:
                j = randint(0, len(new_population.individuals) - 1)
                cross = np.random.randint(self.length_of_chromosome - 1, size=2)
                self.population.add_individual(new_population.individuals[i], new_population.individuals[j], cross)
            else:
                self.population.individuals.append(new_population.individuals[i])

    def crossover_two_points(self):
        # TODO
        1

    def crossover_three_points(self):
        # TODO
        1

    def crossover_uniform(self):
        # TODO
        1

    def mutation_edge(self):
        # TODO
        1

    def mutation_one_point(self):
        for individual in self.population.individuals:
            rand = random()
            if rand < self.mutation_probability:
                mutation = np.random.randint(self.length_of_chromosome - 1, size=2)
                individual.mutate(mutation)

    def mutation_two_points(self):
        # TODO
        1

    def inversion(self):
        for individual in self.population.individuals:
            rand = random()
            if rand < self.inversion_probability:
                inversion = np.random.randint(self.length_of_chromosome - 1, size=(2, 2))
                individual.inverse(inversion)

    def run(self):
        self.population.generate_individuals()
        for i in range(self.epochs):
            new_population = self.elitist_strategy()
            new_population = self.selection_best(new_population)
            self.crossover_one_point(new_population)
            self.mutation_one_point()
            self.inversion()
        self.population.show_population()
