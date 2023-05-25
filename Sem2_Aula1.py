import pyomo.environ as pyo

# Solver options
opt = pyo.SolverFactory('Ipopt')

# Model
m = pyo.ConcreteModel()
m.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

# Variables
m.x1 = pyo.Var(bounds=(2,10))
m.x2 = pyo.Var(bounds=(2,10))

# Objective
m.obj = pyo.Objective(expr = m.x1 + 3*m.x2)

# Constraints
m.Constraint0 = pyo.Constraint(expr = m.x1 - m.x2 == 3)
m.Constraint1 = pyo.Constraint(expr = 5*m.x1 + 2*m.x2 == 29.4)

# Solving model
opt.solve(m)

print("Primals")
for v in [m.x1, m.x2]:
    print(v, pyo.value(v), sep=' = ')

print("Objective")
print(pyo.value(m.obj))

print("Duals")
for v in [m.Constraint0, m.Constraint1]:
    print(v, m.dual[v], sep=' = ')
    


