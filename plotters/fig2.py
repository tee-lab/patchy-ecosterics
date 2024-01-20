from matplotlib import pyplot as plt
from numpy import delete, transpose, loadtxt, zeros
from os import path
from tqdm import tqdm


def get_cluster_dynamics(folder_path, file_name):
    file_path = path.join(folder_path, file_name)
    changes_data = transpose(loadtxt(open(file_path, 'r')))
    changes, changes_histogram = list(changes_data[0]), changes_data[1]
    changes_probabilities = changes_histogram / sum(changes_histogram)

    abs_changes = list(range(0, int(max(max(changes), -min(changes)))))
    abs_changes_histogram = [0] * len(abs_changes)

    for abs_change in abs_changes:
        value = 0

        if abs_change in changes:
            value += changes_probabilities[changes.index(abs_change)]
        if -abs_change in changes:
            value += changes_probabilities[changes.index(-abs_change)]
        
        abs_changes_histogram[abs_change] = value

    abs_changes_histogram[0] = abs_changes_histogram[0] / 2

    probability_distribution = abs_changes_histogram / sum(abs_changes_histogram)
    inverse_cdf = zeros(len(probability_distribution))
    for i in range(len(probability_distribution)):
        inverse_cdf[i] = sum(probability_distribution[i:])

    cutoff = 0
    for i in range(3, len(inverse_cdf)):
        if inverse_cdf[i] < 1e-12:
            cutoff = i
            break

    if cutoff == 0:
        cutoff = len(inverse_cdf)

    return abs_changes[3:cutoff], inverse_cdf[3:cutoff]


if __name__ == '__main__':
    results_path = path.join(path.dirname(__file__), "..", "results")
    control_model = "null_stochastic"

    models = []
    model_names = []
    model_params = []
    model_densities = []
    model_datasets = []
    model_variables = []

    models.append(path.join("tricritical", "q0"))
    model_names.append("Contact Process")
    model_datasets.append("paper")
    model_params.append([0.65, 0.7, 0.72])
    model_densities.append([0.27, 0.48, 0.54])
    model_variables.append("p")
    
    models.append(path.join("tricritical", "q0p5"))
    model_names.append("TDP (q = 0.5)")
    model_datasets.append("paper")
    model_params.append([0.51, 0.54, 0.55])
    model_densities.append([0.25, 0.49, 0.53])
    model_variables.append("p")

    models.append(path.join("scanlon_kalahari"))
    model_names.append("Scanlon")
    model_datasets.append("paper")
    model_params.append([500, 770, 830])
    model_densities.append([0.26, 0.49, 0.54])
    model_variables.append("rainfall")

    # models.append(path.join("tricritical", "q0p25"))
    # model_names.append("TDP (q = 0.25)")
    # model_datasets.append("100x100_residue")
    # model_params.append([0.59, 0.62, 0.64])
    # model_densities.append([0.27, 0.45, 0.52])
    # model_variables.append("p")

    # models.append(path.join("tricritical", "q0p75"))
    # model_names.append("TDP (q = 0.75)")
    # model_datasets.append("100x100_residue")
    # model_params.append([0.405, 0.41, 0.42])
    # model_densities.append([0.24, 0.38, 0.52])
    # model_variables.append("p")

    title_size = 14
    label_size = 12
    tick_size = 10
    legend_size = 10

    num_rows = len(models)
    num_cols = len(model_params[0])
    plt.subplots(num_rows, num_cols, figsize=(8.27, 8.27 * num_rows / num_cols))
    plt.suptitle("Cluster Dynamics: Distribution of Changes in Cluster Sizes", fontsize=title_size)

    print("This takes a while...")
    for i in tqdm(range(len(models))):
        row = i
        model = models[i]
        model_name = model_names[i]
        model_dataset = model_datasets[i]
        model_param = model_params[i]
        model_density = model_densities[i]
        model_variable = model_variables[i]

        dataset_path = path.join(results_path, model, model_dataset)

        # dynamics plots
        for j in range(len(model_param)):
            file_prefix = str(model_param[j]).replace(".", "p")
            file_name = file_prefix + "_changes.txt"
            folder_path = path.join(dataset_path, file_prefix)
            cluster_sizes, inverse_cdf = get_cluster_dynamics(folder_path, file_name)

            null_prefix = str(model_density[j]).replace(".", "p")
            null_file_name = null_prefix + "_changes.txt"
            null_folder_path = path.join(results_path, control_model, null_prefix)
            null_cluster_sizes, null_inverse_cdf = get_cluster_dynamics(null_folder_path, null_file_name)

            plt.subplot(num_rows, num_cols, row * num_cols + j + 1)

            if row == num_rows - 1:
                plt.xlabel("change in cluster size ($\Delta$s)", fontsize=label_size)
            if j == 0:
                plt.ylabel("P ($\Delta$S > $\Delta$s)", fontsize=label_size)
            if j == num_cols - 1:
                plt.ylabel(model_name, fontsize=label_size, rotation=270, labelpad=15)
                ax = plt.gca()
                ax.yaxis.set_label_position("right")

            if row == 0 and j == 0:
                plt.loglog(cluster_sizes, inverse_cdf, "b-", label=f"model")
                plt.loglog(null_cluster_sizes, null_inverse_cdf, "0.7", label=f"null")
            else:
                plt.loglog(cluster_sizes, inverse_cdf, "b-")
                plt.loglog(null_cluster_sizes, null_inverse_cdf, "0.7")

            plt.ylim(10 ** (-10), 1)
            if j == 0:
                plt.xlim(1, 10 ** 3)
            elif j == 1:
                plt.xlim(1, 10 ** 3.5)
            elif j == 2:
                plt.xlim(1, 10 ** 4.5)

            if row != num_rows - 1:
                plt.xticks([])
            else:
                plt.xticks(fontsize=tick_size)
            if j != 0:
                plt.yticks([])
            else:
                plt.yticks(fontsize=tick_size)

            plt.title(chr(65 + row) + str(j + 1), loc="left", fontsize=title_size)
            plt.tight_layout()

    plt.figlegend(loc="upper right", fontsize=legend_size, bbox_to_anchor=(0.99, 0.99))
    plt.savefig("fig2.png", dpi=300)
    plt.show()