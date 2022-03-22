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

    def add_individual(self, ind1, ind2, cross):
        individual = Individual(self.a, self.b, self.length_of_chromosome)
        individual.cross(ind1, ind2, cross)
        self.individuals.append(individual)
