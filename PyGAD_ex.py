import pygad
import numpy as np

def fitness_func(ga_instance, solution, solution_idx):
    return -solution**2


ga_instance = pygad.GA(num_generations = 50,
                       num_parents_mating = 4,
                       fitness_func = fitness_func,
                       parent_selection_type = "rank",
                       num_genes=1,
                       sol_per_pop=5,
                       keep_parents = -1,
                       crossover_type = None,
                       mutation_type = "random",
                       mutation_percent_genes = 50,
                       random_mutation_min_val = -10,
                       random_mutation_max_val = +10,
                       save_best_solutions = True)


ga_instance.run()

ga_instance.plot_result()