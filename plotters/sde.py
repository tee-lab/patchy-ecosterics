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
    results_path = path.join(path.dirname(path.dirname(__file__)), 'results')
    model = "tricritical"
    subfolder = "q0p5"
    dataset = "max_regime"

    data_path = path.join(results_path, model, subfolder, dataset)
    p_values = [0.5, 0.53, 0.55, 0.57]
    cluster_limits = [100, 1000, 4000, 5000]
    q = 0.5
    num_cols = len(p_values)

    plt.subplots(2, num_cols, figsize=(20, 10))

    for i in tqdm(range(num_cols)):
        col = i + 1
        p = p_values[i]
        limit = cluster_limits[i]
        name = str(p).replace('.', 'p')

        row = 0
        cluster_sizes, mean_ds = get_mean_ds(name, limit)
        plt.subplot(2, num_cols, row * num_cols + col)
        plt.title(f"p = {p}")
        plt.xlabel("Cluster Size")
        plt.ylabel("Mean |dS|")
        plt.plot(cluster_sizes, mean_ds)
        plt.plot([0, limit], [0, 0], 'k--')

        row = 1
        cluster_sizes, mean_ds_sq = get_mean_ds_sq(name, limit)
        plt.subplot(2, num_cols, row * num_cols + col)
        plt.xlabel("Cluster Size")
        plt.ylabel("Mean (dS^2)")
        plt.plot(cluster_sizes, mean_ds_sq)
    
    plt.savefig("cluster_sde.png")
    plt.show()