from math import exp, sqrt, cos, pi

import numpy as np


def objective(x):
    return -20 * exp(-0.2 * sqrt(0.5 * (x[0] ** 2 + x[1] ** 2))) - exp(
        0.5 * (cos(2 * pi * x[0]) + cos(2 * pi * x[1]))) + 20 + exp(1)


best = np.random.uniform(-40, 40, 2)
step_size = 0.5

for x in range(0, 1000):
    tmp = best + np.random.uniform(-40, 40, 2) * step_size
    best = tmp
    print(objective(tmp))

print('Result:')
print('x:', best)
print('Fitness:', objective(best))
