from numpy import arange, array, dot, ones, transpose, zeros
from numpy.random import random
from scipy.optimize import minimize


def get_cost(w, *args):
    x, y = args
    return sum((dot(x, w) - y) ** 2)


def get_grad(w, *args):
    x, y = args
    m, degree = len(x), len(w) - 1
    return sum(2 * ((dot(x, w) - y) @ ones((m, degree + 1))) * x)


if __name__ == '__main__':
    degree = 2
    x_vals = arange(0, 1, 0.0001)
    poly_func = lambda x: 1 + 2 * x + 3 * x * x
    y_vals = poly_func(x_vals)

    X = []
    for i in range(len(x_vals)):
        X.append([x_vals[i] ** j for j in range(degree + 1)])

    w = random(degree + 1)

    res = minimize(get_cost, w, args=(X, y_vals), jac=get_grad, method='Nelder-Mead')
    print(res)