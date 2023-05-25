import pyomo.environ as pyo
import numpy as np

# Constants
LOAD = 50
VA0 = 90
TOL = 1e-2


opt = pyo.SolverFactory('glpk')

# Models (Stages)
mS1 = pyo.ConcreteModel()
mS1.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
mS2 = pyo.ConcreteModel()
mS2.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
mS3 = pyo.ConcreteModel()
mS3.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

# Variables - Stage 1
mS1.Pg1 = pyo.Var(bounds=(0,30))
mS1.Pg2 = pyo.Var(bounds=(0,30))
mS1.Pr = pyo.Var(bounds=(0,LOAD))
mS1.Vt1 = pyo.Var(bounds=(0,50))
mS1.Va1 = pyo.Var(bounds=(0,90))
mS1.alpha = pyo.Var(bounds=(0,10000))

# Variables - Stage 2
mS2.Pg1 = pyo.Var(bounds=(0,30))
mS2.Pg2 = pyo.Var(bounds=(0,30))
mS2.Pr = pyo.Var(bounds=(0,LOAD))
mS2.Vt2 = pyo.Var(bounds=(0,50))
mS2.Va2 = pyo.Var(bounds=(0,90))
mS2.alpha = pyo.Var(bounds=(0,10000))

# Variables - Stage 3
mS3.Pg1 = pyo.Var(bounds=(0,30))
mS3.Pg2 = pyo.Var(bounds=(0,30))
mS3.Pr = pyo.Var(bounds=(0,LOAD))
mS3.Vt3 = pyo.Var(bounds=(0,50))
mS3.Va3 = pyo.Var(bounds=(0,90))

# Load Balance Constraints
mS1.LoadBalance = pyo.Constraint(expr = mS1.Pg1 + mS1.Pg2 + mS1.Vt1 + mS1.Pr == LOAD)
mS2.LoadBalance = pyo.Constraint(expr = mS2.Pg1 + mS2.Pg2 + mS2.Vt2 + mS2.Pr == LOAD)
mS3.LoadBalance = pyo.Constraint(expr = mS3.Pg1 + mS3.Pg2 + mS3.Vt3 + mS3.Pr == LOAD)

# Objectives
mS1.obj = pyo.Objective(rule = 10*mS1.Pg1 + 20*mS1.Pg2 + 1000*mS1.Pr + mS1.alpha)
mS2.obj = pyo.Objective(rule = 10*mS2.Pg1 + 20*mS2.Pg2 + 1000*mS2.Pr + mS2.alpha)
mS3.obj = pyo.Objective(rule = 10*mS3.Pg1 + 20*mS3.Pg2 + 1000*mS3.Pr)

# List of cuts
mS1.cuts = pyo.ConstraintList()
mS2.cuts = pyo.ConstraintList()

# Dynamic Optimization

## -------
## Forward
## -------
# Stage 1

mS1.Hydro= pyo.Constraint(expr = mS1.Va1 + mS1.Vt1 == VA0)

opt.solve(mS1)

print("Primals of Stage 1:")
for v in [mS1.Pg1, mS1.Pg2, mS1.Pr, mS1.Vt1, mS1.Va1, mS1.alpha]:
    print(v, pyo.value(v), sep=' = ')

print("Objective of Stage 1:")
print(pyo.value(mS1.obj))

OBJ_S1 = pyo.value(mS1.obj)
ALPHA_S1 = pyo.value(mS1.alpha)

