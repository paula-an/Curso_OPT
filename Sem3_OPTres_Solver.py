import pyomo.environ as pyo

# Solver options
opt = pyo.SolverFactory('Ipopt')

# Model
m = pyo.ConcreteModel()
m.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

# Variables
m.x = pyo.Var()
m.y = pyo.Var()

# Objective
m.obj = pyo.Objective(expr = pyo.exp(m.x)*(4*m.x**2+2*m.y**2+4*m.x*m.y+2*m.y+1))

# Constraints
m.Constraint0 = pyo.Constraint(expr = m.x*m.y >= -10)
m.Constraint1 = pyo.Constraint(expr = 1.5+m.x*m.y-m.x-m.y <= 0)

# Solving model
opt.solve(m)

print("Primals")
for v in [m.x, m.y]:
    print(v, pyo.value(v), sep=' = ')

print("Objective")
print(pyo.value(m.obj))

print("Duals")
for v in [m.Constraint0,m.Constraint1]:
    print(v, m.dual[v], sep=' = ')
