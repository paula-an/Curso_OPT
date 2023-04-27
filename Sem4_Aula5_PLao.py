import pyomo.environ as pyo

# Constants
LOAD = 50
VA0 = 90

# Solver options
opt = pyo.SolverFactory('glpk')

# Model
mS = pyo.ConcreteModel()
mS.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

# Variables
mS.Pg1_1 = pyo.Var(bounds=(0,30))
mS.Pg2_1 = pyo.Var(bounds=(0,30))
mS.Pr_1 = pyo.Var(bounds=(0,LOAD))
mS.Vt_1 = pyo.Var(bounds=(0,50))
mS.Va_1 = pyo.Var(bounds=(0,90))

mS.Pg1_2 = pyo.Var(bounds=(0,30))
mS.Pg2_2 = pyo.Var(bounds=(0,30))
mS.Pr_2 = pyo.Var(bounds=(0,LOAD))
mS.Vt_2 = pyo.Var(bounds=(0,50))
mS.Va_2 = pyo.Var(bounds=(0,90))

mS.Pg1_3 = pyo.Var(bounds=(0,30))
mS.Pg2_3 = pyo.Var(bounds=(0,30))
mS.Pr_3 = pyo.Var(bounds=(0,LOAD))
mS.Vt_3 = pyo.Var(bounds=(0,50))
mS.Va_3 = pyo.Var(bounds=(0,90))

# Objectives
mS.obj = pyo.Objective(rule = 10*mS.Pg1_1 + 20*mS.Pg2_1 + 1000*mS.Pr_1
                        + 10*mS.Pg1_2 + 20*mS.Pg2_2 + 1000*mS.Pr_2
                        + 10*mS.Pg1_3 + 20*mS.Pg2_3 + 1000*mS.Pr_3)

# Load Balance Constraints
mS.LoadBalance1 = pyo.Constraint(expr = mS.Pg1_1 + mS.Pg2_1 + mS.Vt_1 + mS.Pr_1 == LOAD)
mS.LoadBalance2 = pyo.Constraint(expr = mS.Pg1_2 + mS.Pg2_2 + mS.Vt_2 + mS.Pr_2 == LOAD)
mS.LoadBalance3 = pyo.Constraint(expr = mS.Pg1_3 + mS.Pg2_3 + mS.Vt_3 + mS.Pr_3 == LOAD)

# Hydro balance
mS.Hydro1 = pyo.Constraint(expr = mS.Va_1 + mS.Vt_1 == VA0)
mS.Hydro2 = pyo.Constraint(expr = mS.Va_2 + mS.Vt_2 == mS.Va_1)
mS.Hydro3 = pyo.Constraint(expr = mS.Va_3 + mS.Vt_3 == mS.Va_2)

resS1 = opt.solve(mS)

print("Primals:")
for v in [mS.Pg1_1, mS.Pg2_1, mS.Pr_1, mS.Vt_1, mS.Va_1,
          mS.Pg1_2, mS.Pg2_2, mS.Pr_2, mS.Vt_2, mS.Va_2,
          mS.Pg1_3, mS.Pg2_3, mS.Pr_3, mS.Vt_3, mS.Va_3]:
    print(v, pyo.value(v), sep=' = ')

print("Objective:")
print(pyo.value(mS.obj))