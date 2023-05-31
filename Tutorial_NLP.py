import pyomo.environ as pyo

# Solver options
opt = pyo.SolverFactory('Ipopt')

# Model
m = pyo.ConcreteModel()
m.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

# Variables
m.h = pyo.Var(bounds=(0,100))
m.w = pyo.Var(bounds=(0,100))
m.d = pyo.Var(bounds=(0,100))

# Objective
m.obj = pyo.Objective(expr = m.h*m.w*m.d, sense=pyo.maximize)

# Constraints
m.Constraint = pyo.Constraint(expr = 2*m.w*m.h + 2*m.d*m.h + 6*m.w*m.d <= 60)

# Solving model
opt.solve(m)

print("Primals")
for v in [m.h, m.w, m.d]:
    print(v, pyo.value(v), sep=' = ')

print("Objective")
print(pyo.value(m.obj))

print("Duals")
for v in [m.Constraint]:
    print(v, m.dual[v], sep=' = ')
