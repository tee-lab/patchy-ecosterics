from matplotlib import pyplot as plt
from math import sqrt
from numba import njit
from numpy import array, delete, loadtxt, polyfit, transpose, zeros
from numpy.random import choice, normal, randint
from os import path
from skimage.measure import label
from tqdm import tqdm

from linear_regression import perform_linear_regression


def get_random_cluster_sizes(lattice_size = 100):
    lattice = randint(0, 2, (lattice_size, lattice_size))
    labelled_lattice = label(lattice, background=0, connectivity=1)

    cluster_sizes = []
    for i in range(1, labelled_lattice.max() + 1):
        cluster_sizes.append(len(labelled_lattice[labelled_lattice == i]))

    return array(cluster_sizes, dtype=float)


def load_mean_ds_data(folder_name):
    folder = path.join(data_path, folder_name)
    cluster_ds_data = transpose(loadtxt(open(path.join(folder, folder_name + '_cluster_ds.txt'), 'r')))
    mean_ds_data, mean_ds_sq_data, number_samples = cluster_ds_data[1], cluster_ds_data[2], cluster_ds_data[3]

    limit = 0
    for i in range(1, len(mean_ds_data)):
        if number_samples[i] < samples_threshold:
            limit = i
            break

    return array(range(1, limit)), mean_ds_data[1:limit], mean_ds_sq_data[1:limit]


def get_cluster_distribution(folder_path, file_name):
    file_path = path.join(folder_path, file_name)
    cluster_distribution_data = transpose(loadtxt(open(file_path, 'r')))
    cluster_sizes, num = cluster_distribution_data[0][1:], cluster_distribution_data[1][1:]

    inverse_cdf = zeros(len(num))
    for i in range(len(num)):
        inverse_cdf[i] = sum(num[i:])
    inverse_cdf = inverse_cdf / sum(num)

    remove_indices = []
    for i in range(len(cluster_sizes) - 1):
        if inverse_cdf[i] == inverse_cdf[i + 1]:
            remove_indices.append(i)

    cluster_sizes = delete(cluster_sizes, remove_indices)
    inverse_cdf = delete(inverse_cdf, remove_indices)

    return cluster_sizes, inverse_cdf


def construct_drift_function(params, approximation):
    if approximation == "logistic_sqrt":
        a, b, c = params
        @njit(fastmath=True)
        def drift_function(size):
            return a * sqrt(size) - b * size + c
        return drift_function
    
    elif approximation == "logistic":
        a, b, c = params
        @njit(fastmath=True)
        def drift_function(size):
            return a * size - b * size ** 2 + c
        return drift_function

    elif approximation == "poly":
        @njit(fastmath=True)
        def drift_function(size):
            return sum([params[deg] * size ** deg for deg in range(len(params))])
        return drift_function

    elif approximation == "linear":
        a, b, c = params
        @njit(fastmath=True)
        def drift_function(size):
            return a * size + c
        return drift_function


@njit(fastmath=True)
def simulate(cluster_sizes, drift_function):
    for i in range(num_steps):
        for j in range(len(cluster_sizes)):
            drift = drift_function(cluster_sizes[j])
            diffusion = sqrt(noise_slope * cluster_sizes[j]) * normal()
            cluster_sizes[j] += (drift * dt + diffusion * sqrt_dt)

            if cluster_sizes[j] <= 0:
                cluster_sizes[j] = 1

    return cluster_sizes


