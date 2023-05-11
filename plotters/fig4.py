from matplotlib import pyplot as plt
from math import sqrt
from numba import njit
from numpy import array, delete, histogram, loadtxt, transpose, zeros
from numpy.random import normal
from os import path
from tqdm import tqdm

from linear_regression import perform_linear_regression


def load_mean_ds_data(folder_path, file_name):
    cluster_ds_data = transpose(loadtxt(open(path.join(folder_path, file_name), 'r')))
    mean_ds_data, mean_ds_sq_data, number_samples = cluster_ds_data[1], cluster_ds_data[2], cluster_ds_data[3]

    limit = 0
    for i in range(len(mean_ds_data)):
        if number_samples[i] < samples_threshold:
            limit = i
            break

    return array(range(1, limit)), mean_ds_data[1:limit], mean_ds_sq_data[1:limit]


@njit(fastmath=True)
def simulate(time_series):
    size = 10

    for i in range(num_steps):
        time_series[i] = size
        drift = a * size - b * size ** 2 + c
        diffusion = sqrt(noise_slope * size) * normal()
        size += (drift * dt + diffusion * sqrt_dt)

        if size < 0:
            size = 1


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


if __name__ == '__main__':
    results_path = path.join(path.dirname(__file__), "..", "results")
    samples_threshold = 25000

    simulation_time = 10000
    dt = 0.01
    sqrt_dt = sqrt(dt)
    num_steps = int(simulation_time / dt)

    models = []
    model_names = []
    model_params = []
    model_densities = []
    model_datasets = []
    model_variables = []
    model_approximations = []

    models.append(path.join("tricritical", "q0"))
    model_names.append("TDP across q = 0")
    model_datasets.append("100x100_new")
    model_params.append([0.64, 0.66, 0.68])
    model_variables.append("p")
    model_approximations.append(["linear", "linear", "logistic"])
    
    models.append(path.join("tricritical", "q0p5"))
    model_names.append("TDP across q = 0.5")
    model_datasets.append("100x100")
    model_params.append([0.5, 0.51, 0.52])
    model_variables.append("p")
    model_approximations.append(["linear", "linear", "logistic"])

    title_size = "xx-large"
    label_size = "x-large"
    tick_size = "x-large"
    legend_size = "x-large"

    num_rows = len(models)
    num_cols = len(model_params[0])
    plt.subplots(num_rows, num_cols, figsize=(num_cols * 6, num_rows * 4))

    for i in tqdm(range(len(models))):
        row = i
        model = models[i]
        model_name = model_names[i]
        model_dataset = model_datasets[i]
        model_param = model_params[i]
        model_variable = model_variables[i]
        model_approximation = model_approximations[i]

        dataset_path = path.join(results_path, model, model_dataset)

        # dynamics plots
        for j in range(len(model_param)):
            file_prefix = str(model_param[j]).replace(".", "p")
            folder_path = path.join(dataset_path, file_prefix)
            
            # plot actual csd
            file_name = file_prefix + "_cluster_distribution.txt"
            cluster_sizes, inverse_cdf = get_cluster_distribution(folder_path, file_name)

            plt.subplot(num_rows, num_cols, row * num_cols + j + 1)
            if row == 0:
                plt.title("Self consistency check", fontsize=title_size)
            plt.loglog(cluster_sizes, inverse_cdf, label=f"Spatial simulation ({model_variable} = {model_param[j]})")

            # self consistency part
            approximation = model_approximation[j]
            file_name = file_prefix + "_cluster_ds.txt"
            cluster_sizes, cluster_ds, cluster_ds_sq = load_mean_ds_data(folder_path, file_name)
            data_length = len(cluster_sizes)

            # fit model to f(s)
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

                max_x = fixed_point / 2
                max_value = a * max_x - b * max_x ** 2 + c
                scaling_constant = max(cluster_ds) / max_value

                a *= scaling_constant
                b *= scaling_constant
                c *= scaling_constant
            else:
                slope, intercept, _ = perform_linear_regression(cluster_sizes, cluster_ds)
                a = slope
                b = 0
                c = intercept

            # simulate sde
            time_series = zeros(num_steps, dtype=float)
            simulate(time_series) 
            hist, bins = histogram(time_series, bins=range(0, int(max(time_series)) + 1))
            hist = hist / sum(hist)
            inverse_cdf = zeros(len(hist))
            for i in range(len(hist)):
                inverse_cdf[i] = sum(hist[i:])

            # plot csd from sde simulation
            plt.loglog(bins[:-1], inverse_cdf, label="SDE simulation")

            plt.ylim(10 ** -5, 1)
            if j == 0:
                plt.xlim(1, 10 ** 2.5)
            elif j == 1:
                plt.xlim(1, 10 ** 3)
            else:
                plt.xlim(1, 10 ** 3.5)

            if row != num_rows - 1:
                plt.xticks([])
            else:
                plt.xticks(fontsize=tick_size)
            if j != 0:
                plt.yticks([])
            else:
                plt.yticks(fontsize=tick_size)
            
            if row == num_rows - 1:
                plt.xlabel("Cluster size s", fontsize=label_size)
            if j == 0:
                plt.ylabel("P(S > s)", fontsize=label_size)

            plt.legend()

    plt.savefig("fig4.png", bbox_inches="tight")
    plt.show()