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
m.pg1 = pyo.Var(bounds=(0,40))
m.pg2 = pyo.Var(bounds=(0,40))
m.pg3 = pyo.Var(bounds=(0,40))

# Objective
m.obj = pyo.Objective(expr = 10*m.pg1 + 17*m.pg2 + 28*m.pg3)

# Constraint
m.Constraint = pyo.Constraint(expr = m.pg1 + m.pg2 + m.pg3 == 100)

# Solving model
opt.solve(m)

print("Primals")
for v in [m.pg1, m.pg2, m.pg3]:
    print(v, pyo.value(v), sep=' = ')

print("Objective")
print(pyo.value(m.obj))

print("Duals")
for v in [m.Constraint]:
    print(v, m.dual[v], sep=' = ')

print("Duals of canalization")
for v in [m.pg1, m.pg2, m.pg3]:
    print(
        "%s %12g %12g" % (v, m.ipopt_zL_out[v], m.ipopt_zU_out[v])
    )

