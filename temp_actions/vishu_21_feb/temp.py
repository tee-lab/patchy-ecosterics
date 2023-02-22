from matplotlib import pyplot as plt
from numpy import zeros
from os import path


if __name__ == '__main__':
    base_path = "C:\\Code\\Github\\vegetation-dynamics\\results\\tricritical\\q0\\alternate"
    p_value = 0.74
    file_prefix = str(p_value).replace('.', 'p')
    folder_path = path.join(base_path, file_prefix)
    output_path = path.dirname(__file__)

    cluster_ds_data = open(path.join(folder_path, file_prefix + '_cluster_ds.txt'), 'r').readlines()
    cluster_analyze_limit = 200
    mean_ds_values, mean_ds_sq_values, num_changes = zeros(cluster_analyze_limit), zeros(cluster_analyze_limit), zeros(cluster_analyze_limit)

    for i, line in enumerate(cluster_ds_data):
        cluster_size, ds_values = line.split(":")

        if int(cluster_size) == cluster_analyze_limit or ds_values == " \n":
            break

        ds_values = [int(ds) for ds in ds_values.strip().split(" ")]
        ds_sq_values = [ds ** 2 for ds in ds_values]
        mean_ds_values[i] = sum(ds_values) / len(ds_values)
        mean_ds_sq_values[i] = sum(ds_sq_values) / len(ds_sq_values)
        num_changes[i] = len(ds_values)

    bin_size = 5
    binned_ds = zeros(len(mean_ds_values) // bin_size)
    bins = zeros(len(binned_ds) + 1)

    for i in range(len(binned_ds)):
        binned_ds[i] = sum(mean_ds_values[i * bin_size:(i + 1) * bin_size]) / bin_size
        bins[i] = i * bin_size

    plt.figure()
    plt.title("Mean Cluster Change")
    plt.xlabel("Cluster Size")
    plt.ylabel("Mean dS")
    plt.plot(bins[:-1], binned_ds)
    plt.savefig(path.join(output_path, file_prefix + '_cluster_mean_ds.png'))
    plt.show()

    # plt.figure()
    # plt.title("Mean Cluster Change")
    # plt.xlabel("Cluster Size")
    # plt.ylabel("Mean dS")
    # plt.plot(range(cluster_analyze_limit), mean_ds_values)
    # plt.savefig(path.join(output_path, file_prefix + '_cluster_mean_ds.png'))
    # plt.show()

    # plt.figure()
    # plt.title("Mean Cluster Change Squared")
    # plt.xlabel("Cluster Size")
    # plt.ylabel("Mean dS^2")
    # plt.plot(range(cluster_analyze_limit), mean_ds_sq_values)
    # plt.savefig(path.join(output_path, file_prefix + '_cluster_mean_ds_sq.png'))
    # plt.show()

    # plt.figure()
    # plt.title("Number of Cluster Changes")
    # plt.xlabel("Cluster Size")
    # plt.ylabel("Number of Changes")
    # plt.plot(range(cluster_analyze_limit), num_changes)
    # plt.savefig(path.join(output_path, file_prefix + '_cluster_num_changes.png'))
    # plt.show()