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
    # results_path = path.join(path.dirname(path.dirname(__file__)), 'results')
    # model = "tricritical"
    # dataset = "100x100_2"

    # q = 0
    # p_values = [0.65, 0.7, 0.72, 0.74]
    # cluster_limits = [100, 500, 4000, 6000]

    # # q = 0.5
    # # p_values = [0.5, 0.53, 0.55, 0.57]
    # # cluster_limits = [100, 1000, 4000, 5000]

    # # q = 0.92
    # # p_values = [0.28, 0.285, 0.29, 0.31]
    # # cluster_limits = [1000, 1000, 1000, 1000]

    # subfolder = "q" + str(q).replace('.', 'p')
    # data_path = path.join(results_path, model, subfolder, dataset)

    # num_cols = len(p_values)
    # plt.subplots(2, num_cols, figsize=(20, 10))

    # for i in tqdm(range(num_cols)):
    #     col = i + 1
    #     p = p_values[i]
    #     limit = cluster_limits[i]
    #     name = str(p).replace('.', 'p')

    #     row = 0
    #     cluster_sizes, mean_ds = get_mean_ds(name, limit)
    #     plt.subplot(2, num_cols, row * num_cols + col)
    #     plt.title(f"p = {p}")
    #     plt.xlabel("Cluster Size")

    #     if col == 1:
    #         plt.ylabel("Mean dS")
    #     plt.plot(cluster_sizes, mean_ds)
    #     plt.plot([0, limit], [0, 0], 'k--')

    #     row = 1
    #     cluster_sizes, mean_ds_sq = get_mean_ds_sq(name, limit)
    #     plt.subplot(2, num_cols, row * num_cols + col)
    #     plt.xlabel("Cluster Size")

    #     if col == 1:
    #         plt.ylabel("Mean (dS^2)")
    #     plt.plot(cluster_sizes, mean_ds_sq)
    
    # plt.savefig(subfolder + "_cluster_sde.png")
    # plt.show()

    ####################
    # Scanlon Kalahari #
    ####################
    results_path = path.join(path.dirname(path.dirname(__file__)), 'results')
    model = "scanlon_kalahari"
    dataset = "100x100"
    rainfall_values = [300, 500, 700, 900]
    cluster_limits = [100, 500, 1000, 2000]

    data_path = path.join(results_path, model, dataset)

    num_cols = len(rainfall_values)
    plt.subplots(2, num_cols, figsize=(20, 10))

    for i in tqdm(range(num_cols)):
        col = i + 1
        rainfall = rainfall_values[i]
        limit = cluster_limits[i]
        name = str(rainfall).replace('.', 'p')

        row = 0
        cluster_sizes, mean_ds = get_mean_ds(name, limit)
        plt.subplot(2, num_cols, row * num_cols + col)
        plt.title(f"Rainfall = {rainfall}")
        plt.xlabel("Cluster Size")

        if col == 1:
            plt.ylabel("Mean dS")
        plt.plot(cluster_sizes, mean_ds)
        plt.plot([0, limit], [0, 0], 'k--')

        row = 1
        cluster_sizes, mean_ds_sq = get_mean_ds_sq(name, limit)
        plt.subplot(2, num_cols, row * num_cols + col)
        plt.xlabel("Cluster Size")

        if col == 1:
            plt.ylabel("Mean (dS^2)")
        plt.plot(cluster_sizes, mean_ds_sq)
    
    plt.savefig("scanlon_cluster_sde.png")
    plt.show()