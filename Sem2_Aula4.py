import pyomo.environ as pyo
import numpy as np
import matplotlib.pyplot as plt

def cons_rule(icon):
    return sum(m.p[i]*X[i+icon] for i in setP) + m.Rd[icon] - m.Re[icon] == X[icon+NVARS]


# Parâmetros do problema de regressão
X = [4.2456, 5.6633, 7.2894, 12.2750, 18.1518, 23.3164, 32.1196,
     37.3820, 47.6247, 51.4674, 59.3872, 64.3107, 69.9837, 78.3740,
     81.8589, 83.5148, 89.6984, 87.6712, 91.8379, 93.3468]
NVARS = 6
NSAMPLES = np.shape(X)[0]
NCONS = NSAMPLES - NVARS



m = pyo.ConcreteModel()

setP = range(NVARS)
setR = range(NCONS)

m.p = pyo.Var(setP, bounds=(-10, 10))
m.Rd = pyo.Var(setR, bounds=(0, 1000))
m.Re = pyo.Var(setR, bounds=(0, 1000))

m.OBJ = pyo.Objective(expr=sum(m.Rd[k]+m.Re[k] for k in setR))

m.cons = pyo.ConstraintList()

for icon in setR:
    m.cons.add(cons_rule(icon))

opt = pyo.SolverFactory('Ipopt')

res = opt.solve(m)

print("Primals")
p = list()
for i in setP:
    print(m.p[i], pyo.value(m.p[i]), sep=' = ')
    p.append(pyo.value(m.p[i]))
for k in setR:
    print(m.Rd[k], pyo.value(m.Rd[k]), sep=' = ')
for k in setR:
    print(m.Re[k], pyo.value(m.Re[k]), sep=' = ')

X.append(sum(p[i]*X[i-NVARS] for i in setP))

plt.plot(X)
plt.plot(NSAMPLES, X[-1], 'r*')
plt.show()