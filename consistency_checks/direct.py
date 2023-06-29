from matplotlib import pyplot as plt
from math import sqrt
from numba import njit
from numpy import array, histogram, loadtxt, transpose, zeros
from numpy.random import choice, normal, randint
from os import path
from skimage.measure import label
from tqdm import tqdm

from utils import perform_linear_regression


def load_mean_ds_data(folder_name):
    folder = path.join(data_path, folder_name)
    cluster_ds_data = transpose(loadtxt(open(path.join(folder, folder_name + '_cluster_ds.txt'), 'r')))
    mean_ds_data, mean_ds_sq_data, number_samples = cluster_ds_data[1], cluster_ds_data[2], cluster_ds_data[3]

    limit = 0
    for i in range(len(mean_ds_data)):
        if number_samples[i] < samples_threshold:
            limit = i
            break

    return array(range(1, limit)), mean_ds_data[1:limit], mean_ds_sq_data[1:limit]


if __name__ == '__main__':
    q = 0
    p = 0.7
    samples_threshold = 50000

    results_path = path.join(path.dirname(__file__), "..", 'results')
    model = "tricritical"
    dataset = "100x100"
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
    print("Fixed point =", fixed_point)

    slope, intercept, _ = perform_linear_regression(cluster_sizes[data_length // 2:], cluster_ds[data_length // 2:])

    plt.title(f"Drift term approximation for (p, q) = ({p}, {q})")
    plt.xlabel("Cluster size s")
    plt.ylabel("$f(s)$")
    plt.plot(cluster_sizes, cluster_ds, label="data")
    plt.plot(cluster_sizes, slope * cluster_sizes + intercept, label="fit")   
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

    simulation_time = 10000
    dt = 0.01
    sqrt_dt = sqrt(dt)
    num_steps = int(simulation_time / dt)

    time_series = zeros(num_steps, dtype=float)
    size = 10

    for i in range(num_steps):
        time_series[i] = size
        
        if size < data_length:
            drift = cluster_ds[int(size)]
            diffusion = sqrt(cluster_ds_sq[int(size)]) * normal()
        else:
            drift = slope * size + intercept
            diffusion = sqrt(noise_slope * size) * normal()

        size += drift * dt + diffusion * sqrt_dt

        if size < 0:
            size = 0

    plt.title(f"Time series for (p, q) = ({p}, {q})")
    plt.xlabel("Time")
    plt.ylabel("Cluster size")
    plt.plot(range(num_steps), time_series)
    plt.show()

    hist, bins = histogram(time_series, bins=range(0, int(max(time_series)) + 1))
    
    plt.title(f"Histogram for time series of (p, q) = ({p}, {q})")
    plt.xlabel("Cluster size")
    plt.ylabel("Frequency")
    plt.loglog(bins[:-1], hist)
    plt.savefig("direct.png")
    plt.show()