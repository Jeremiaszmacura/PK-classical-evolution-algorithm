from math import exp, sqrt, cos, pi

from classic_EA.chromosome import Chromosome


class Individual:
    def __init__(self, a, b, length_of_chromosome):
        self.a = a
        self.b = b
        self.length_of_chromosome = length_of_chromosome
        self.chromosomes = [Chromosome(self.a, self.b, self.length_of_chromosome),
                            Chromosome(self.a, self.b, self.length_of_chromosome)]

    def get_chromosomes(self):
        return [chromosome.get_chromosome() for chromosome in self.chromosomes]

    def get_decimals(self):
        return [chromosome.get_decimal() for chromosome in self.chromosomes]

    def fitness_function(self):
        return -20 * exp(
            -0.2 * sqrt(0.5 * (self.chromosomes[0].get_decimal() ** 2) + self.chromosomes[1].get_decimal() ** 2)) - exp(
            0.5 * (cos(2 * pi * self.chromosomes[0].get_decimal()) + cos(
                2 * pi * self.chromosomes[1].get_decimal()))) + 20 + exp(1)

    def cross(self, ind1, ind2, cross):
        for i in range(len(self.chromosomes)):
            self.chromosomes[i].genes[:(cross[i])] = ind1.chromosomes[i].genes[:(cross[i])]
            self.chromosomes[i].genes[(cross[i]):] = ind2.chromosomes[i].genes[(cross[i]):]

    def mutate(self, mutation):
        for i in range(len(self.chromosomes)):
            self.chromosomes[i].genes[mutation[i]].inverse()

    def inverse(self, inversion):
        for i in range(len(self.chromosomes)):
            self.chromosomes[i].inverse(inversion[i])
