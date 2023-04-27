import pyomo.environ as pyo

# Solver options
opt = pyo.SolverFactory('Ipopt')

# Model
m = pyo.ConcreteModel()

# Variable
m.x = pyo.Var()

# Objective
m.obj = pyo.Objective(expr = -1.5*m.x**6-2*m.x**4+12*m.x, sense=pyo.maximize)

# Solving model
res = opt.solve(m)

print("Primals")
for v in [m.x]:
    print(v, pyo.value(v), sep=' = ')
