from math import isnan
from numpy import arange, array, delete, loadtxt, log, mean, sum, transpose, zeros
from os import path
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
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
    results_path = path.join(path.dirname(path.dirname(__file__)), 'results')
    model = "tricritical"
    dataset = "100x100"

    q = 0
    p_values = arange(0.72, 0.62, -0.01)

    subfolder = "q" + str(q).replace('.', 'p')
    phase_diagram_path = path.join(results_path, model)
    data_path = path.join(phase_diagram_path, subfolder, dataset)

    goodness = []
    for i in tqdm(range(len(p_values))):
        p = p_values[i]
        folder_name= str(round(p, 2)).replace('.', 'p')
        file_name = f"{folder_name}_changes.txt"
        changes, inverse_cdf = get_cluster_dynamics(folder_name, file_name)
        log_inverse_cdf = log(inverse_cdf, where=(inverse_cdf != 0))

        x = array(changes).reshape((-1, 1))
        y = log_inverse_cdf
        model = LinearRegression().fit(x, y)
        goodness.append(model.score(x, y))

    print(goodness)

    remove_indices = []
    for r in range(len(goodness)):
        if isnan(goodness[r]):
            remove_indices.append(r)

    p_values = delete(p_values, remove_indices)
    goodness = delete(goodness, remove_indices)

    plt.title("Variation of goodness of exp fit")
    plt.xlabel("Increasing closeness to critical point (1 - p)")
    plt.ylabel("Goodness of exp fit")
    plt.plot(1 - p_values, goodness)
    plt.savefig(f"q{str(q).replace('.', 'p')}_ews2_fit.png")
    plt.show()