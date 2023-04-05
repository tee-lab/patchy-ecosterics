from matplotlib import pyplot as plt
from numba import njit
from numpy import array, arange, zeros
from numpy.random import normal
from scipy.stats import skew
from tqdm import tqdm


@njit
def x_dot(x, r, k):
    g = r * x * (1 - x / k)
    p = x / (1 + x ** 2)
    return g - p


def simulate(x0, r, k):
    x_values = zeros(eq_time + simul_time)
    x_values[0] = x0

    for i in range(eq_time):
        x_values[i + 1] = x_values[i] + x_dot(x_values[i], r, k)

    for i in range(simul_time - 1):
        x_values[i + eq_time + 1] = x_values[i + eq_time] + x_dot(x_values[i + eq_time], r, k) + normal(0, noise)

    return x_values


if __name__ == '__main__':
    eq_time = 1000
    simul_time = 10000

    k = 4
    r_values = array([0.4, 0.43, 0.46, 0.5, 0.53, 0.56])
    noise = 0.05

    variances = zeros(len(r_values))
    skewnesses = zeros(len(r_values))

    plt.subplots(figsize=(15, 7))
    num_rows = 2
    num_cols = len(r_values) // num_rows

    for i, r in enumerate(tqdm(r_values)):
        population = simulate(k, r, k)
        stochastic_population = population[eq_time:]

        mean = stochastic_population.mean()
        variances[i] = stochastic_population.var()
        skewnesses[i] = skew(stochastic_population)\
        
        row = i // num_cols
        col = i % num_cols
        plt.subplot(num_rows, num_cols, i + 1)

        if row == num_rows - 1:
            plt.xlabel("Time")
        if col == 0:
            plt.ylabel("Population")

        plt.plot(stochastic_population, label=f'r = {r:.2f}')
        plt.axhline(mean, color='black', linestyle='--', label=f'mean = {mean:.2f}')
        plt.legend()

    plt.legend()
    plt.savefig("critical_slowing_down.png", bbox_inches='tight')
    plt.show()

    plt.title("Increase in variance with stress")
    plt.plot(1 - r_values, variances)
    plt.xlabel("Stress (1 - r)")
    plt.ylabel("Variance")
    plt.savefig("variance.png", bbox_inches='tight')
    plt.show()