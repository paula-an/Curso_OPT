import pyomo.environ as pyo

# Master problem
print("Iteration: 1")

mM = pyo.ConcreteModel()

mM.Pg1 = pyo.Var(bounds=(0,40))
mM.alpha = pyo.Var(bounds=(0,10000))
mM.OBJ = pyo.Objective(rule = 10*mM.Pg1 + mM.alpha)

mM.cuts = pyo.ConstraintList()

opt = pyo.SolverFactory('Ipopt')

resM = opt.solve(mM)

print("Primals of master problem:")
for v in [mM.Pg1, mM.alpha]:
    print(v, pyo.value(v), sep=' = ')

print("Objective of master problem:")
print(pyo.value(mM.OBJ))

OBJ_M = pyo.value(mM.OBJ)
ALPHA = pyo.value(mM.alpha)
PG1 = pyo.value(mM.Pg1)

# Subproblem

mS = pyo.ConcreteModel()

mS.Pg1 = pyo.Var(bounds=(0,40))
mS.Pg2 = pyo.Var(bounds=(0,40))
mS.Pg3 = pyo.Var(bounds=(0,40))
mS.Pr = pyo.Var(bounds=(0,100))

mS.OBJ = pyo.Objective(rule = 17*mS.Pg2 + 28*mS.Pg3 + 1000*mS.Pr)

mS.Constraint = pyo.Constraint(expr = mS.Pg1 + mS.Pg2 + mS.Pg3 + mS.Pr == 100)

mS.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

for iter in range(100):
    if iter>0:
        mS.del_component(mS.ConstraintFix)
    mS.ConstraintFix = pyo.Constraint(expr = mS.Pg1 == PG1)
    resS = opt.solve(mS)

    print("Primals of subproblem:")
    for v in [mS.Pg1, mS.Pg2, mS.Pg3, mS.Pr]:
        print(v, pyo.value(v), sep=' = ')

    print("Objective of subproblem:")
    print(pyo.value(mS.OBJ))

    print("Duals of subproblem:")
    for v in [mS.ConstraintFix]:
        print(v, mS.dual[v], sep=' = ')

    lamb = mS.dual[mS.ConstraintFix]
    OBJ_S = pyo.value(mS.OBJ)

    # Convergence checking

    z_up = OBJ_M - ALPHA + OBJ_S
    z_dn = OBJ_M
    print("Zup: ", z_up)
    print("Zdn: ", z_dn)

    if z_up - z_dn < 1e-3:
        break

    print('----------')
    print("Iteration: ", iter+2)

    # Master Problem

    mM.cuts.add(expr = OBJ_S + lamb*mM.Pg1 <= mM.alpha + lamb*PG1)

    resM = opt.solve(mM)

    print("Primals:")
    for v in [mM.Pg1, mM.alpha]:
        print(v, pyo.value(v), sep=' = ')

    print("Objective of master problem:")
    print(pyo.value(mM.OBJ))

    OBJ_M = pyo.value(mM.OBJ)
    ALPHA = pyo.value(mM.alpha)
    PG1 = pyo.value(mM.Pg1)

