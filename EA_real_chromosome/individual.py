from math import exp, sqrt, cos, pi

from numpy import random


class Individual:
    def __init__(self):
        self.a = -40
        self.b = 40
        self.chromosomes = random.rand(2) * (self.b - self.a) + self.a

    def fitness_function(self):
        return -20 * exp(-0.2 * sqrt(0.5 * (self.chromosomes[0] ** 2 + self.chromosomes[1] ** 2))) - exp(
            0.5 * (cos(2 * pi * self.chromosomes[0]) + cos(2 * pi * self.chromosomes[1]))) + 20 + exp(1)

    def check_boundaries(self):
        for i in self.chromosomes:
            if self.chromosomes[i] < self.a:
                self.chromosomes[i] = self.a
            elif self.chromosomes[i] > self.b:
                self.chromosomes[i] = self.b
