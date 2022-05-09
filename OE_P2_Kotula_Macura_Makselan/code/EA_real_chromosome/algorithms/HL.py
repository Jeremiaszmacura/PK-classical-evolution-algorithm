# https://machinelearningmastery.com/stochastic-hill-climbing-in-python-from-scratch/
from math import exp, sqrt, cos, pi

from matplotlib import pyplot
from numpy import asarray
from numpy.random import rand
from numpy.random import randn
from numpy.random import seed


# objective function
def objective(x):
    return -20 * exp(-0.2 * sqrt(0.5 * (x[0] ** 2 + x[1] ** 2))) - exp(
        0.5 * (cos(2 * pi * x[0]) + cos(2 * pi * x[1]))) + 20 + exp(1)


# hill climbing local search algorithm
def hill_climbing(objective, bounds, n_iterations, step_size):
    # generate an initial point
    solution = [bounds[:, 0] + rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0]),
                bounds[:, 0] + rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])]
    # evaluate the initial point
    solution_eval = objective(solution)
    # run the hill climb
    scores = list()
    scores.append(solution_eval)
    for i in range(n_iterations):
        # take a step
        candidate = solution + randn(len(bounds)) * step_size
        # evaluate candidate point
        candidate_eval = objective(candidate)
        # check if we should keep the new point
        if candidate_eval <= solution_eval:
            # store the new point
            solution, solution_eval = candidate, candidate_eval
            # keep track of scores
            scores.append(solution_eval)
            # report progress
            print('>%d f(%s,%s) = %.5f' % (i, solution[0], solution[1], solution_eval))
    return [solution, solution_eval, scores]


# seed the pseudorandom number generator
seed(5)
# define range for input
bounds = asarray([[-40, 40]])
# define the total iterations
n_iterations = 1000
# define the maximum step size
step_size = 0.1
# perform the hill climbing search
best, score, scores = hill_climbing(objective, bounds, n_iterations, step_size)
print('Done!')
print('f(%s) = %f' % (best, score))
# line plot of best scores
pyplot.plot(scores, '.-')
pyplot.xlabel('Improvement Number')
pyplot.ylabel('Evaluation f(x)')
pyplot.show()
