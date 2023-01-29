from matplotlib import pyplot as plt
from numpy import loadtxt, transpose
from os import makedirs, path


def get_data(file_path):
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

    return abs_changes[3:], abs_changes_histogram[3:]


def superimpose_graphs(experiment_path, exp_data, null_path, null_data, output_name):
    output_path = path.join(path.dirname(__file__), "outputs")
    makedirs(output_path, exist_ok=True)

    exp_changes, exp_changes_histogram = get_data(path.join(experiment_path, exp_data))
    null_changes, null_changes_histogram = get_data(path.join(null_path, null_data))

    plt.figure()
    plt.title("Cluster Absolute Change Probabilities")
    plt.xlabel("|dS|")
    plt.ylabel("P(|dS|)")
    plt.loglog(exp_changes, exp_changes_histogram, label="Experiment")
    plt.loglog(null_changes, null_changes_histogram, label="Null")
    plt.legend()
    plt.savefig(path.join(output_path, output_name + ".png"))
    plt.show()


if __name__ == '__main__':
    # experiment
    exp_model = "tricritical"
    q = "0"
    regime = "max"
    p = "0.71"

    # null
    null_model = "null_ising"
    x = "0.51"

    # processing
    regime = regime + "_regime"
    q = "q" + str(q).replace('.', 'p')
    p = str(p).replace('.', 'p')
    x = str(x).replace('.', 'p')
    exp_data = f"{p}_changes.txt"
    null_data = f"{x}_changes.txt"

    # combining paths
    experiment_path = path.join(path.dirname(__file__), "results", exp_model, q, regime, p)
    null_path = path.join(path.dirname(__file__), "results", null_model, x)
    output_name = f"{exp_model}_{p}_{q}_{x}"

    superimpose_graphs(experiment_path, exp_data, null_path, null_data, output_name)