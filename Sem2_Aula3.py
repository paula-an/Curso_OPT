import pyomo.environ as pyo

m = pyo.ConcreteModel()

m.pg1 = pyo.Var(bounds=(0,40))
m.pg2 = pyo.Var(bounds=(0,40))
m.pg3 = pyo.Var(bounds=(0,40))
m.pgF = pyo.Var(bounds=(0,400))

m.OBJ = pyo.Objective(expr = 10*m.pg1 + 17*m.pg2 + 28*m.pg3 + 100*m.pgF)

m.Constraint0 = pyo.Constraint(expr = m.pg1 + m.pg2 + m.pg3  + m.pgF== 130)

m.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)


# Ipopt bound multipliers (obtained from solution)
m.ipopt_zL_out = pyo.Suffix(direction=pyo.Suffix.IMPORT)
m.ipopt_zU_out = pyo.Suffix(direction=pyo.Suffix.IMPORT)

opt = pyo.SolverFactory('Ipopt')

res = opt.solve(m)

print("Primals")
for v in [m.pg1, m.pg2, m.pg3, m.pgF]:
    print(v, pyo.value(v), sep=' = ')

print("Objective")
print(pyo.value(m.OBJ))

print("Duals")
for v in [m.Constraint0]:
    print(v, m.dual[v], sep=' = ')

for v in [m.pg1, m.pg2, m.pg3, m.pgF]:
    print(
        "%s %7g %12g %12g" % (v, pyo.value(v), m.ipopt_zL_out[v], m.ipopt_zU_out[v])
    )
