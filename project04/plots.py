import matplotlib.pyplot as plt
import numpy as np


def make_plots(bests, individuals):
    bests = np.array(bests)
    individuals = np.array(individuals)
    fitness_function_plot(bests)
    mean_plot(individuals)
    deviation_plot(individuals)


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
