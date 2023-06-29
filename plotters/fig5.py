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
    position = 1

    models = []
    model_names = []
    model_params = []
    model_densities = []
    model_datasets = []

    models.append(path.join("tricritical", "q0"))
    model_names.append("Contact Process")
    model_datasets.append("100x100_residue")

    models.append(path.join("tricritical", "q0p5"))
    model_names.append("TDP (q = 0.5)")
    model_datasets.append("100x100_residue")

    models.append(path.join("scanlon_kalahari"))
    model_names.append("Scanlon")
    model_datasets.append("100x100_residue")

    if position == 1:
        cluster_sizes = [10, 20, 30]

        model_params.append(0.65)
        model_densities.append(0.27)

        model_params.append(0.51)
        model_densities.append(0.25)

        model_params.append(500)
        model_densities.append(0.26)
    elif position == 2:
        cluster_sizes = [10, 50, 100]

        model_params.append(0.7)
        model_densities.append(0.48)

        model_params.append(0.53)
        model_densities.append(0.43)

        model_params.append(700)
        model_densities.append(0.43)
    elif position == 3:
        cluster_sizes = [10, 50, 100]

        model_params.append(0.72)
        model_densities.append(0.54)

        model_params.append(0.55)
        model_densities.append(0.53)

        model_params.append(850)
        model_densities.append(0.56)

    num_cols = len(cluster_sizes)
    num_rows = len(models)

    title_size = 14
    label_size = 12
    tick_size = 10
    legend_size = 10

    num_rows = len(models)
    num_cols = len(cluster_sizes)
    plt.subplots(num_rows, num_cols, figsize=(8.27, 8.27 * num_rows / num_cols))

    meta_title = ""
    if position == 1:
        meta_title = "near critical threshold"
    if position == 2:
        meta_title = "between thresholds"
    if position == 3:
        meta_title = "near percolation threshold"

    plt.suptitle("Distribution of residues " + meta_title, fontsize=title_size)

    for i in tqdm(range(len(models))):
        param = str(model_params[i]).replace('.', 'p')
        null_param = str(model_densities[i]).replace('.', 'p')
        file_name = param + "_residue_info.txt"
        file_path = path.join(results_path, models[i], model_datasets[i], param)
        null_file_name = null_param + "_residue_info.txt"
        null_file_path = path.join(results_path, "null_stochastic", null_param)
        
        for j in range(len(cluster_sizes)):
            residues, freqs = load_residue_data(file_path, file_name, cluster_sizes[i])
            print(null_file_path)
            null_residues, null_freqs = load_residue_data(null_file_path, null_file_name, cluster_sizes[i])

            plt.subplot(num_rows, num_cols, i * num_cols + j + 1)

            if i == 0 and j == 0:
                plt.loglog(residues, freqs, 'bo', label="model")
                plt.loglog(null_residues, null_freqs, 'ko', label="null")
            else:
                plt.loglog(residues, freqs, 'bo')
                plt.loglog(null_residues, null_freqs, 'ko')

            plt.xlim(1, 10 ** 2.5)
            plt.ylim(1, 10 ** 5.5)

            if i != num_rows - 1:
                plt.xticks([])
            if j != 0:
                plt.yticks([])

            if i == 0:
                plt.title("Cluster size " + str(cluster_sizes[j]), fontsize=label_size)
            if j == num_cols - 1:
                ax = plt.gca()
                plt.ylabel(model_names[i], fontsize=label_size, rotation=270, labelpad=15)
                ax = plt.gca()
                ax.yaxis.set_label_position("right")

            plt.tight_layout()

    plt.figlegend(loc="upper right", fontsize=legend_size, bbox_to_anchor=(0.99, 0.99))
    plt.savefig(f"fig5_{position}.png", dpi=300)
    plt.show()