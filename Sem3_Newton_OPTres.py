# Newton Metodh
import numpy as np
import numdifftools as nd

# Lagragian function
def L(var):
    x = var[0]
    y = var[1]
    s1 = var[2]
    s2 = var[3]
    lbd1 = var[4]
    lbd2 = var[5]
    return (
        np.exp(x) * (4 * x**2 + 2 * y**2 + 4 * x * y + 2 * y + 1)
        - lbd1 * (x * y - s1**2 + 10)
        + lbd2 * (x * y - x - y + s2**2 + 1.5)
    )


J = nd.Jacobian(L)
H = nd.Hessian(L)

# Initial guest
x = np.array([-20, 20, 0, 0, 1, 1])

TOL = 1e-12
for iter in range(100):
    # Jacobian in x
    J_in_x = J(x).reshape(-1, 1)

    # Stop crietrion
    err = np.max(np.abs(J_in_x))
    print("iter:", iter, "| Error:", err)
    print("x =",x[0],'| y =',x[1])
    print("lbd1 =",x[4],"| lbd2 =",x[5])
    if err < TOL:
        break

    # Hessian in x
    H_in_x = H(x)

    # New x
    delta_x = np.dot(-np.linalg.inv(H_in_x), J_in_x).flatten()
    x = x + delta_x
