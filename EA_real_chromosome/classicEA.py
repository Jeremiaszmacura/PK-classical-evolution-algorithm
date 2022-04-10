from random import randint, random
from time import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from EA_real_chromosome.population import Population


def make_plots(bests, individuals):
    bests = np.array(bests)
    individuals = np.array(individuals)
    fitness_function_plot(bests)
    mean_plot(individuals)
    deviation_plot(individuals)
    df = pd.DataFrame(individuals)
    filepath = 'data.xlsx'
    df.to_excel(filepath, index=False)


def fitness_function_plot(bests):
    plt.figure()
    plt.xlabel('Epochs')
    plt.ylabel('Fitness function')
    plt.plot(range(len(bests)), bests)
    plt.title('Wartości funkcji najlepszego osobnika od kolejnej iteracji')
    plt.show()


def mean_plot(individuals):
    means = []
    for epoch in individuals:
        means.append(np.mean(epoch))
    plt.figure()
    plt.xlabel('Epochs')
    plt.ylabel('Mean')
    plt.plot(range(len(means)), means)
    plt.title('Średnia wartość funkcji osobników od kolejnej iteracji')
    plt.show()


def deviation_plot(individuals):
    deviations = []
    for epoch in individuals:
        deviations.append(np.std(epoch))
    plt.figure()
    plt.xlabel('Epochs')
    plt.ylabel('Standard deviation')
    plt.plot(range(len(deviations)), deviations)
    plt.title('Odchylenie standardowe funkcji osobników od kolejnej iteracji')
    plt.show()


class ClassicEA:
    def __init__(self, **kwargs):
        self.number_of_population = int(kwargs.get('numberOfPopulation'))
        self.epochs = int(kwargs.get('epochs'))
        self.cross_probability = float(kwargs.get('crossProbability'))
        self.mutation_probability = float(kwargs.get('mutationProbability'))
        self.selection_percent = float(kwargs.get('selectionPercent'))
        self.elitist_strategy_percent = float(kwargs.get('elitistStrategyPercent'))
        self.size_of_tournament = int(kwargs.get('sizeOfTournament'))
        self.selection_name = kwargs.get('selectionName')
        self.crossover_name = kwargs.get('crossoverName')
        self.mutation_name = kwargs.get('mutationName')
        self.population = Population(self.number_of_population)

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
                    new_population.individuals.append(individual)
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

    def crossover_arithmetic(self, new_population):
        self.population.add_individuals(new_population.individuals)
        while len(self.population.individuals) < self.number_of_population:
            i = randint(0, len(new_population.individuals) - 1)
            rand = random()
            if rand < self.cross_probability:
                j = randint(0, len(new_population.individuals) - 1)
                k = random()
                if k == 0.0:
                    k = 0.5
                self.population.cross_arithmetic(new_population.individuals[i], new_population.individuals[j], k)
            else:
                self.population.add_individuals(new_population.individuals[i])

    def crossover_linear(self, new_population):
        self.population.add_individuals(new_population.individuals)
        while len(self.population.individuals) < self.number_of_population:
            i = randint(0, len(new_population.individuals) - 1)
            rand = random()
            if rand < self.cross_probability:
                j = randint(0, len(new_population.individuals) - 1)
                self.population.cross_linear(new_population.individuals[i], new_population.individuals[j])
            else:
                self.population.add_individuals(new_population.individuals[i])

    def crossover_blend_alpha(self, new_population):
        self.population.add_individuals(new_population.individuals)
        while len(self.population.individuals) < self.number_of_population:
            i = randint(0, len(new_population.individuals) - 1)
            rand = random()
            if rand < self.cross_probability:
                j = randint(0, len(new_population.individuals) - 1)
            #     cross = np.random.randint(self.length_of_chromosome - 1, size=(2, 3))
            #     self.population.cross_three_points(new_population.individuals[i], new_population.individuals[j], cross)
            else:
                self.population.add_individuals(new_population.individuals[i])

    def crossover_average(self, new_population):
        self.population.add_individuals(new_population.individuals)
        while len(self.population.individuals) < self.number_of_population:
            i = randint(0, len(new_population.individuals) - 1)
            rand = random()
            if rand < self.cross_probability:
                j = randint(0, len(new_population.individuals) - 1)
                self.population.cross_average(new_population.individuals[i], new_population.individuals[j], cross)
            else:
                self.population.add_individuals(new_population.individuals[i])

    def crossover_blend_alpha_beta(self, new_population):
        self.population.add_individuals(new_population.individuals)
        while len(self.population.individuals) < self.number_of_population:
            i = randint(0, len(new_population.individuals) - 1)
            rand = random()
            if rand < self.cross_probability:
                j = randint(0, len(new_population.individuals) - 1)
            #     self.population.cross_uniform(new_population.individuals[i], new_population.individuals[j])
            else:
                self.population.add_individuals(new_population.individuals[i])

    def mutation_uniform(self):
        for individual in self.population.individuals:
            rand = random()
            # if rand < self.mutation_probability:
            #     mutation = [self.length_of_chromosome - 1, self.length_of_chromosome - 1]
            #     individual.mutate(mutation)

    def mutation_gauss(self):
        for individual in self.population.individuals:
            rand = random()
            # if rand < self.mutation_probability:
            #     mutation = np.random.randint(self.length_of_chromosome - 1, size=2)
            #     individual.mutate(mutation)

    def run(self):
        self.population.generate_individuals()
        bests = []
        individuals = []
        start = time()

        for i in range(self.epochs):
            new_population = Population(self.number_of_population)

            new_population = self.elitist_strategy(new_population)

            if self.selection_name == 'best':
                new_population = self.selection_best(new_population)
            elif self.selection_name == 'roulette':
                new_population = self.selection_roulette(new_population)
            elif self.selection_name == 'tournament':
                new_population = self.selection_tournament(new_population)

            if self.crossover_name == 'arithmetic':
                self.crossover_arithmetic(new_population)
            elif self.crossover_name == 'linear':
                self.crossover_linear(new_population)
            elif self.crossover_name == 'beta_alpha':
                self.crossover_blend_alpha(new_population)
            elif self.crossover_name == 'blend_alpha_beta':
                self.crossover_blend_alpha_beta(new_population)
            elif self.crossover_name == 'average':
                self.crossover_average(new_population)

            if self.mutation_name == 'uniform':
                self.mutation_uniform()
            elif self.mutation_name == 'gauss':
                self.mutation_gauss()

            bests.append(self.get_best())
            individuals.append(self.get_all_individuals())
            # TODO po krzyżowaniu i mutacji sprawdzić zakres (-40;40) i ewentualnie poprawić

        end = time()
        self.population.show_population()
        make_plots(bests, individuals)
        return end - start

    def get_best(self):
        self.population.individuals += self.population.elitist_strategy_individuals
        self.population.individuals.sort(key=lambda x: x.fitness_function())
        return self.population.individuals[0].fitness_function()

    def get_all_individuals(self):
        self.population.individuals += self.population.elitist_strategy_individuals
        self.population.individuals.sort(key=lambda x: x.fitness_function())
        return [individual.fitness_function() for individual in self.population.individuals]
