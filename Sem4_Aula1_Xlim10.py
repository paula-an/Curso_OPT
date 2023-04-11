import pyomo.environ as pyo

# Problema Primal

mP = pyo.ConcreteModel()

mP.x1 = pyo.Var(bounds=(0,10))
mP.x2 = pyo.Var(bounds=(0,10))
mP.x3 = pyo.Var(bounds=(0,10))

mP.OBJ = pyo.Objective(rule = 5*mP.x1 + 2*mP.x2 + mP.x3)

mP.Constraint1 = pyo.Constraint(expr = 2*mP.x1 + 3*mP.x2 +   mP.x3 >= 20)
mP.Constraint2 = pyo.Constraint(expr = 6*mP.x1 + 8*mP.x2 + 5*mP.x3 >= 30)
mP.Constraint3 = pyo.Constraint(expr = 7*mP.x1 +   mP.x2 + 3*mP.x3 >= 40)
mP.Constraint4 = pyo.Constraint(expr =   mP.x1 + 2*mP.x2 + 4*mP.x3 >= 50)
mP.Constraint5 = pyo.Constraint(expr =-  mP.x1                     >=-10)
mP.Constraint5 = pyo.Constraint(expr =         -   mP.x2           >=-10)
mP.Constraint5 = pyo.Constraint(expr =                   -   mP.x3 >=-10)


mP.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

opt = pyo.SolverFactory('Ipopt')

resP = opt.solve(mP)

print("Primals:")
for v in [mP.x1, mP.x2, mP.x3]:
    print(v, pyo.value(v), sep=' = ')

print("Objective of primal problem:")
print(pyo.value(mP.OBJ))

print("Duals from primal problem:")
for v in [mP.Constraint1, mP.Constraint2, mP.Constraint3, mP.Constraint4]:
    print(v, mP.dual[v], sep=' = ')

# Problema dual

mD = pyo.ConcreteModel()

mD.w1 = pyo.Var(bounds=(0,100))
mD.w2 = pyo.Var(bounds=(0,100))
mD.w3 = pyo.Var(bounds=(0,100))
mD.w4 = pyo.Var(bounds=(0,100))
mD.w5 = pyo.Var(bounds=(0,100))
mD.w6 = pyo.Var(bounds=(0,100))
mD.w7 = pyo.Var(bounds=(0,100))

mD.OBJ = pyo.Objective(rule = 20*mD.w1 + 30*mD.w2 + 40*mD.w3 + 50*mD.w4 - 10*mD.w5 - 10*mD.w6 - 10*mD.w7, sense=pyo.maximize)

mD.Constraint0 = pyo.Constraint(expr = 2*mD.w1 + 6*mD.w2 + 7*mD.w3 +   mD.w4 - mD.w5                  <= 5)
mD.Constraint1 = pyo.Constraint(expr = 3*mD.w1 + 8*mD.w2 +   mD.w3 + 2*mD.w4         - mD.w6          <= 2)
mD.Constraint2 = pyo.Constraint(expr =   mD.w1 + 5*mD.w2 + 3*mD.w3 + 4*mD.w4                 - mD.w7  <= 1)

resD = opt.solve(mD)

print("Duals from dual problem:")
for v in [mD.w1, mD.w2, mD.w3, mD.w4, mD.w5, mD.w6, mD.w7]:
    print(v, pyo.value(v), sep=' = ')

print("Objective of primal problem:")
print(pyo.value(mD.OBJ))
    