flag_to_break = False
for iter in range(1000):
    print('  ')
    print('iter:', iter)
    print('  ')

    # Stage 2 - Forward
    VA1 = pyo.value(mS1.Va1)
    if iter>0:
        mS2.del_component(mS2.Hydro)
    mS2.Hydro = pyo.Constraint(expr = mS2.Va2 + mS2.Vt2 == VA1)

    opt.solve(mS2)

    print("Primals of Stage 2:")
    for v in [mS2.Pg1, mS2.Pg2, mS2.Pr, mS2.Vt2, mS2.Va2, mS2.alpha]:
        print(v, pyo.value(v), sep=' = ')

    print("Objective of Stage 2:")
    print(pyo.value(mS2.obj))
    
    OBJ_S2 = pyo.value(mS2.obj)
    ALPHA_S2 = pyo.value(mS2.alpha)

    # Stage 3 - Forward
    VA2 = pyo.value(mS2.Va2)
    if iter>0:
        mS3.del_component(mS3.Hydro)
    mS3.Hydro = pyo.Constraint(expr = mS3.Va3 + mS3.Vt3 == VA2)

    opt.solve(mS3)

    print("Primals of Stage 3:")
    for v in [mS3.Pg1, mS3.Pg2, mS3.Pr, mS3.Vt3, mS3.Va3]:
        print(v, pyo.value(v), sep=' = ')

    print("Objective of Stage 3:")
    print(pyo.value(mS3.obj))

    print("Duals of Stage 3:")
    for v in [mS3.Hydro]:
        print(v, mS3.dual[v], sep=' = ')
    
    OBJ_S3 = pyo.value(mS3.obj)
    LAMB3 = mS3.dual[mS3.Hydro]

    if flag_to_break:
        break

    ## --------
    ## Backward
    ## --------
    z_up = list()
    z_dn = list()

    # Stage 2 - Backward
    mS2.cuts.add(expr = OBJ_S3 + LAMB3*mS2.Va2 <= mS2.alpha + LAMB3*VA2)

    opt.solve(mS2)

    print("Primals of Stage 2:")
    for v in [mS2.Pg1, mS2.Pg2, mS2.Pr, mS2.Vt2, mS2.Va2, mS2.alpha]:
        print(v, pyo.value(v), sep=' = ')

    print("Objective of Stage 2:")
    print(pyo.value(mS2.obj))

    print("Duals of Stage 2:")
    for v in [mS2.Hydro]:
        print(v, mS2.dual[v], sep=' = ')

    OBJ_S2 = pyo.value(mS2.obj)
    ALPHA_S2 = pyo.value(mS2.alpha)
    LAMB2 = mS2.dual[mS2.Hydro]

    z_up.append(OBJ_S2 - ALPHA_S2 + OBJ_S3)
    z_dn.append(OBJ_S2)

    # Stage 1 - Backward
    mS1.cuts.add(expr = OBJ_S2 + LAMB2*mS1.Va1 <= mS1.alpha + LAMB2*VA1)

    opt.solve(mS1)

    print("Primals of Stage 1:")
    for v in [mS1.Pg1, mS1.Pg2, mS1.Pr, mS1.Vt1, mS1.Va1, mS1.alpha]:
        print(v, pyo.value(v), sep=' = ')

    print("Objective of Stage 1:")
    print(pyo.value(mS1.obj))

    OBJ_S1 = pyo.value(mS1.obj)
    ALPHA_S1 = pyo.value(mS1.alpha)

    # Convergence check
    z_up.append(OBJ_S1 - ALPHA_S1 + OBJ_S2)
    z_dn.append(OBJ_S1)
    z_up = np.array(z_up)
    z_dn = np.array(z_dn)
    print("Zup =", z_up, "| Zdn =", z_dn)
    print("Convergence:", np.max(z_up - z_dn))
    
    if np.max(np.abs(z_up - z_dn)) < TOL:
        flag_to_break = True

# Results
print(" ")
print("Results:")
print('Stage 1:')
for v in [mS1.Pg1, mS1.Pg2, mS1.Pr, mS1.Vt1, mS1.Va1]:
    print(v, pyo.value(v), sep=' = ')
print('Stage 2:')
for v in [mS2.Pg1, mS2.Pg2, mS2.Pr, mS2.Vt2, mS2.Va2]:
    print(v, pyo.value(v), sep=' = ')
print('Stage 3:')
for v in [mS3.Pg1, mS3.Pg2, mS3.Pr, mS3.Vt3, mS3.Va3]:
    print(v, pyo.value(v), sep=' = ')

total_cost = 10*(pyo.value(mS1.Pg1)+pyo.value(mS2.Pg1)+pyo.value(mS3.Pg1))\
+20*(pyo.value(mS1.Pg2)+pyo.value(mS2.Pg2)+pyo.value(mS3.Pg2))

print("Total cost:")
print(total_cost)