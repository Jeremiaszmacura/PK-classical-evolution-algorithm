from classic_EA.gene import Gene


class Chromosome:
    def __init__(self, a, b, length_of_chromosome):
        self.a = a
        self.b = b
        self.length_of_chromosome = length_of_chromosome
        self.genes = self.generate_genes()
        self.decimal = self.binary_to_decimal()

    def generate_genes(self):
        genes = []
        [genes.append(Gene()) for _ in range(self.length_of_chromosome)]
        return genes

    def binary_to_decimal(self):
        decimal = 0.0
        for i in range(self.length_of_chromosome):
            decimal += 2 ** i * self.genes[-1 - i].get_allel()
        dx = (self.b - self.a) / (2 ** self.length_of_chromosome - 1)
        return self.a + decimal * dx

    def get_chromosome(self):
        return [gene.get_allel() for gene in self.genes]

    def get_decimal(self):
        return self.decimal

    def inverse(self, inversion):
        self.genes[inversion.min():inversion.max()].reverse()
