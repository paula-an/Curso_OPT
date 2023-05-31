import numpy as np
from geneticalgorithm import geneticalgorithm as ga

def fob(x):
    return -np.abs(
        np.sin(x[0])
        * np.cos(x[1])
        * np.exp(np.abs(1 - np.sqrt(x[0] ** 2 + x[1] ** 2) / np.pi))
    )


# Seed for reprodutibility
np.random.seed(seed=0)

## GA parameters
GEN_NUM = 2  # Number of genes
POP_SIZE = 10  # Size of population
NPOP_SIZE = 10  # Maximum size of new populations
CROSSOVER_PROB = 0.6  # Probability of crossover
MUTATION_PROB = 0.2  # Probability of mutation
SIGMA = 0.3  # Mutation range
ITER_MAX = 1000  # Maximum of iterations

algotithm_param = {
    "max_num_iteration": ITER_MAX,
    "population_size": POP_SIZE,
    "mutation_probability": MUTATION_PROB,
    "elit_ratio": 0.01,
    "crossover_probability": CROSSOVER_PROB,
    "parents_portion": 0.2,
    "crossover_type": "uniform",
    "max_iteration_without_improv": None,
}

model = ga(
    function=fob,
    dimension=GEN_NUM,
    variable_type="real",
    variable_boundaries=np.array([[-10, 10], [-10, 10]]),
    algorithm_parameters=algotithm_param,
)
model.run()
