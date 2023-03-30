from matplotlib import pyplot as plt
from numba import njit
from numpy import arange
from tqdm import tqdm


@njit
def x_dot(x, r, k):
    g = r * x * (1 - x / k)
    p = x / (1 + x ** 2)
    return g - p


@njit
def simulate(x0, r, k):
    x = x0
    for _ in range(time):
        x += x_dot(x, r, k)
    return x


if __name__ == '__main__':
    time = 1000

    k = 10
    r_range = arange(0, 2, 0.01)
    x_range = arange(0, 1, 0.01)

    pop_scatter = []
    r_scatter = []

    for r in tqdm(r_range):
        fixed_points = [simulate(x * k, r, k) for x in x_range]
        for x in fixed_points:
            pop_scatter.append(x / k)
            r_scatter.append(r)

    plt.title('Bifurcation Diagram')
    plt.xlabel('r')
    plt.ylabel('Population capacity (x/k)')
    plt.scatter(r_scatter, pop_scatter, s=0.1)
    plt.show()