import pyomo.environ as pyo
import numpy as np

# Scenarios data
LOAD = np.array([67, 35, 60, 79, 75])
PROB = np.array([30, 25, 20, 15, 10])/100
NCEN = len(LOAD)

# Solver options
opt = pyo.SolverFactory('glpk')

# Master problem
print("Iteration: 1")
mM = pyo.ConcreteModel()

# Variables
mM.Pg1 = pyo.Var(bounds=(0,40))
mM.alpha1 = pyo.Var(bounds=(0,10000))
mM.alpha2 = pyo.Var(bounds=(0,10000))
mM.alpha3 = pyo.Var(bounds=(0,10000))
mM.alpha4 = pyo.Var(bounds=(0,10000))
mM.alpha5 = pyo.Var(bounds=(0,10000))

# Objective
mM.obj = pyo.Objective(rule = 10*mM.Pg1 + mM.alpha1 + mM.alpha2 + mM.alpha3 + mM.alpha4 + mM.alpha5)

# List of Benders' cuts
mM.cuts = pyo.ConstraintList()

# Solving master problem
resM = opt.solve(mM)

print("Primals of master problem:")
for v in [mM.Pg1, mM.alpha1, mM.alpha2, mM.alpha3, mM.alpha4, mM.alpha5]:
    print(v, pyo.value(v), sep=' = ')

print("Objective of master problem:")
print(pyo.value(mM.obj))

OBJ_M = pyo.value(mM.obj)
ALPHA1 = pyo.value(mM.alpha1)
ALPHA2 = pyo.value(mM.alpha2)
ALPHA3 = pyo.value(mM.alpha3)
ALPHA4 = pyo.value(mM.alpha4)
ALPHA5 = pyo.value(mM.alpha5)
PG1 = pyo.value(mM.Pg1)

# Subproblem
mS = pyo.ConcreteModel()
mS.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

# Variables
mS.Pg1 = pyo.Var(bounds=(0,40))
mS.Pg2 = pyo.Var(bounds=(0,40))
mS.Pg3 = pyo.Var(bounds=(0,40))
mS.Pr_pos = pyo.Var(bounds=(0,110))
mS.Pr_neg = pyo.Var(bounds=(0,110))

# Objective
mS.obj = pyo.Objective(rule = 0*mS.Pg2 + 100*mS.Pg3 + 1000*mS.Pr_pos + 1000*mS.Pr_neg)

for iter in range(100):
    # Fixed constraint
    if iter>0:
        mS.del_component(mS.ConstraintFix)
    mS.ConstraintFix = pyo.Constraint(expr = mS.Pg1 == PG1)

    LAMB = []
    OBJ_S = []

    # Scenarios
    for icen in range(NCEN):
        print("  ")
        print("Scenario:", icen+1)

        # Load Balance in isce
        if icen>0 or iter>0:
            mS.del_component(mS.LoadBalance)
        mS.LoadBalance = pyo.Constraint(expr = mS.Pg1 + mS.Pg2 + mS.Pg3 + mS.Pr_pos - mS.Pr_neg == LOAD[icen])
        
        # Solving subproblem
        resS = opt.solve(mS)

        print("Primals of subproblem:")
        for v in [mS.Pg1, mS.Pg2, mS.Pg3, mS.Pr_pos, mS.Pr_neg]:
            print(v, pyo.value(v), sep=' = ')

        print("Objective of subproblem:")
        print(pyo.value(mS.obj))

        print("Duals of subproblem:")
        for v in [mS.ConstraintFix]:
            print(v, mS.dual[v], sep=' = ')

        LAMB.append(mS.dual[mS.ConstraintFix])
        OBJ_S.append(pyo.value(mS.obj))

    # Convergence checking
    z_up = OBJ_M - ALPHA1 - ALPHA2 - ALPHA3 - ALPHA4 - ALPHA5 + np.sum([OBJ_S[icen]*PROB[icen] for icen in range(NCEN)])
    z_dn = OBJ_M
    print("Zup: ", z_up)
    print("Zdn: ", z_dn)
    if z_up - z_dn < 1e-3:
        break

    print("----------")
    print("Iteration: ", iter+2)

    # Adding cuts to the master problem
    mM.cuts.add(expr = OBJ_S[0] + LAMB[0]*mM.Pg1 <= mM.alpha1/PROB[0] + LAMB[0]*PG1)
    mM.cuts.add(expr = OBJ_S[1] + LAMB[1]*mM.Pg1 <= mM.alpha2/PROB[1] + LAMB[1]*PG1)
    mM.cuts.add(expr = OBJ_S[2] + LAMB[2]*mM.Pg1 <= mM.alpha3/PROB[2] + LAMB[2]*PG1)
    mM.cuts.add(expr = OBJ_S[3] + LAMB[3]*mM.Pg1 <= mM.alpha4/PROB[3] + LAMB[3]*PG1)
    mM.cuts.add(expr = OBJ_S[4] + LAMB[4]*mM.Pg1 <= mM.alpha5/PROB[4] + LAMB[4]*PG1)

    # Solving master problem
    resM = opt.solve(mM)

    print("Primals:")
    for v in [mM.Pg1, mM.alpha1, mM.alpha2, mM.alpha3, mM.alpha4, mM.alpha5]:
        print(v, pyo.value(v), sep=' = ')

    print("Objective of master problem:")
    print(pyo.value(mM.obj))

    OBJ_M = pyo.value(mM.obj)
    ALPHA1 = pyo.value(mM.alpha1)
    ALPHA2 = pyo.value(mM.alpha2)
    ALPHA3 = pyo.value(mM.alpha3)
    ALPHA4 = pyo.value(mM.alpha4)
    ALPHA5 = pyo.value(mM.alpha5)
    PG1 = pyo.value(mM.Pg1)
