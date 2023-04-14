from matplotlib import pyplot as plt
from numpy import loadtxt, transpose
from os import path
from tqdm import tqdm


def get_mean_ds(name):
    folder = path.join(data_path, name)
    cluster_ds_data = transpose(loadtxt(open(path.join(folder, name + '_cluster_ds.txt'), 'r')))
    mean_ds_data = cluster_ds_data[1]
    number_samples = cluster_ds_data[3]

    limit = 0
    for i in range(len(mean_ds_data)):
        if number_samples[i] < samples_threshold:
            limit = i
            break

    return range(limit), mean_ds_data[:limit]


if __name__ == '__main__':
    results_path = path.join(path.dirname(path.dirname(__file__)), 'results')
    model = "tricritical"
    dataset = "100x100"
    lower_limit = 5
    samples_threshold = 25000

    # q = 0
    # p_values = [round(0.63 + 0.01 * i, 2) for i in range(0, 10)]
    # percolation_threshold = 0.72
    # critical_threshold = 0.62

    # q = 0.25
    # p_values = [round(0.58 + 0.01 * i, 2) for i in range(0, 8)]
    # percolation_threshold = 0.65
    # critical_threshold = 0.57

    q = 0.5
    p_values = [round(0.51 + 0.01 * i, 2) for i in range(0, 5)]
    percolation_threshold = 0.55
    critical_threshold = 0.5

    subfolder = "q" + str(q).replace('.', 'p')
    data_path = path.join(results_path, model, subfolder, dataset)
    fixed_points = []

    for i in tqdm(range(len(p_values))):
        p = p_values[i]
        folder_name= str(p).replace('.', 'p')

        cluster_sizes, cluster_ds = get_mean_ds(folder_name)
        possible_fixed_points = []

        for i in range(lower_limit, len(cluster_ds) - 1):
            if cluster_ds[i - 1] * cluster_ds[i] < 0:
                possible_fixed_points.append(i)

        fixed_point = sum(possible_fixed_points) / len(possible_fixed_points)
        fixed_points.append(fixed_point)

    plt.title("Decrease in critical cluster size")
    plt.xlabel("p")
    plt.ylabel("Critial cluster size")
    plt.plot(p_values, fixed_points)
    plt.axvline(percolation_threshold, color='b', linestyle='--', label='Percolation threshold')
    plt.axvline(critical_threshold, color='r', linestyle='--', label='Critical threshold')
    plt.legend()
    plt.savefig(f"q{str(q).replace('.', 'p')}_ews3_fp.png")
    plt.show()