from matplotlib import pyplot as plt
from numpy import delete, transpose, loadtxt, zeros
from os import path
from tqdm import tqdm


def get_sde(folder_path, file_name):
    cluster_ds_data = transpose(loadtxt(open(path.join(folder_path, file_name), 'r')))
    mean_ds_data, mean_ds_sq_data, number_samples = cluster_ds_data[1], cluster_ds_data[2], cluster_ds_data[3]

    limit = 0
    for i in range(len(mean_ds_data)):
        if number_samples[i] < samples_threshold:
            limit = i
            break

    return range(limit), mean_ds_data[:limit], mean_ds_sq_data[:limit]


if __name__ == '__main__':
    results_path = path.join(path.dirname(__file__), "..", "results")
    control_model = "null_stochastic"
    samples_threshold = 25000

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

    title_size = "xx-large"
    label_size = "x-large"
    tick_size = "x-large"
    legend_size = "x-large"

    num_rows = len(models)
    num_cols = len(model_params[0])
    plt.subplots(num_rows, num_cols, figsize=(num_cols * 6 + 1, num_rows * 4 + 4))

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
            file_name = file_prefix + "_cluster_ds.txt"
            folder_path = path.join(dataset_path, file_prefix)
            cluster_sizes, mean_ds, mean_ds_sq = get_sde(folder_path, file_name)

            null_prefix = str(model_density[j]).replace(".", "p")
            null_file_name = null_prefix + "_cluster_ds.txt"
            null_folder_path = path.join(results_path, control_model, null_prefix)
            null_cluster_sizes, null_mean_ds, null_mean_ds_sq = get_sde(null_folder_path, null_file_name)

            plt.subplot(num_rows, num_cols, row * num_cols + j + 1)

            if row == num_rows - 1:
                plt.xlabel("cluster size s", fontsize=label_size)
            if j == 0:
                plt.ylabel("f(s)", fontsize=label_size)

            plt.plot(cluster_sizes, mean_ds, label=f"{model_variable} = {model_param[j]}")
            plt.plot(null_cluster_sizes, null_mean_ds, label=f"null model (f = {model_density[j]})")
            plt.axhline(y=0, linestyle="--")

            ax = plt.gca()
            axins = ax.inset_axes([0.15, 0.1, 0.4, 0.3])
            axins.plot(cluster_sizes, mean_ds_sq)
            axins.plot(null_cluster_sizes, null_mean_ds_sq)

            if row == 0:
                plt.title("Drift and Diffusion", fontsize=title_size)

            plt.legend(fontsize=legend_size, loc="upper right")

    plt.savefig("fig3.png", bbox_inches="tight")
    plt.show()