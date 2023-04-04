# Newton Metodh
import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return -1.5*x**6-2*x**4+12*x


def df(x):
    h = 0.0001
    return (f(x+h)-f(x))/h

def ddf(x):
    h = 0.0001
    return (f(x+h)-2*f(x)+f(x-h))/h**2


x = np.linspace(-1,2,1000)
plt.plot(x,f(x))
plt.grid()

# Method parameters
MAXITER = 1000
TOL = 1e-12

# Initial guest
x = 8

# Evaluating convexity
if ddf(x) >= 0:
    t = 1
else:
    t = -1

if df(x)>=0:
    is_asc = True
else:
    is_asc = False

if x <= 2:
    plt.plot(x,f(x), '*r')

for iter in range(MAXITER):
    x_old = x
    print('Iteration: ', iter+1)
    x = x +t*df(x)/ddf(x)
    print('x = ', x)
    print('dfx = ', df(x))
    if x <= 2:
        plt.plot(x,f(x), '*r')

    # Stop Criterion
    if np.abs(df(x)) < TOL:
        break

    # Reducing t
    if df(x)<=0 and is_asc:
        is_asc = False
        t = t/10
    elif df(x)>0 and not is_asc:
        is_asc = True
        t = t/10
        

plt.show()