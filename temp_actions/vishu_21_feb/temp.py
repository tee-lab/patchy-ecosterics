from matplotlib import pyplot as plt
from numpy import loadtxt, transpose, zeros
from os import path


if __name__ == '__main__':
    base_path = "C:\\Code\\Github\\vegetation-dynamics\\results\\tricritical\\q0\\longer"
    p_value = 0.7
    file_prefix = str(p_value).replace('.', 'p')
    folder_path = path.join(base_path, file_prefix)
    output_path = path.dirname(__file__)

    cluster_ds_data = transpose(loadtxt(open(path.join(folder_path, file_prefix + '_cluster_ds.txt'), 'r')))
    cluster_analyze_limit = min(200, len(cluster_ds_data[0]))
    cluster_ds_data = cluster_ds_data[:, :cluster_analyze_limit]

    mean_ds_values = cluster_ds_data[1]
    bin_size = 5
    binned_ds = zeros(len(mean_ds_values) // bin_size)
    bins = zeros(len(mean_ds_values) // bin_size)

    for i in range(len(binned_ds)):
        binned_ds[i] = sum(mean_ds_values[i * bin_size:(i + 1) * bin_size]) / bin_size
        bins[i] = i * bin_size

    plt.figure()
    plt.title("Mean Cluster Change")
    plt.xlabel("Cluster Size")
    plt.ylabel("Mean dS")
    plt.plot(bins, binned_ds)
    plt.savefig(path.join(output_path, file_prefix + '_cluster_mean_ds.png'))
    plt.show()