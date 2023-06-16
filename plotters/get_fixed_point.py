from matplotlib import pyplot as plt
from numpy import loadtxt, transpose
from os import path
from tqdm import tqdm


def get_mean_ds(data_path, name):
    folder = path.join(data_path, name)
    cluster_ds_data = transpose(loadtxt(open(path.join(folder, name + '_cluster_ds.txt'), 'r')))
    mean_ds_data = cluster_ds_data[1]
    number_samples = cluster_ds_data[3]

    limit = 0
    for i in range(1, len(mean_ds_data)):
        if number_samples[i] < samples_threshold:
            limit = i
            break

    return range(1, limit), mean_ds_data[1:limit]


def get_fixed_point(cluster_ds):
    possible_fixed_points = []

    for i in range(lower_limit, len(cluster_ds) - 1):
        if cluster_ds[i - 1] * cluster_ds[i] < 0:
            possible_fixed_points.append(i)

    return sum(possible_fixed_points) / len(possible_fixed_points)


if __name__ == '__main__':
    results_path = path.join(path.dirname(path.dirname(__file__)), 'results')
    lower_limit = 5
    samples_threshold = 25000

    model = "tricritical"
    p = 0.42
    subfolder = "q0p75"
    dataset = "100x100_residue"
    data_path = path.join(results_path, model, subfolder, dataset)
    folder = str(p).replace('.', 'p')

    # model = "null_stochastic"
    # f = 0.53
    # data_path = path.join(results_path, model)
    # folder = str(f).replace('.', 'p')

    cluster_sizes, cluster_ds = get_mean_ds(data_path, folder)

    plt.plot(cluster_sizes, cluster_ds)
    plt.axhline(y=0, color='r', linestyle='-')
    plt.show()

    fixed_point = get_fixed_point(cluster_ds)
    print(fixed_point)