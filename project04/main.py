import random
import time

import pandas as pd
import multiprocessing
from deap import base
from deap import creator
from deap import tools
from sklearn import metrics
from sklearn import model_selection
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC

from plots import make_plots


def mutationSVC(individual):
    numberParamer = random.randint(0, len(individual) - 1)
    if numberParamer == 0:
        # kernel
        listKernel = ["linear", "rbf", "poly", "sigmoid"]
        individual[0] = listKernel[random.randint(0, 3)]
    elif numberParamer == 1:
        # C
        k = random.uniform(0.1, 100)
        individual[1] = k
    elif numberParamer == 2:
        # degree
        individual[2] = random.uniform(0.1, 5)
    elif numberParamer == 3:
        # gamma
        gamma = random.uniform(0.01, 1)
        individual[3] = gamma
    elif numberParamer == 4:
        # coeff
        coeff = random.uniform(0.1, 1)
        individual[2] = coeff
    else:  # genetyczna selekcja cech
        if individual[numberParamer] == 0:
            individual[numberParamer] = 1
        else:
            individual[numberParamer] = 0


def SVCParametersFitness(y, df, numberOfAtributtes, individual):
    split = 5
    cv = StratifiedKFold(n_splits=split)

    listColumnsToDrop = []  # lista cech do usuniecia
    for i in range(numberOfAtributtes, len(individual)):
        if individual[i] == 0:  # gdy atrybut ma zero to usuwamy cechę
            listColumnsToDrop.append(i - numberOfAtributtes)

    dfSelectedFeatures = df.drop(df.columns[listColumnsToDrop], axis=1, inplace=False)

    mms = MinMaxScaler()
    df_norm = mms.fit_transform(dfSelectedFeatures)
    estimator = SVC(kernel=individual[0], C=individual[1], degree=individual[2], gamma=individual[3],
                    coef0=individual[4], random_state=101)
    resultSum = 0
    for train, test in cv.split(df_norm, y):
        estimator.fit(df_norm[train], y[train])
        predicted = estimator.predict(df_norm[test])
        expected = y[test]
        tn, fp, fn, tp = metrics.confusion_matrix(expected, predicted).ravel()
        result = (tp + tn) / (
                tp + fp + tn + fn)  # w oparciu o macierze pomyłek
        # https://www.dataschool.io/simple-guide-to-confusion-matrix-terminology/
        resultSum = resultSum + result  # zbieramy wyniki z poszczególnych etapów walidacji krzyżowej

    return resultSum / split,


def SVCParameters(numberFeatures, icls):
    genome = list()

    # kernel
    listKernel = ["linear", "rbf", "poly", "sigmoid"]
    genome.append(listKernel[random.randint(0, 3)])

    # c
    k = random.uniform(0.1, 100)
    genome.append(k)

    # degree
    genome.append(random.uniform(0.1, 5))

    # gamma
    gamma = random.uniform(0.001, 5)
    genome.append(gamma)

    # coeff
    coeff = random.uniform(0.01, 10)
    genome.append(coeff)

    for _ in range(0, numberFeatures):
        genome.append(random.randint(0, 1))

    return icls(genome)


def main():
    pd.set_option('display.max_columns', None)
    # df = pd.read_csv("project04/data.csv", sep=';')  # for Visual Studio Code
    df = pd.read_csv("data.csv", sep=';')  # for PyCharm
    y = df['status']
    df.drop('status', axis=1, inplace=True)
    numberOfAtributtes = len(df.columns)
    print(numberOfAtributtes)

    mms = MinMaxScaler()
    df_norm = mms.fit_transform(df)
    clf = SVC()
    scores = model_selection.cross_val_score(clf, df_norm, y, cv=5, scoring='accuracy', n_jobs=-1)
    print(scores.mean())

    creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()

    # generowanie nowych osobników
    toolbox.register('individual', SVCParameters, numberOfAtributtes, creator.Individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # wskazanie funkcji celu
    toolbox.register("evaluate", SVCParametersFitness, y, df, numberOfAtributtes)

    # wybieranie algorytmu selekcji
    # toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("select", tools.selRandom)
    # toolbox.register("select", tools.selBest)
    # toolbox.register("select", tools.selWorst)
    # toolbox.register("select", tools.selRoulette)

    # krzyżowanie dla binarnej reprezentacji
    # toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mate", tools.cxUniform)
    # toolbox.register("mate", tools.cxTwoPoint)

    # definicja algorytmu mutacji
    toolbox.register("mutate", mutationSVC)

    # konfiguracja parametów algorytmu genetycznego
    sizePopulation = 100
    probabilityMutation = 0.6
    probabilityCrossover = 0.8
    numberIteration = 5  # <- było 300
    # generujemy początkową populację i obliczamy jej wartość funkcji dopasowania
    pop = toolbox.population(n=sizePopulation)

    # if __name__ == "__main__":
    #     pool = multiprocessing.Pool(processes=4)
    #     toolbox.register("map", pool.map)

    # fitnesses = toolbox.map(toolbox.evaluate, pop)
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # pętla genetyczna
    g = 0
    numberElitism = 1
    all_best_inds = []
    all_fits = []

    start_time = time.time()
    while g < numberIteration:
        g = g + 1
        print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        listElitism = []
        for x in range(0, numberElitism):
            listElitism.append(tools.selWorst(pop, 1)[0])

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < probabilityCrossover:
                toolbox.mate(child1, child2, probabilityCrossover)
                # toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            # mutate an individual with probability MUTPB
            if random.random() < probabilityMutation:
                # toolbox.mutate(mutant, probabilityMutation)
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        # fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
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
        best_ind = tools.selWorst(pop, 1)[0]
        all_best_inds.append(SVCParametersFitness(y, df, numberOfAtributtes, best_ind))
        all_fits.append(fits)
        print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

    print("-- End of (successful) evolution --")
    end_time = time.time()
    print(f'Evolution time: {end_time - start_time} [ms]')
    make_plots(all_best_inds, all_fits)


if __name__ == '__main__':
    main()