if __name__ == '__main__':
    q = 0
    p = 0.7
    lattice_size = 100
    samples_threshold = 50000
    approximation = "logistic"

    results_path = path.join(path.dirname(__file__), "..", 'results')
    model = "tricritical"
    dataset = "100x100_new"
    subfolder = "q" + str(q).replace('.', 'p')
    folder_name = str(p).replace('.', 'p')
    data_path = path.join(results_path, model, subfolder, dataset)

    cluster_sizes, cluster_ds, cluster_ds_sq = load_mean_ds_data(folder_name)
    data_length = len(cluster_sizes)

    noise_slope = (cluster_ds_sq[-1] - cluster_ds_sq[0]) / (cluster_sizes[-1] - cluster_sizes[0])

    possible_fixed_points = []
    for i in range(1, len(cluster_ds) - 1):
        if cluster_ds[i - 1] * cluster_ds[i] < 0:
            possible_fixed_points.append(i)

    fixed_point = sum(possible_fixed_points) / len(possible_fixed_points)

    # dx/dt = ax - bx^2 + c
    a, b, c = 0, 0, 0

    if approximation == "logistic":
        a = fixed_point
        b = 1
        c = 0
        params = [a, b, c]

        drift_function = construct_drift_function(params, approximation)

        max_x = fixed_point / 2
        max_value = drift_function(max_x)
        scaling_constant = max(cluster_ds) / max_value

        a *= scaling_constant
        b *= scaling_constant
        c *= scaling_constant
        params = [a, b, c]

        drift_function = construct_drift_function(params, approximation)
    elif approximation == "logistic_sqrt":
        a = sqrt(fixed_point)
        b = 1
        c = 0
        params = [a, b, c]

        drift_function = construct_drift_function(params, approximation)

        max_x = (a / (2 * b)) ** 2
        max_value = drift_function(max_x)
        scaling_constant = max(cluster_ds) / max_value

        a *= scaling_constant
        b *= scaling_constant
        c *= scaling_constant
        params = [a, b, c]

        drift_function = construct_drift_function(params, approximation)
    elif approximation == "poly":
        params = polyfit(cluster_sizes, cluster_ds, 6)
        params = array(list(reversed(params)))
        drift_function = construct_drift_function(params, approximation)
    elif approximation == "linear":
        slope, intercept, _ = perform_linear_regression(cluster_sizes, cluster_ds)
        a = slope
        b = 0
        c = intercept
        params = [a, b, c]

        drift_function = construct_drift_function(params, approximation)

    plt.title(f"Drift term approximation ({approximation}) for (p, q) = ({p}, {q})")
    plt.xlabel("Cluster size s")
    plt.ylabel("$f(s)$")
    plt.plot(cluster_sizes, cluster_ds, label="data")
    plt.plot(cluster_sizes, a * cluster_sizes - b * cluster_sizes ** 2 + c, label="fit")   
    plt.plot(range(data_length), [0] * data_length, '--')
    plt.legend()
    plt.show()

    plt.title(f"Diffusion term approximation for (p, q) = ({p}, {q})")
    plt.xlabel("Cluster size s")
    plt.ylabel("$g^2(s)$")
    plt.plot(cluster_sizes, cluster_ds_sq, label="data")
    plt.plot(cluster_sizes, noise_slope * cluster_sizes, label="fit")
    plt.plot(range(data_length), [0] * data_length, '--')
    plt.legend()
    plt.show()

    simulation_time = 1000
    dt = 0.01
    sqrt_dt = sqrt(dt)
    num_steps = int(simulation_time / dt)

    init_cluster_sizes = get_random_cluster_sizes(lattice_size)

    cluster_sizes = init_cluster_sizes.copy()
    num_clusters = len(cluster_sizes)
    cluster_sizes = simulate(cluster_sizes, drift_function)

    print(cluster_sizes)

    pdf = zeros(int(max(cluster_sizes)) + 1)
    for i in range(num_clusters):
        pdf[int(cluster_sizes[i])] += 1
    pdf /= sum(pdf)

    inverse_cdf = zeros(len(pdf))
    for i in range(len(pdf)):
        inverse_cdf[i] = sum(pdf[i:])
    
    plt.title(f"Cluster size distribution for (p, q) = ({p}, {q})")
    plt.xlabel("Cluster size s")
    plt.ylabel("P(S > s)")
    plt.loglog(range(1, len(pdf) + 1), inverse_cdf, label="SDE simulation")

    cluster_sizes, inverse_cdf = get_cluster_distribution(path.join(data_path, folder_name), f"{folder_name}_cluster_distribution.txt")
    plt.loglog(cluster_sizes, inverse_cdf, label="actual data")
    plt.legend()
    plt.savefig(f"spatial.png")
    plt.show()