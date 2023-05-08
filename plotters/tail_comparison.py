from matplotlib import pyplot as plt
from numpy import delete, loadtxt, transpose, zeros
from os import path
from tqdm import tqdm


def get_cluster_dynamics(folder, file_name):
    file_path = path.join(data_path, folder, file_name)
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
    CB_friendly_palette = ['#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00']
    
    ####################################
    # Tricritical Directed Percolation #
    ####################################
    results_path = path.join(path.dirname(path.dirname(__file__)), 'results')
    model = "tricritical"
    dataset = "100x100"

    q = 0
    p_values = [0.64, 0.68, 0.72, 0.76, 0.78, 0.8]
    
    # q = 0.25
    # p_values = [0.6, 0.62, 0.65, 0.67]

    # q = 0.5
    # p_values = [0.5, 0.53, 0.55, 0.57]

    # q = 0.75
    # p_values = [0.405, 0.41, 0.42, 0.44]

    # q = 0.92
    # p_values = [0.282, 0.283, 0.285, 0.29]

    subfolder = "q" + str(q).replace('.', 'p')
    phase_diagram_path = path.join(results_path, model)
    data_path = path.join(phase_diagram_path, subfolder, dataset)

    num_cols = len(p_values)

    plt.title(f"Comparison of tails in cluster dynamics")

    for i in tqdm(range(len(p_values))):
        p = p_values[i]
        folder_name = str(p).replace('.', 'p')
        file_name = folder_name + "_changes.txt"
        changes, inverse_cdf = get_cluster_dynamics(folder_name, file_name)                    
        plt.semilogy(changes, inverse_cdf, label=f"p = {p}", color=CB_friendly_palette[i % len(CB_friendly_palette)])
    plt.legend()

    plt.savefig(subfolder + "_tail_comparison.png", bbox_inches='tight')
    plt.show()