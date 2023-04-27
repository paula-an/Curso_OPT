import pyomo.environ as pyo

# Solver options
opt = pyo.SolverFactory('glpk')

# Primal problem
mP = pyo.ConcreteModel()
mP.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

# Variables
mP.x1 = pyo.Var(bounds=(0,20))
mP.x2 = pyo.Var(bounds=(0,20))
mP.x3 = pyo.Var(bounds=(0,20))

# Objective
mP.obj = pyo.Objective(rule = 5*mP.x1 + 2*mP.x2 + mP.x3)

# Constraints
mP.Constraint1 = pyo.Constraint(expr = 2*mP.x1 + 3*mP.x2 +   mP.x3 >= 20)
mP.Constraint2 = pyo.Constraint(expr = 6*mP.x1 + 8*mP.x2 + 5*mP.x3 >= 30)
mP.Constraint3 = pyo.Constraint(expr = 7*mP.x1 +   mP.x2 + 3*mP.x3 >= 40)
mP.Constraint4 = pyo.Constraint(expr =   mP.x1 + 2*mP.x2 + 4*mP.x3 >= 50)

# Solving primal problem
resP = opt.solve(mP)

print("Primals:")
for v in [mP.x1, mP.x2, mP.x3]:
    print(v, pyo.value(v), sep=' = ')

print("Objective of primal problem:")
print(pyo.value(mP.obj))

print("Duals from primal problem:")
for v in [mP.Constraint1, mP.Constraint2, mP.Constraint3, mP.Constraint4]:
    print(v, mP.dual[v], sep=' = ')

# Dual problemn
mD = pyo.ConcreteModel()

# Variables
mD.w1 = pyo.Var(bounds=(0,100))
mD.w2 = pyo.Var(bounds=(0,100))
mD.w3 = pyo.Var(bounds=(0,100))
mD.w4 = pyo.Var(bounds=(0,100))

# Objective
mD.obj = pyo.Objective(rule = 20*mD.w1 + 30*mD.w2 + 40*mD.w3 + 50*mD.w4, sense=pyo.maximize)

# Constraints
mD.Constraint0 = pyo.Constraint(expr = 2*mD.w1 + 6*mD.w2 + 7*mD.w3 +   mD.w4 <= 5)
mD.Constraint1 = pyo.Constraint(expr = 3*mD.w1 + 8*mD.w2 +   mD.w3 + 2*mD.w4 <= 2)
mD.Constraint2 = pyo.Constraint(expr =   mD.w1 + 5*mD.w2 + 3*mD.w3 + 4*mD.w4 <= 1)

# Solving dual problem
resD = opt.solve(mD)

print("Duals from dual problem:")
for v in [mD.w1, mD.w2, mD.w3, mD.w4]:
    print(v, pyo.value(v), sep=' = ')

print("Objective of dual problem:")
print(pyo.value(mD.obj))
    


