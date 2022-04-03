from random import randint, random
from time import time

import numpy as np
import matplotlib.pyplot as plt

from classic_EA.population import Population


class ClassicEA:
    def __init__(self, **kwargs):
        self.number_of_population = int(kwargs.get('numberOfPopulation'))
        self.length_of_chromosome = int(kwargs.get('lengthOfChromosome'))
        self.epochs = int(kwargs.get('epochs'))
        self.cross_probability = float(kwargs.get('crossProbability'))
        self.mutation_probability = float(kwargs.get('mutationProbability'))
        self.inversion_probability = float(kwargs.get('inversionProbability'))
        self.selection_percent = float(kwargs.get('selectionPercent'))
        self.elitist_strategy_percent = float(kwargs.get('elitistStrategyPercent'))
        self.size_of_tournament = int(kwargs.get('sizeOfTournament'))
        self.selection_name = kwargs.get('selectionName')
        self.crossover_name = kwargs.get('crossoverName')
        self.mutation_name = kwargs.get('mutationName')
        self.population = Population(self.number_of_population, self.length_of_chromosome)

    def elitist_strategy(self, new_population):
        self.population.individuals += self.population.elitist_strategy_individuals
        self.population.individuals.sort(key=lambda x: x.fitness_function())
        new_population.elitist_strategy_individuals = self.population.individuals[
                                                      :int(self.elitist_strategy_percent * self.number_of_population)]
        new_population.individuals += self.population.individuals[
                                      :int(self.elitist_strategy_percent * self.number_of_population)]
        return new_population

    def selection_best(self, new_population):
        self.population.individuals.sort(key=lambda x: x.fitness_function())
        new_population.individuals += self.population.individuals[
                                      :int(self.selection_percent * self.number_of_population)]
        return new_population

    def selection_roulette(self, new_population):
        fitness_functions_sum = 0
        for individual in self.population.individuals:
            fitness_functions_sum += 1.0 / individual.fitness_function()
        probabilities = []
        for individual in self.population.individuals:
            probabilities.append(1.0 / individual.fitness_function() / fitness_functions_sum)
        while len(new_population.individuals) + len(
                new_population.elitist_strategy_individuals) < self.number_of_population * self.selection_percent:
            rand = random()
            probabilities_sum = 0.0
            for individual in self.population.individuals:
                probabilities_sum += 1.0 / individual.fitness_function()
                if rand < probabilities_sum:
                    new_population.individuals += individual
                    break

        return new_population

    def selection_tournament(self, new_population):
        individuals_copy = self.population.individuals[:]
        while len(individuals_copy) >= self.size_of_tournament:
            individuals_group = []
            for i in range(self.size_of_tournament):
                individual = randint(0, len(individuals_copy) - 1)
                individuals_group.append(individuals_copy[individual])
                del individuals_copy[individual]
            individuals = [individual_element.fitness_function() for individual_element in individuals_group]
            index_min = min(range(len(individuals)), key=individuals.__getitem__)
            new_population.individuals.append(individuals_group[index_min])
        return new_population

    def crossover_one_point(self, new_population):
        self.population.individuals = new_population.individuals[:]
        while len(self.population.individuals) < self.number_of_population:
            i = randint(0, len(new_population.individuals) - 1)
            rand = random()
            if rand < self.cross_probability:
                j = randint(0, len(new_population.individuals) - 1)
                cross = np.random.randint(self.length_of_chromosome - 1, size=2)
                self.population.cross_one_point(new_population.individuals[i], new_population.individuals[j], cross)
            else:
                self.population.individuals.append(new_population.individuals[i])

    def crossover_two_points(self, new_population):
        self.population.individuals = new_population.individuals[:]
        while len(self.population.individuals) < self.number_of_population:
            i = randint(0, len(new_population.individuals) - 1)
            rand = random()
            if rand < self.cross_probability:
                j = randint(0, len(new_population.individuals) - 1)
                cross = np.random.randint(self.length_of_chromosome - 1, size=(2, 2))
                self.population.cross_two_points(new_population.individuals[i], new_population.individuals[j], cross)
            else:
                self.population.individuals.append(new_population.individuals[i])

    def crossover_three_points(self, new_population):
        self.population.individuals = new_population.individuals[:]
        while len(self.population.individuals) < self.number_of_population:
            i = randint(0, len(new_population.individuals) - 1)
            rand = random()
            if rand < self.cross_probability:
                j = randint(0, len(new_population.individuals) - 1)
                cross = np.random.randint(self.length_of_chromosome - 1, size=(2, 3))
                self.population.cross_three_points(new_population.individuals[i], new_population.individuals[j], cross)
            else:
                self.population.individuals.append(new_population.individuals[i])

    def crossover_uniform(self, new_population):
        self.population.individuals = new_population.individuals[:]
        while len(self.population.individuals) < self.number_of_population:
            i = randint(0, len(new_population.individuals) - 1)
            rand = random()
            if rand < self.cross_probability:
                j = randint(0, len(new_population.individuals) - 1)
                self.population.cross_uniform(new_population.individuals[i], new_population.individuals[j])
            else:
                self.population.individuals.append(new_population.individuals[i])

    def mutation_edge(self):
        for individual in self.population.individuals:
            rand = random()
            if rand < self.mutation_probability:
                mutation = [self.length_of_chromosome - 1, self.length_of_chromosome - 1]
                individual.mutate(mutation)

    def mutation_one_point(self):
        for individual in self.population.individuals:
            rand = random()
            if rand < self.mutation_probability:
                mutation = np.random.randint(self.length_of_chromosome - 1, size=2)
                individual.mutate(mutation)

    def mutation_two_points(self):
        for individual in self.population.individuals:
            rand = random()
            if rand < self.mutation_probability:
                mutation = np.random.randint(self.length_of_chromosome - 1, size=(2, 2))
                individual.mutate_two_points(mutation)

    def inversion(self):
        for individual in self.population.individuals:
            rand = random()
            if rand < self.inversion_probability:
                inversion = np.random.randint(self.length_of_chromosome - 1, size=(2, 2))
                individual.inverse(inversion)

    def run(self):
        start = time()
        self.population.generate_individuals()
        bests = []
        for i in range(self.epochs):
            new_population = Population(self.number_of_population, self.length_of_chromosome)

            new_population = self.elitist_strategy(new_population)

            if self.selection_name == 'best':
                new_population = self.selection_best(new_population)
            elif self.selection_name == 'roulette':
                new_population = self.selection_roulette(new_population)
            elif self.selection_name == 'tournament':
                new_population = self.selection_tournament(new_population)

            if self.crossover_name == 'one_point':
                self.crossover_one_point(new_population)
            elif self.crossover_name == 'two_points':
                self.crossover_two_points(new_population)
            elif self.crossover_name == 'three_points':
                self.crossover_three_points(new_population)
            elif self.crossover_name == 'uniform':
                self.crossover_uniform(new_population)

            if self.mutation_name == 'edge':
                self.mutation_edge()
            elif self.mutation_name == 'one_point':
                self.mutation_one_point()
            elif self.mutation_name == 'two_points':
                self.mutation_two_points()

            self.inversion()
            bests.append(self.get_best())

        end = time()
        self.make_plots(bests)
        return end - start

    def get_best(self):
        self.population.individuals += self.population.elitist_strategy_individuals
        self.population.individuals.sort(key=lambda x: x.fitness_function())
        return self.population.individuals[0].fitness_function()

    def make_plots(self, bests):
        self.fitness_function_plot(bests)
        self.mean_plot(bests)
        self.deviation_plot(bests)

    def fitness_function_plot(self, bests):
        plt.figure()
        plt.xlabel('Epochs')
        plt.ylabel('Fitness function')
        plt.plot(range(len(bests)), bests)
        plt.title('Wartości funkcji od kolejnej iteracji')
        plt.show()

    def mean_plot(self, bests):
        pass

    def deviation_plot(self, bests):
        pass
