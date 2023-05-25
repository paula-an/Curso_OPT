import pyomo.environ as pyo

# Solver options
opt = pyo.SolverFactory('glpk')

# Master problem
print("Iteration: 1")
mM = pyo.ConcreteModel()

# Variables
mM.Pg1 = pyo.Var(bounds=(0,40))
mM.alpha = pyo.Var(bounds=(0,10000))

# Objective
mM.obj = pyo.Objective(rule = 10*mM.Pg1 + mM.alpha)

# List of Benders' cuts
mM.cuts = pyo.ConstraintList()

# Solving master problem
opt.solve(mM)

print("Primals of master problem:")
for v in [mM.Pg1, mM.alpha]:
    print(v, pyo.value(v), sep=' = ')

print("Objective of master problem:")
print(pyo.value(mM.obj))

OBJ_M = pyo.value(mM.obj)
ALPHA = pyo.value(mM.alpha)
PG1 = pyo.value(mM.Pg1)

# Subproblem
mS = pyo.ConcreteModel()
mS.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

# Variables
mS.Pg1 = pyo.Var(bounds=(0,40))
mS.Pg2 = pyo.Var(bounds=(0,40))
mS.Pg3 = pyo.Var(bounds=(0,40))
mS.Pr = pyo.Var(bounds=(0,100))

# Objective
mS.obj = pyo.Objective(rule = 17*mS.Pg2 + 28*mS.Pg3 + 1000*mS.Pr)

# Load Balance
mS.LoadBalance = pyo.Constraint(expr = mS.Pg1 + mS.Pg2 + mS.Pg3 + mS.Pr == 100)

for iter in range(100):
    # Fixed constraint
    if iter>0:
        mS.del_component(mS.ConstraintFix)
    mS.ConstraintFix = pyo.Constraint(expr = mS.Pg1 == PG1)
    
    # Solving subproblem
    opt.solve(mS)

    print("Primals of subproblem:")
    for v in [mS.Pg1, mS.Pg2, mS.Pg3, mS.Pr]:
        print(v, pyo.value(v), sep=' = ')

    print("Objective of subproblem:")
    print(pyo.value(mS.obj))

    print("Duals of subproblem:")
    for v in [mS.ConstraintFix]:
        print(v, mS.dual[v], sep=' = ')

    LAMB = mS.dual[mS.ConstraintFix]
    OBJ_S = pyo.value(mS.obj)

    # Convergence checking
    z_up = OBJ_M - ALPHA + OBJ_S
    z_dn = OBJ_M
    print("Zup: ", z_up)
    print("Zdn: ", z_dn)
    if z_up - z_dn < 1e-3:
        break

    print('----------')
    print("Iteration: ", iter+2)

    # Adding cut to the master problem
    mM.cuts.add(expr = OBJ_S + LAMB*mM.Pg1 <= mM.alpha + LAMB*PG1)

    # Solving master problem
    opt.solve(mM)

    print("Primals:")
    for v in [mM.Pg1, mM.alpha]:
        print(v, pyo.value(v), sep=' = ')

    print("Objective of master problem:")
    print(pyo.value(mM.obj))

    OBJ_M = pyo.value(mM.obj)
    ALPHA = pyo.value(mM.alpha)
    PG1 = pyo.value(mM.Pg1)

