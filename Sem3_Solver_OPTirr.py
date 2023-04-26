import pyomo.environ as pyo

m = pyo.ConcreteModel()

m.x = pyo.Var()

m.OBJ = pyo.Objective(expr = -1.5*m.x**6-2*m.x**4+12*m.x, sense=pyo.maximize)

opt = pyo.SolverFactory('Ipopt')

res = opt.solve(m)

print("Primals")
for v in [m.x]:
    print(v, pyo.value(v), sep=' = ')
    


