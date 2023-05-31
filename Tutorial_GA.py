import numpy as np
from geneticalgorithm import geneticalgorithm as ga
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator


def fob(x):
    return x[0]**2+x[1]**2


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

# plotting surface
def fob_plot(X,Y):
    #return X**2+Y**2
    return X**2+Y**2
# Plot 3D surface
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# Make data.
X = np.arange(-10, 10, 0.25)
Y = np.arange(-10, 10, 0.25)
X, Y = np.meshgrid(X, Y)
Z = fob_plot(X,Y)
# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')
# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()