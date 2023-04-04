# Newton Metodh
import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return -1.5*x**6-2*x**4+12*x


def df(x):
    h = 0.0001
    return (f(x+h)-f(x))/h


x = np.linspace(-1,2,1000)
plt.plot(x,f(x))
plt.grid()

x = 2  # Initial guest
MAXITER = 1000
TOL = 1e-12

plt.plot(x,f(x), '*r')

for iter in range(MAXITER):
    x_old = x
    print('Iteration: ', iter+1)
    x = x - f(x)/df(x)
    print('x = ', x)
    plt.plot(x,f(x), '*r')

    # Stop Criterion
    if np.abs(x-x_old) < TOL:
        break


plt.show()