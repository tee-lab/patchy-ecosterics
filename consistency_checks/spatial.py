from matplotlib import pyplot as plt
from math import sqrt
from numpy import array, loadtxt, transpose, zeros
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
    for i in range(len(mean_ds_data)):
        if number_samples[i] < samples_threshold:
            limit = i
            break

    return array(range(1, limit)), mean_ds_data[1:limit], mean_ds_sq_data[1:limit]


if __name__ == '__main__':
    q = 0
    p = 0.7
    lattice_size = 100
    samples_threshold = 50000
    # approximation = "linear"
    approximation = "logistic"

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

    plt.title(f"Drift term approximation for (p, q) = ({p}, {q})")
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

    simulation_time = 500
    dt = 0.1
    sqrt_dt = sqrt(dt)
    num_steps = int(simulation_time / dt)

    init_cluster_sizes = get_random_cluster_sizes(lattice_size)

    cluster_sizes = init_cluster_sizes.copy()
    num_clusters = len(cluster_sizes)
    print(f"Number of clusters: {num_clusters}")

    num_interventions = 0
    for _ in tqdm(range(num_steps)):
        # print(cluster_sizes[0])

        for i in range(num_clusters):
            drift = a * cluster_sizes[i] - b * cluster_sizes[i] ** 2 + c
            diffusion = sqrt(noise_slope * cluster_sizes[i]) * normal()
            cluster_sizes[i] += (drift * dt + diffusion * sqrt_dt)

            if cluster_sizes[i] <= 0:
                num_interventions += 1

                # cluster_sizes[i] = 0
                cluster_sizes[i] = choice(init_cluster_sizes, 1)[0]

    print(f"Number of interventions: {num_interventions}")
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
    plt.loglog(range(1, len(pdf) + 1), inverse_cdf, label="inverse cdf")
    plt.savefig(f"spatial.png")
    plt.show()