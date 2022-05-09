from random import randint


class Gene:
    def __init__(self):
        self.allel = randint(0, 1)

    def get_allel(self):
        return self.allel

    def inverse(self):
        self.allel = 0 if self.allel else 1
