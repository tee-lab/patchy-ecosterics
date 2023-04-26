from matplotlib import pyplot as plt
from numpy import loadtxt, transpose
from os import path
from tqdm import tqdm


def get_mean_ds(name, limit):
    folder = path.join(data_path, name)
    cluster_ds_data = transpose(loadtxt(open(path.join(folder, name + '_cluster_ds.txt'), 'r')))
    cluster_analyze_limit = min(limit, len(cluster_ds_data[0]))
    cluster_ds_data = cluster_ds_data[1]

    return range(cluster_analyze_limit), cluster_ds_data[:cluster_analyze_limit]


def get_mean_ds_sq(name, limit):
    folder = path.join(data_path, name)
    cluster_ds_data = transpose(loadtxt(open(path.join(folder, name + '_cluster_ds.txt'), 'r')))
    cluster_analyze_limit = min(limit, len(cluster_ds_data[0]))
    cluster_ds_data = cluster_ds_data[2]

    return range(cluster_analyze_limit), cluster_ds_data[:cluster_analyze_limit]


if __name__ == '__main__':
    ####################################
    # Tricritical Directed Percolation #
    ####################################
    results_path = path.join(path.dirname(path.dirname(__file__)), '..', 'results')
    model = "tricritical"
    dataset = "100x100"

    # q = 0
    # p_values = [0.65, 0.7, 0.72, 0.74]
    # cluster_limits = [100, 500, 4000, 6000]

    # q = 0.25
    # p_values = [0.6, 0.62, 0.65, 0.67]
    # cluster_limits = [100, 500, 4000, 6000]

    # q = 0.5
    # p_values = [0.5, 0.53, 0.55, 0.57]
    # cluster_limits = [100, 500, 4000, 6000]

    # q = 0.75
    # p_values = [0.405, 0.41, 0.42, 0.44]
    # cluster_limits = [200, 1000, 4000, 6000]

    # q = 0.92
    # p_values = [0.282, 0.283, 0.285, 0.29]
    # cluster_limits = [300, 1000, 4000, 6000]

    q = 0.92
    p = 0.282
    limit = 500

    subfolder = "q" + str(q).replace('.', 'p')
    data_path = path.join(results_path, model, subfolder, dataset)
    name = str(p).replace('.', 'p')

    cluster_sizes, mean_ds = get_mean_ds(name, limit)
    plt.title(f"Drift term for p = {p}, q = {q}", fontsize=14)
    plt.xlabel("s", fontsize=12)
    plt.ylabel("f(s)", fontsize=12)
    plt.plot(cluster_sizes[1:], mean_ds[1:])
    plt.plot([0, limit], [0, 0], 'k--')
    plt.savefig(f"p{p}_q{q}_f.png")
    plt.show()