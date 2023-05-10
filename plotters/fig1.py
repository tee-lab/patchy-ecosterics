from matplotlib import pyplot as plt
from numpy import delete, transpose, loadtxt, zeros
from os import path
from tqdm import tqdm


def get_phase_diagram(folder_path):
    if "scanlon" in folder_path:
        rainfalls = list(range(0, 1000))
        slope = 0.0008588
        intercept = -0.1702
        densities = [max(0, slope * rainfall + intercept) for rainfall in rainfalls]
        return rainfalls, densities
    else:
        file_path = path.join(folder_path, "transitions.txt")
        transitions = transpose(loadtxt(open(file_path, 'r')))
        return transitions[0], transitions[1]


def get_cluster_distribution(folder_path, file_name):
    file_path = path.join(folder_path, file_name)
    cluster_distribution_data = transpose(loadtxt(open(file_path, 'r')))
    cluster_sizes, num = cluster_distribution_data[0][1:], cluster_distribution_data[1][1:]

    inverse_cdf = zeros(len(num))
    for i in range(len(num)):
        inverse_cdf[i] = sum(num[i:])
    inverse_cdf = inverse_cdf / sum(num)

    remove_indices = []
    for i in range(len(cluster_sizes) - 1):
        if inverse_cdf[i] == inverse_cdf[i + 1]:
            remove_indices.append(i)

    cluster_sizes = delete(cluster_sizes, remove_indices)
    inverse_cdf = delete(inverse_cdf, remove_indices)

    return cluster_sizes, inverse_cdf


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
    model_datasets.append("100x100_new")
    model_params.append([0.65, 0.7, 0.72])
    model_densities.append([0.27, 0.48, 0.54])
    model_variables.append("p")
    
    models.append(path.join("tricritical", "q0p5"))
    model_names.append("TDP (q = 0)")
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

    title_size = "xx-large"
    label_size = "x-large"
    tick_size = "x-large"
    legend_size = "x-large"

    num_rows = len(models)
    num_cols = 1 + len(model_params[0])
    # plt.subplot_mosaic([[chr(65 + i) + str(j + 1) for j in range(num_cols)] for i in range(num_rows)])
    plt.subplots(num_rows, num_cols, figsize=(num_cols * 6 + 4, num_rows * 4 + 7))

    for i in tqdm(range(len(models))):
        row = i
        model = models[i]
        model_name = model_names[i]
        model_dataset = model_datasets[i]
        model_param = model_params[i]
        model_density = model_densities[i]
        model_variable = model_variables[i]

        dataset_path = path.join(results_path, model, model_dataset)

        # phase diagram
        col = 1
        phase_diagram = get_phase_diagram(dataset_path)

        plt.subplot(len(models), 1 + len(model_params[0]), row * num_cols + col)
        plt.title("Phase diagram of " + model_name, fontsize=title_size)
        plt.xlabel(model_variable, fontsize=label_size)
        plt.ylabel("density", fontsize=label_size)
        plt.xticks(fontsize=tick_size)
        plt.yticks(fontsize=tick_size)
        plt.plot(phase_diagram[0], phase_diagram[1])

        # distribution plots
        for j in range(len(model_param)):
            file_prefix = str(model_param[j]).replace(".", "p")
            file_name = file_prefix + "_cluster_distribution.txt"
            folder_path = path.join(dataset_path, file_prefix)
            cluster_sizes, inverse_cdf = get_cluster_distribution(folder_path, file_name)

            null_prefix = str(model_density[j]).replace(".", "p")
            null_file_name = null_prefix + "_cluster_distribution.txt"
            null_folder_path = path.join(results_path, control_model, null_prefix)
            null_cluster_sizes, null_inverse_cdf = get_cluster_distribution(null_folder_path, null_file_name)

            plt.subplot(len(models), 1 + len(model_params[0]), row * num_cols + col + j + 1)

            if row == 0:
                plt.title("Cluster Size Distribution", fontsize=title_size)

            if row == num_rows - 1:
                plt.xlabel("cluster size s", fontsize=label_size)
            if j == 0:
                plt.ylabel("P(S > s)", fontsize=label_size)

            plt.loglog(cluster_sizes, inverse_cdf, label=f"{model_variable} = {model_param[j]}")
            plt.loglog(null_cluster_sizes, null_inverse_cdf, label=f"null model (f = {model_density[j]})")

            plt.ylim(10 ** (-5.5), 1)
            if j == 0:
                plt.xlim(1, 10 ** 2.5)
            elif j == 1:
                plt.xlim(1, 10 ** 3.5)
            elif j == 2:
                plt.xlim(1, 10 ** 4.5)

            if j != 0:
                plt.yticks([])
            else:
                plt.yticks(fontsize=tick_size)
            if row != num_rows - 1:
                plt.xticks([])
            else:
                plt.xticks(fontsize=tick_size)

            if j == 0:
                ax = plt.gca()
                axins = ax.inset_axes([0.1, 0.05, 0.4, 0.3])
                axins.semilogy(cluster_sizes, inverse_cdf)
                axins.semilogy(null_cluster_sizes, null_inverse_cdf)
                axins.xaxis.set_visible(False)
                axins.yaxis.set_visible(False)

            plt.legend(fontsize=legend_size)

    plt.savefig("fig1.png", bbox_inches="tight")
    plt.show()