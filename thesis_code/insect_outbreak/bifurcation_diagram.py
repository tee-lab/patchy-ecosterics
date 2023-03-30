from matplotlib import pyplot as plt
from numba import njit
from numpy import arange
from tqdm import tqdm


def get_function(r, k):
    def x_dot(x):
        g = r * x * (1 - x / k)
        p = x / (1 + x ** 2)
        return g - p

    return x_dot


def binary_search(f, lower, upper):
    while upper - lower > tol:
        mid = (lower + upper) / 2
        if f(lower) * f(mid) < 0:
            upper = mid
        else:
            lower = mid
    return (lower + upper) / 2


def find_roots(r, k):
    equation = get_function(r, k)
    roots = []
    
    for interval in range(num_intervals):
        lower_x, upper_x = (interval - 1) / num_intervals, (interval + 1) / num_intervals
        lower_pop, upper_pop = lower_x * k, upper_x * k

        if equation(lower_pop) * equation(upper_pop) < 0:
            root = binary_search(equation, lower_pop, upper_pop)
            if equation(upper_pop) < 0 and equation(lower_pop) > 0:
                roots.append({'root': root, 'type': 'stable'})
            elif equation(upper_pop) > 0 and equation(lower_pop) < 0:
                roots.append({'root': root, 'type': 'unstable'})

    return roots


if __name__ == '__main__':
    # root finding
    tol = 1e-12
    num_intervals = 100

    k_range = arange(1, 10, 1)
    r_range = arange(0, 1.5, 0.001)

    for k in tqdm(k_range):
        stable_r = []
        unstable_r = []
        stable_roots = []
        unstable_roots = []
        
        for r in r_range:
            roots = find_roots(r, k)
            for root in roots:
                if root['type'] == 'stable':
                    stable_r.append(r)
                    stable_roots.append(root['root'] / k)
                else:
                    unstable_r.append(r)
                    unstable_roots.append(root['root'] / k)

        plt.figure()
        plt.title(f'Bifurcation Diagram across k = {k}')
        plt.xlabel('r')
        plt.ylabel('Population capacity (x/k)')
        plt.scatter(stable_r, stable_roots, c='b', label='Stable fixed points')
        plt.scatter(unstable_r, unstable_roots, c='r', label='Unstable fixed points')
        plt.ylim(0, 1)
        plt.legend(loc='upper left')
        plt.savefig(f'k_{k}.png')