from matplotlib import pyplot as plt
from numpy import loadtxt, transpose
from os import path


def get_num_samples(folder_path, file_name):
    cluster_ds_data = transpose(loadtxt(open(path.join(folder_path, file_name), 'r')))
    cluster_size, number_samples = cluster_ds_data[0], cluster_ds_data[3]

    return cluster_size[100:], number_samples[100:]


if __name__ == '__main__':
    results_path = path.join(path.dirname(__file__), "..", "results")
    samples_threshold = 25000

    models = []
    model_names = []
    model_params = []
    model_densities = []
    model_datasets = []
    model_variables = []

    # models.append(path.join("scanlon_kalahari"))
    # model_names.append("Scanlon")
    # model_datasets.append("100x100_residue")
    # model_params.append([700, 850])
    # model_variables.append("rainfall")

    models.append(path.join("tricritical", "q0"))
    model_names.append("TDP (q = 0)")
    model_datasets.append("100x100_residue")
    model_params.append([0.7, 0.72])
    model_variables.append("p")

    for i in range(len(models)):
        row = i
        model = models[i]
        model_name = model_names[i]
        model_dataset = model_datasets[i]
        model_param = model_params[i]
        model_variable = model_variables[i]

        dataset_path = path.join(results_path, model, model_dataset)

        plt.title("Number of Samples vs Cluster Size")
        plt.xlabel("Cluster Size s")
        plt.ylabel("Number of Samples")
        

        for j in range(len(model_param)):
            file_prefix = str(model_param[j]).replace(".", "p")
            file_name = file_prefix + "_cluster_ds.txt"
            folder_path = path.join(dataset_path, file_prefix)
            cluster_sizes, num_samples = get_num_samples(folder_path, file_name)

            plt.plot(cluster_sizes, num_samples, label=f"{model_name} ({model_variable} = {model_param[j]})")
    
    plt.axhline(y=samples_threshold, linestyle='--')
    plt.legend()
    plt.show()