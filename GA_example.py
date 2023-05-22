import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

def fob(x):
    #return x[0]**2+x[1]**2
    return -np.abs(np.sin(x[0])*np.cos(x[1])*np.exp(np.abs(1-np.sqrt(x[0]**2+x[1]**2)/np.pi)))

# Seed for reprodutibility
np.random.seed(seed=0)

## GA parameters
GEN_NUM = 2  # Number of genes
POP_SIZE = 10  # Size of population
NPOP_SIZE = 10  # Maximum size of new populations
CROSSOVER_PROB = 0.6  # Probability of crossover
MUTATION_PROB = 0.2  # Probability of mutation
SIGMA = 0.3  # Mutation range
ITER_MAX = 100  # Maximum of iterations

# Problem parameters
GEN_MIN = np.array([-10, -10])  # Minimal value for each gene
GEN_MAX = np.array([10, 10])  # Maximum value for each gene

# GA Performance by iteration
perf_best_ind = np.zeros((ITER_MAX+1, GEN_NUM))  # Best individual
perf_best_fit = np.zeros(ITER_MAX+1)  # Best fitness

# Initial population
np.random.seed(seed=0)
pop = np.random.uniform(low=GEN_MIN,high=GEN_MAX,size=(POP_SIZE, GEN_NUM))
pop_fit = np.zeros(POP_SIZE)

# Evaluating initial population
for ind in range(POP_SIZE):
    pop_fit[ind] = fob(pop[ind])

# Sorting population (minimization problem)
pop_idx = np.argsort(pop_fit)
pop_fit = np.sort(pop_fit)
perf_best_fit[0] = pop_fit[0]
perf_best_ind[0] = pop[pop_idx[0]]
print("iter: ",0,"| fitness:", perf_best_fit[0])

# Main loop
for iter in range(ITER_MAX):
    # New population size (crossovers + mutations)
    npop_size_cross = np.sum(np.random.rand(NPOP_SIZE) < CROSSOVER_PROB)
    npop_size_mut = np.sum(np.random.rand(NPOP_SIZE) < MUTATION_PROB)
    npop_size = npop_size_cross + npop_size_mut

    # Initializing new population
    npop = np.zeros((npop_size, GEN_NUM))
    npop_fit = np.zeros(npop_size)

    # Crossover and Mutation
    for ind in range(npop_size):
        if ind < npop_size_cross:
        # Crossover
            G1 = np.random.randint(low=GEN_NUM-1)  # Gen 1: [0, low)
            G2 = np.random.randint(low=G1+1,high=GEN_NUM+1)  # Gen 2: [low, high)
            F1 = np.random.randint(low=POP_SIZE)
            F2 = np.random.randint(low=POP_SIZE)
            ALPHA = np.random.uniform(low=-.1,high=1.1)  # Alpha: [-.1, 1.1)

            npop[ind] = np.concatenate((ALPHA*pop[F1,range(G1+1)]+(1-ALPHA)*pop[F2,range(G1+1)],
                                        (1-ALPHA)*pop[F1,range(G1+1,G2)]+ALPHA*pop[F2,range(G1+1,G2)]))  # Crossover
        else:
        # Mutation
            F1 = np.random.randint(low=POP_SIZE)  # Father
            npop[ind] = pop[F1]+np.random.normal(loc=0,scale=SIGMA,size=GEN_NUM)

    
    # New population
    for ind in range(npop_size):
        # Bounds of new population
        for gen in range(GEN_NUM):
            if npop[ind,gen] < GEN_MIN[gen]:
                npop[ind,gen] = GEN_MIN[gen]
            elif npop[ind,gen] > GEN_MAX[gen]:
                npop[ind,gen] = GEN_MAX[gen]

        # Evaluating new population
        npop_fit[ind] = fob(npop[ind])

    # Elitist Selection
    full_pop = np.concatenate((pop,npop))
    full_pop_fit = np.concatenate((pop_fit,npop_fit))

    # Sorting population (minimization problem)
    full_pop_idx = np.argsort(full_pop_fit)
    full_pop_fit = np.sort(full_pop_fit)

    # Updating population
    pop = full_pop[full_pop_idx[range(POP_SIZE)]]
    pop_fit = full_pop_fit[range(POP_SIZE)]

    perf_best_fit[iter+1] = full_pop_fit[0]
    perf_best_ind[iter+1] = full_pop[pop_idx[0]]

    print("iter: ",iter+1,"| fitness:", perf_best_fit[iter+1])

# plotting surface
def fob_plot(X,Y):
    #return X**2+Y**2
    return -np.abs(np.sin(X)*np.cos(Y)*np.exp(np.abs(1-np.sqrt(X**2+Y**2)/np.pi)))
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