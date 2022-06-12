from math import exp, sqrt, cos, pi

from mealpy.bio_based.IWO import OriginalIWO


def fitness_function(solution):
    return -20 * exp(-0.2 * sqrt(0.5 * (solution[0] ** 2 + solution[1] ** 2))) \
           - exp(0.5 * (cos(2 * pi * solution[0]) + cos(2 * pi * solution[1]))) + 20 + exp(1)


problem_dict1 = {
    "fit_func": fitness_function,
    "lb": [-10, -10],
    "ub": [10, 10],
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
