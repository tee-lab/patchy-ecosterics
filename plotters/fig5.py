from matplotlib import pyplot as plt
from os import path
from tqdm import tqdm


def load_residue_data(file_path, file_name, cluster_size):
    residue_data = open(path.join(file_path, file_name), "r").readlines()

    for data in residue_data[:-1]:
        size, bins, freq = data.split(':')
        min_bin, max_bin = bins.split(',')
        freqs = list(map(int, freq.split(',')))

        if int(size) == cluster_size:
            zero_index = -int(min_bin) if int(min_bin) < 0 else int(min_bin)
            freqs = freqs[zero_index:]
            residues = range(0, len(freqs))

            return residues, freqs
        

if __name__ == '__main__':
    results_path = path.join(path.dirname(__file__), "..", "results")
    cluster_sizes = [10, 50, 100]

    models = []
    model_names = []
    model_params = []
    model_densities = []
    model_datasets = []

    models.append(path.join("tricritical", "q0"))
    model_names.append("Contact Process")
    model_params.append(0.7)
    model_densities.append(0.48)
    model_datasets.append("100x100_residue")

    models.append(path.join("tricritical", "q0p5"))
    model_names.append("TDP (q = 0.5)")
    model_params.append(0.53)
    model_densities.append(0.43)
    model_datasets.append("100x100_residue")

    models.append(path.join("scanlon_kalahari"))
    model_names.append("Scanlon")
    model_params.append(700)
    model_densities.append(0.43)
    model_datasets.append("100x100_residue")

    num_cols = len(cluster_sizes)
    num_rows = len(models)

    title_size = 14
    label_size = 12
    tick_size = 10
    legend_size = 10

    num_rows = len(models)
    num_cols = len(cluster_sizes)
    plt.subplots(num_rows, num_cols, figsize=(8.27, 8.27 * num_rows / num_cols))
    plt.suptitle("Distribution of residues", fontsize=title_size)

    for i in tqdm(range(len(models))):
        param = str(model_params[i]).replace('.', 'p')
        file_name = param + "_residue_info.txt"
        file_path = path.join(results_path, models[i], model_datasets[i], param)
        
        for j in range(len(cluster_sizes)):
            residues, freqs = load_residue_data(file_path, file_name, cluster_sizes[i])

            plt.subplot(num_rows, num_cols, i * num_cols + j + 1)
            plt.loglog(residues, freqs, 'o')

            if i == 0:
                plt.title("Cluster size " + str(cluster_sizes[j]), fontsize=label_size)
            if j == num_cols - 1:
                ax = plt.gca()
                plt.ylabel(model_names[i], fontsize=label_size, rotation=270, labelpad=15)
                ax = plt.gca()
                ax.yaxis.set_label_position("right")

            plt.tight_layout()
    plt.show()