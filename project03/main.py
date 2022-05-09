import random
from math import exp, sqrt, cos, pi

from deap import base
from deap import creator
from deap import tools


BOUNDARIES_UP = 10
BOUNDARIES_DOWN = -10


def check_boundaries(ind):
    for i in range(len(ind)):
        if ind[i] < BOUNDARIES_DOWN:
            ind[i] = BOUNDARIES_DOWN
        elif ind[i] > BOUNDARIES_UP:
            ind[i] = BOUNDARIES_UP
    return ind

def cross_blend_alpha(ind1, ind2):


def cross_linear(ind1, ind2):
    # k - prawdopodobieństwo krzyżowania
    k = 0.6
    ind1_tmp = [0.5 * ind1[0] + 0.5 * ind2[0], 0.5 * ind1[1] + 0.5 * ind2[1]]
    ind2_tmp = [1.5 * ind1[0] - 0.5 * ind2[0], 1.5 * ind1[1] - 0.5 * ind2[1]]
    ind3_tmp = [-0.5 * ind1[0] + 1.5 * ind2[0], -0.5 * ind1[1] + 1.5 * ind2[1]]

    # sprawdzamy czy są w zakresie
    ind1_tmp = check_boundaries(ind1_tmp)
    ind2_tmp = check_boundaries(ind2_tmp)
    ind3_tmp = check_boundaries(ind3_tmp)

    # porównanie - wstawiamy do fitness function
    result_ind1_tmp = fitnessFunction(ind1_tmp)
    result_ind2_tmp = fitnessFunction(ind2_tmp)
    result_ind3_tmp = fitnessFunction(ind3_tmp)

    # dwa najmniejsze z 3
    sorted_results = sorted([result_ind1_tmp, result_ind2_tmp, result_ind3_tmp])

    return sorted_results[0], sorted_results[1]

def cross_arithmetic(ind1, ind2):
    k = 0.6
    ind1_tmp = ind1
    ind2_tmp = ind2
    ind1[0] = k * ind1_tmp[0] + (1 - k) * ind2_tmp[0]
    ind1[1] = k * ind1_tmp[1] + (1 - k) * ind2_tmp[1]
    ind2[0] = (1 - k) * ind1_tmp[0] + k * ind2_tmp[0]
    ind2[1] = (1 - k) * ind1_tmp[1] + k * ind2_tmp[1]
    ind1 = check_boundaries(ind1)
    ind2 = check_boundaries(ind2)
    return ind1, ind2

# def individual(icls):
#     genome = list()
#     for x in range(0, 40):
#         genome.append(random.randint(0, 1))
#     return icls(genome)

def individual(icls):
    genome = list()
    genome.append(random.uniform(BOUNDARIES_DOWN, BOUNDARIES_UP))
    genome.append(random.uniform(BOUNDARIES_DOWN, BOUNDARIES_UP))
    return icls(genome)

def decodeInd(individual):
    individual_len = len(individual) // 2
    decoded_individual = []
    for i in range(2):
        s = 0
        for el in individual[i * individual_len: (i + 1) * individual_len]:
            s = s * 2 + el
        decoded_individual.append(s / (2 ** individual_len - 1))
    return decoded_individual

def fitnessFunction(individual):
    # tutaj rozkoduj binarnego osobnika! Napisz funkcje decodeInd
    # post binarna
    # ind = decodeInd(individual)
    # postac rzeczywista
    ind = individual
    # result = (ind[0] + 2 * ind[1] - 7) ** 2 + (2 * ind[0] + ind[1] - 5) ** 2
    result = -20 * exp(-0.2 * sqrt(0.5 * (ind[0] ** 2 + ind[1] ** 2))) - exp(
        0.5 * (cos(2 * pi * ind[0]) + cos(2 * pi * ind[1]))) + 20 + exp(1)
    return result,

def main():
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)
    toolbox = base.Toolbox()
    # generowanie nowych osobników
    toolbox.register('individual', individual, creator.Individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    # wskazanie funkcji celu
    toolbox.register("evaluate", fitnessFunction)
    # wybieranie algorytmu selekcji
    toolbox.register("select", tools.selTournament, tournsize=3)
    # toolbox.register("select", tools.selRandom, tournsize=3)
    # toolbox.register("select", tools.selBest, tournsize=3)
    # toolbox.register("select", tools.selWorst, tournsize=3)
    # toolbox.register("select", tools.selRoulette, tournsize=3)
    # wybieranie algorytmu krzyżowania
    toolbox.register("mate", cross_linear)
    # toolbox.register("mate", tools.cxOnePoint)
    # toolbox.register("mate", tools.cxUniform)
    # toolbox.register("mate", tools.cxTwoPoint)
    # definicja algorytmu mutacji
    # dla rzeczywistej reprezentacji
    toolbox.register("mutate", tools.mutGaussian, mu=5, sigma=10)
    # toolbox.register("mutate", tools.mutUniformInt, low=-40, up=40)
    # dla binarnej reprezentacji
    # toolbox.register("mutate", tools.mutFlipBit)
    # toolbox.register("mutate", tools.mutShuffleIndexes)
    # konfiguracja parametów algorytmu genetycznego
    sizePopulation = 100
    probabilityMutation = 0.2
    probabilityCrossover = 0.8
    numberIteration = 100
    # generujemy początkową populację i obliczamy jej wartość funkcji dopasowania
    pop = toolbox.population(n=sizePopulation)
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # pętla genetyczna
    g = 0
    numberElitism = 1
    while g < numberIteration:
        g = g + 1
        print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        listElitism = []
        for x in range(0, numberElitism):
            listElitism.append(tools.selBest(pop, 1)[0])

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < probabilityCrossover:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            # mutate an individual with probability MUTPB
            if random.random() < probabilityMutation:
                # toolbox.mutate(mutant, probabilityMutation)
                toolbox.mutate(mutant, indpb=probabilityMutation)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(invalid_ind))
        pop[:] = offspring + listElitism

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)
        print()
        best_ind = tools.selBest(pop, 1)[0]
        print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    #
    print("-- End of (successful) evolution --")


if __name__ == '__main__':
    main()
