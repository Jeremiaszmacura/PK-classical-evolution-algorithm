import random
import time

import pandas as pd
from deap import base
from deap import creator
from deap import tools
from sklearn import model_selection
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.svm import SVC
from sklearn.svm import SVC

from SVC_classifier import mutationSVC, SVCParametersFitness, SVCParameters
from KNeighborsClassifier_classifier import mutationKNeighborsClassifier, KNeighborsClassifierParametersFitness,\
    KNeighborsClassifierParameters
from MLPClassifier_classifier import mutationMLPClassifier, MLPClassifierParametersFitness, MLPClassifierParameters
from GaussianProcessClassifier_classifier import mutationGaussianProcessClassifier,\
    GaussianProcessClassifierParametersFitness, GaussianProcessClassifierParameters
from SVC_classifier import mutationSVC, SVCParametersFitness, SVCParameters
from SVC_classifier import mutationSVC, SVCParametersFitness, SVCParameters
from plots import make_plots


def main():
    pd.set_option('display.max_columns', None)
    # df = pd.read_csv("project04/data.csv", sep=';')  # for Visual Studio Code
    df = pd.read_csv("data.csv", sep=';')  # for PyCharm
    y = df['status']
    df.drop('status', axis=1, inplace=True)
    numberOfAtributtes = len(df.columns)

    mms = MinMaxScaler()
    df_norm = mms.fit_transform(df)
    # -----------classifier-1-------------------------------
    # clf = SVC()
    # clf = KNeighborsClassifier()
    # clf = MLPClassifier()
    clf = GaussianProcessClassifier()
    # clf = SVC()
    # clf = SVC()

    # -----------classifier-1-------------------------------
    scores = model_selection.cross_val_score(clf, df_norm, y, cv=5, scoring='accuracy', n_jobs=-1)
    print(scores.mean())

    creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()

    # generowanie nowych osobników
    # -----------classifier-2-------------------------------
    # toolbox.register('individual', SVCParameters, numberOfAtributtes, creator.Individual)
    # toolbox.register('individual', KNeighborsClassifierParameters, numberOfAtributtes, creator.Individual)
    # toolbox.register('individual', MLPClassifierParameters, numberOfAtributtes, creator.Individual)
    toolbox.register('individual', GaussianProcessClassifierParameters, numberOfAtributtes, creator.Individual)
    # toolbox.register('individual', SVCParameters, numberOfAtributtes, creator.Individual)
    # toolbox.register('individual', SVCParameters, numberOfAtributtes, creator.Individual)
    # -----------classifier-2-------------------------------
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # wskazanie funkcji celu
    # -----------classifier-3-------------------------------
    # toolbox.register("evaluate", SVCParametersFitness, y, df, numberOfAtributtes)
    # toolbox.register("evaluate", KNeighborsClassifierParametersFitness, y, df, numberOfAtributtes)
    # toolbox.register("evaluate", MLPClassifierParametersFitness, y, df, numberOfAtributtes)
    toolbox.register("evaluate", GaussianProcessClassifierParametersFitness, y, df, numberOfAtributtes)
    # toolbox.register("evaluate", SVCParametersFitness, y, df, numberOfAtributtes)
    # toolbox.register("evaluate", SVCParametersFitness, y, df, numberOfAtributtes)
    # -----------classifier-3-------------------------------

    # wybieranie algorytmu selekcji
    # toolbox.register("select", tools.selTournament, tournsize=3)
    # toolbox.register("select", tools.selRandom)
    # toolbox.register("select", tools.selBest)
    # toolbox.register("select", tools.selWorst)
    toolbox.register("select", tools.selRoulette)

    # krzyżowanie dla binarnej reprezentacji
    # toolbox.register("mate", tools.cxOnePoint)
    # toolbox.register("mate", tools.cxUniform)
    toolbox.register("mate", tools.cxTwoPoint)

    # definicja algorytmu mutacji
    # -----------classifier-4-------------------------------
    # toolbox.register("mutate", mutationSVC)
    # toolbox.register("mutate", mutationKNeighborsClassifier)
    # toolbox.register("mutate", mutationMLPClassifier)
    toolbox.register("mutate", mutationGaussianProcessClassifier)
    # toolbox.register("mutate", mutationSVC)
    # toolbox.register("mutate", mutationSVC)
    # -----------classifier-4-------------------------------

    # konfiguracja parametów algorytmu genetycznego
    sizePopulation = 100
    probabilityMutation = 0.6
    probabilityCrossover = 0.8
    numberIteration = 10  # <- było 300
    # generujemy początkową populację i obliczamy jej wartość funkcji dopasowania
    pop = toolbox.population(n=sizePopulation)

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
                # toolbox.mate(child1, child2, probabilityCrossover)
                toolbox.mate(child1, child2)

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
        # -----------classifier-5-------------------------------
        # all_best_inds.append(SVCParametersFitness(y, df, numberOfAtributtes, best_ind))
        # all_best_inds.append(KNeighborsClassifierParametersFitness(y, df, numberOfAtributtes, best_ind))
        # all_best_inds.append(MLPClassifierParametersFitness(y, df, numberOfAtributtes, best_ind))
        all_best_inds.append(GaussianProcessClassifierParametersFitness(y, df, numberOfAtributtes, best_ind))
        # all_best_inds.append(SVCParametersFitness(y, df, numberOfAtributtes, best_ind))
        # all_best_inds.append(SVCParametersFitness(y, df, numberOfAtributtes, best_ind))
        # -----------classifier-5-------------------------------
        all_fits.append(fits)
        print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

    print("-- End of (successful) evolution --")
    end_time = time.time()
    print(f'Evolution time: {end_time - start_time} [ms]')
    make_plots(all_best_inds, all_fits)


if __name__ == '__main__':
    main()
