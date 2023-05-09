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
    inverse_cdf = inverse_cdf / sum(inverse_cdf)

    return abs_changes[3:], inverse_cdf[3:]


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
    model_names.append("TDP across q = 0")
    model_datasets.append("100x100_new")
    model_params.append([0.65, 0.7, 0.72])
    model_densities.append([0.27, 0.48, 0.54])
    model_variables.append("p")
    
    models.append(path.join("tricritical", "q0p5"))
    model_names.append("TDP across q = 0.5")
    model_datasets.append("100x100")
    model_params.append([0.5, 0.53, 0.55])
    model_densities.append([0.06, 0.43, 0.53])
    model_variables.append("p")

    models.append(path.join("scanlon_kalahari"))
    model_names.append("Scanlon model")
    model_datasets.append("100x100")
    model_params.append([300, 500, 700])
    model_densities.append([0.09, 0.27, 0.43])
    model_variables.append("rainfall")

    num_rows = len(models)
    num_cols = len(model_params[0])
    plt.subplots(num_rows, num_cols, figsize=(num_cols * 6 + 2, num_rows * 4 + 5))

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
            plt.title("Cluster Dynamics")

            if row == num_rows - 1:
                plt.xlabel("change in cluster size ds")
            if j == 0:
                plt.ylabel("P(dS > ds)")
            plt.loglog(cluster_sizes, inverse_cdf, label=f"{model_variable} = {model_param[j]}")
            plt.loglog(null_cluster_sizes, null_inverse_cdf, label="null model")

            # add inset plot with semilogy scale
            ax = plt.gca()
            axins = ax.inset_axes([0.2, 0.1, 0.4, 0.3])
            axins.semilogy(cluster_sizes, inverse_cdf)

            plt.legend()

    plt.savefig("fig2.png", bbox_inches="tight")
    plt.show()