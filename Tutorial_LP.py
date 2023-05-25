import pyomo.environ as pyo

# Solver options
opt = pyo.SolverFactory('Ipopt')

# Model
m = pyo.ConcreteModel()
m.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

# Ipopt bound multipliers (obtained from solution)
m.ipopt_zL_out = pyo.Suffix(direction=pyo.Suffix.IMPORT)
m.ipopt_zU_out = pyo.Suffix(direction=pyo.Suffix.IMPORT)

# Variables
m.x1 = pyo.Var(bounds=(0,12))
m.x2 = pyo.Var(bounds=(0,16))

# Objective
m.obj = pyo.Objective(expr = m.x1 + m.x2, sense=pyo.maximize)

# Constraint
m.Constraint1 = pyo.Constraint(expr = 2/3*m.x1 + m.x2 <= 18)
m.Constraint2 = pyo.Constraint(expr =   2*m.x1 + m.x2 >= 8)

# Solving model
opt.solve(m)

print("Primals")
for v in [m.x1, m.x2]:
    print(v, pyo.value(v), sep=' = ')

print("Objective")
print(pyo.value(m.obj))

print("Duals")
for v in [m.Constraint1, m.Constraint1]:
    print(v, m.dual[v], sep=' = ')

print("Duals of canalization")
for v in [m.x1, m.x2]:
    print("%s %12g %12g" % (v, m.ipopt_zL_out[v], m.ipopt_zU_out[v]))

