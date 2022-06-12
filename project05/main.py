import numpy as np
from mealpy.bio_based.IWO import OriginalIWO


def fitness_function(solution):
    return np.sum(solution ** 2)


problem_dict1 = {
    "fit_func": fitness_function,
    "lb": [-10, -15, -4, -2, -8],
    "ub": [10, 15, 12, 8, 20],
    "minmax": "min",
}
epoch = 1000
pop_size = 50
seeds = (3, 9)
exponent = 3
sigmas = (0.6, 0.01)
model = OriginalIWO(problem_dict1, epoch, pop_size, seeds, exponent, sigmas)
best_position, best_fitness = model.solve()
print(f"Solution: {best_position}, Fitness: {best_fitness}")
