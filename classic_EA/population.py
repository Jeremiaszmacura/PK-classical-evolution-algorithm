from classic_EA.individual import Individual


class Population:
    def __init__(self, a, b, number_of_population, length_of_chromosome):
        self.a = a
        self.b = b
        self.number_of_population = number_of_population
        self.length_of_chromosome = length_of_chromosome
        self.individuals = []
        self.elitist_strategy_individuals = []

    def generate_individuals(self):
        self.individuals = []
        [self.individuals.append(Individual(self.a, self.b, self.length_of_chromosome)) for _ in
         range(self.number_of_population)]

    def show_population(self):
        print('--------------------------')
        print('|Chromosomes|')
        print('--------------------------')
        [print(individual.get_chromosomes()) for individual in self.individuals]
        print('--------------------------')
        print('|Decimals|')
        print('--------------------------')
        [print(individual.get_decimals()) for individual in self.individuals]
        print('--------------------------')
        print('|Fitness Function|')
        print('--------------------------')
        [print(individual.fitness_function()) for individual in self.individuals]

    def cross_one_point(self, ind1, ind2, cross):
        individual1 = Individual(self.a, self.b, self.length_of_chromosome)
        individual2 = Individual(self.a, self.b, self.length_of_chromosome)
        individual1.cross_one_point(ind1, ind2, cross, True)
        individual2.cross_one_point(ind1, ind2, cross, False)
        self.individuals.append(individual1)
        if len(self.individuals) < self.number_of_population:
            self.individuals.append(individual2)

    def cross_two_points(self, ind1, ind2, cross):
        individual1 = Individual(self.a, self.b, self.length_of_chromosome)
        individual2 = Individual(self.a, self.b, self.length_of_chromosome)
        individual1.cross_two_points(ind1, ind2, cross, True)
        individual2.cross_two_points(ind1, ind2, cross, False)
        self.individuals.append(individual1)
        if len(self.individuals) < self.number_of_population:
            self.individuals.append(individual2)

    def cross_three_points(self, ind1, ind2, cross):
        individual1 = Individual(self.a, self.b, self.length_of_chromosome)
        individual2 = Individual(self.a, self.b, self.length_of_chromosome)
        individual1.cross_three_points(ind1, ind2, cross, True)
        individual2.cross_three_points(ind1, ind2, cross, False)
        self.individuals.append(individual1)
        if len(self.individuals) < self.number_of_population:
            self.individuals.append(individual2)

    def cross_uniform(self, ind1, ind2):
        individual1 = Individual(self.a, self.b, self.length_of_chromosome)
        individual2 = Individual(self.a, self.b, self.length_of_chromosome)
        individual1.cross_uniform(ind1, ind2, True)
        individual2.cross_uniform(ind1, ind2, False)
        self.individuals.append(individual1)
        if len(self.individuals) < self.number_of_population:
            self.individuals.append(individual2)
