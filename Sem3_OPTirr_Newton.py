# Newton's Metodh
import numpy as np
import matplotlib.pyplot as plt


# Function
def f(x):
    return -1.5*x**6-2*x**4+12*x


# Numerical first derivative
def df(x):
    h = 0.0001
    return (f(x+h)-f(x))/h


# Numerical second derivative
def ddf(x):
    h = 0.0001
    return (f(x+h)-2*f(x)+f(x-h))/h**2


# Parameters
MAXITER = 1000
TOL = 1e-12

# Algorithm step
t = 1

# Initial guest
x = 8

# For graphic purposes
x_graph = np.linspace(-1,2,1000)
plt.plot(x_graph,f(x_graph))
plt.grid()
if x <= 2:
    plt.plot(x,f(x), '*r')

# Evaluating convexity
if ddf(x) >= 0:
    print('positive convexity')
else:
    print('negative convexity')

if df(x)>=0:
    is_asc = True
else:
    is_asc = False

# Newton's method
for iter in range(MAXITER):
    # Old point
    x_old = x
    print('Iteration: ', iter+1)

    # New point
    x = x-t*df(x)/ddf(x)
    print('x = ', x)
    print('dfx = ', df(x))

    # Plot new point
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

# Plot graphic
plt.show()