import pyomo.environ as pyo
import numpy as np
import matplotlib.pyplot as plt

def cons_rule(icon):
    return m.a + m.b1*X1[icon]+m.b2*X2[icon]+\
        m.c1*X1[icon]**2+m.c2*X2[icon]**2+\
            m.d1*X1[icon]**3+m.d2*X2[icon]**3+\
                m.Rd[icon] - m.Re[icon] == Z[icon]


# Parâmetros do problema de regressão
X1 = [1.4186,2.2044,2.0075,2.2698,2.6108,3.2287,4.1146,5.0125,
      5.4144,6.5138,7.8987,9.7547,11.3829,13.5158,17.3026,20.5118,
      24.8039,30.1037,36.7393,45.5236,55.5673]

X2 = [0.7690,0.8015,1.3545,1.0315,1.2575,1.7678,2.4432,3.2443,4.2349,
      5.5488,6.5130,8.8989,10.5882,12.6697,15.5504,19.7065,24.4637,29.0275,
      36.5826,44.2146,53.7321]

Z = [4.6416,1.5977,8.1200,11.6357,16.2482,22.3178,29.5748,39.7020,
     47.5703,53.5342,62.2676,65.1222,71.5831,74.6670,79.2171,82.1897,
     88.6365,92.1710,93.5720,93.4320,97.6306]

NVARS = 7
NSAMPLES = np.shape(X1)[0]
NCONS = NSAMPLES



m = pyo.ConcreteModel()

setR = range(NCONS)

m.a = pyo.Var(bounds=(-100, 100))
m.b1 = pyo.Var(bounds=(-100, 100))
m.b2 = pyo.Var(bounds=(-100, 100))
m.c1 = pyo.Var(bounds=(-100, 100))
m.c2 = pyo.Var(bounds=(-100, 100))
m.d1 = pyo.Var(bounds=(-100, 100))
m.d2 = pyo.Var(bounds=(-100, 100))
m.Rd = pyo.Var(setR, bounds=(0, 100))
m.Re = pyo.Var(setR, bounds=(0, 100))

m.OBJ = pyo.Objective(expr=sum(m.Rd[k]+m.Re[k] for k in setR))

m.cons = pyo.ConstraintList()

for icon in setR:
    m.cons.add(cons_rule(icon))

opt = pyo.SolverFactory('Ipopt')

res = opt.solve(m)

print("Primals")
print(m.a, pyo.value(m.a), sep=' = ')
a = pyo.value(m.a)
print(m.b1, pyo.value(m.b1), sep=' = ')
b1 = pyo.value(m.b1)
print(m.b2, pyo.value(m.b2), sep=' = ')
b2 = pyo.value(m.b2)
print(m.c1, pyo.value(m.c1), sep=' = ')
c1 = pyo.value(m.c1)
print(m.c2, pyo.value(m.c2), sep=' = ')
c2 = pyo.value(m.c2)
print(m.d1, pyo.value(m.d1), sep=' = ')
d1 = pyo.value(m.d1)
print(m.cd2, pyo.value(m.d2), sep=' = ')
d2 = pyo.value(m.d2)
for k in setR:
    print(m.Rd[k], pyo.value(m.Rd[k]), sep=' = ')
for k in setR:
    print(m.Re[k], pyo.value(m.Re[k]), sep=' = ')

ax = plt.figure().add_subplot(projection='3d')
X1_lin = np.linspace(0,60,1000)
X2_lin = np.linspace(0,60,1000)
Z_lin = a + b1*X1_lin + b2*X2_lin +\
    c1*X1_lin**2 + c2*X2_lin**2 + \
        d1*X1_lin**3 + d2*X2_lin**3
plt.plot(X1, X2, Z, 'r*', zdir='z')
plt.plot(X1_lin, X2_lin, Z_lin, '-b', zdir='z')
plt.show()