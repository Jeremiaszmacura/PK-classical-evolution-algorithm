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

    def cross_one_point(self, ind1, ind2, cross, left_cross):
        for i in range(len(self.chromosomes)):
            if left_cross:
                self.chromosomes[i].genes[:(cross[i])] = ind1.chromosomes[i].genes[:(cross[i])]
                self.chromosomes[i].genes[(cross[i]):] = ind2.chromosomes[i].genes[(cross[i]):]
            else:
                self.chromosomes[i].genes[:(cross[i])] = ind2.chromosomes[i].genes[:(cross[i])]
                self.chromosomes[i].genes[(cross[i]):] = ind1.chromosomes[i].genes[(cross[i]):]

    def cross_two_points(self, ind1, ind2, cross, center_cross):
        for i in range(len(self.chromosomes)):
            if center_cross:
                self.chromosomes[i].genes[:(cross[i].min())] = ind1.chromosomes[i].genes[:(cross[i].min())]
                self.chromosomes[i].genes[(cross[i].min()):(cross[i].max())] = ind2.chromosomes[i].genes[
                                                                               (cross[i].min()):(cross[i].max())]
                self.chromosomes[i].genes[(cross[i].max()):] = ind1.chromosomes[i].genes[(cross[i].max()):]
            else:
                self.chromosomes[i].genes[:(cross[i].min())] = ind2.chromosomes[i].genes[:(cross[i].min())]
                self.chromosomes[i].genes[(cross[i].min()):(cross[i].max())] = ind1.chromosomes[i].genes[
                                                                               (cross[i].min()):(cross[i].max())]
                self.chromosomes[i].genes[(cross[i].max()):] = ind2.chromosomes[i].genes[(cross[i].max()):]

    def cross_three_points(self, ind1, ind2, cross, left_cross):
        for i in range(len(self.chromosomes)):
            cross[i].sort()
            if left_cross:
                self.chromosomes[i].genes[:(cross[i][0])] = ind1.chromosomes[i].genes[:(cross[i][0])]
                self.chromosomes[i].genes[(cross[i][0]):(cross[i][1])] = ind2.chromosomes[i].genes[
                                                                         (cross[i][0]):(cross[i][1])]
                self.chromosomes[i].genes[(cross[i][1]):(cross[i][2])] = ind1.chromosomes[i].genes[
                                                                         (cross[i][1]):(cross[i][2])]
                self.chromosomes[i].genes[(cross[i][2]):] = ind2.chromosomes[i].genes[(cross[i][2]):]
            else:
                self.chromosomes[i].genes[:(cross[i][0])] = ind2.chromosomes[i].genes[:(cross[i][0])]
                self.chromosomes[i].genes[(cross[i][0]):(cross[i][1])] = ind1.chromosomes[i].genes[
                                                                         (cross[i][0]):(cross[i][1])]
                self.chromosomes[i].genes[(cross[i][1]):(cross[i][2])] = ind2.chromosomes[i].genes[
                                                                         (cross[i][1]):(cross[i][2])]
                self.chromosomes[i].genes[(cross[i][2]):] = ind1.chromosomes[i].genes[(cross[i][2]):]

    def mutate(self, mutation):
        for i in range(len(self.chromosomes)):
            self.chromosomes[i].genes[mutation[i]].inverse()

    def inverse(self, inversion):
        for i in range(len(self.chromosomes)):
            self.chromosomes[i].inverse(inversion[i])
