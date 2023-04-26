import pyomo.environ as pyo

m = pyo.ConcreteModel()

m.x1 = pyo.Var(domain=pyo.PositiveIntegers)
m.x2 = pyo.Var(domain=pyo.PositiveIntegers)
m.x3 = pyo.Var(domain=pyo.PositiveIntegers)

m.OBJ = pyo.Objective(expr = 3*m.x1+2*m.x2+4*m.x3, sense=pyo.maximize)

m.Constraint0 = pyo.Constraint(expr = m.x1  -  m.x2+2*m.x3 <= 15)
m.Constraint1 = pyo.Constraint(expr = m.x1  +  m.x2+  m.x3 <= 12)
m.Constraint2 = pyo.Constraint(expr = 4*m.x1+3*m.x2+3*m.x3 <= 25)
m.Constraint3 = pyo.Constraint(expr = 2*m.x1+4*m.x2+5*m.x3 <= 30)

opt = pyo.SolverFactory('glpk')

res = opt.solve(m)

print("Primals")
for v in [m.x1, m.x2, m.x3]:
    print(v, pyo.value(v), sep=' = ')

print("Objective")
print(pyo.value(m.OBJ))
    


