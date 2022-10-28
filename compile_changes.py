from matplotlib import pyplot as plt
from numpy import histogram, zeros
from os import makedirs, path
from utils import load_automaton_data

from depth_first_clustering import depth_first_clustering


def compile_changes(model_name, simulation_indices, plot_name='data'):
    grown_clusters = []
    decayed_clusters = []
    changes_list = []
    final_lattices = []

    print("Analyzing data")
    for i, simulation_index in enumerate(simulation_indices):
        print(f"Simulation {i + 1} of {len(simulation_indices)}", end='\r')
        data = load_automaton_data(model_name, simulation_index)
        
        info = data["info"]
        cluster_data = data["cluster_data"]
        final_lattices.append(data["final_lattice"])

        for update in cluster_data:
            if update is None:
                changes_list.append(0)
            elif update["type"] == "growth":
                grown_clusters.append(update["size"])
                changes_list.append(1)
            elif update["type"] == "decay":
                decayed_clusters.append(update["size"])
                changes_list.append(-1)
            elif update["type"] == "merge":
                initial_sizes, final_size = update["initial_sizes"], update["final_size"]
                grown_clusters.append(min(initial_sizes))
            elif update["type"] == "split":
                initial_size, final_sizes = update["initial_size"], update["final_sizes"]
                decayed_clusters.append(initial_size)
                changes_list.append(int(min(final_sizes)) - int(initial_size))

    print("Computing histogram")
    start = 2
    sizes = list(range(start, 100))
    changes = list(range(int(min(changes_list)), int(max(changes_list)) + 1))
    growth_sizes_histogram = histogram(grown_clusters, bins=sizes)[0]
    decay_sizes_histogram = histogram(decayed_clusters, bins=sizes)[0]
    changes_histogram = histogram(changes_list, bins=changes)[0]
    sizes.pop()
    changes.pop()

    print("Computing probabilities")
    growth_probabilities, decay_probabilities = [], []
    for size in sizes:
        total_events = growth_sizes_histogram[size - start] + decay_sizes_histogram[size - start]

        if total_events != 0:
            growth_probabilities.append(growth_sizes_histogram[size - 2] / total_events)
            decay_probabilities.append(decay_sizes_histogram[size - 2] / total_events)
        else:
            growth_probabilities.append(0)
            decay_probabilities.append(0)

    folder_path = path.join(path.dirname(__file__), "outputs")
    makedirs(folder_path, exist_ok=True)

    print("Computing final cluster distribution")
    lattice_length = len(final_lattices[0])
    cluster_distribution = zeros((lattice_length * lattice_length + 1))

    for lattice in final_lattices:
        distribution = depth_first_clustering(lattice, False)
        probabilities = distribution / sum(distribution[1:])
        cluster_distribution += probabilities

    max_index = -1
    for i in range(len(cluster_distribution) - 1, -1, -1):
        if cluster_distribution[i] != 0:
            max_index = i
            break

    cluster_distribution = cluster_distribution[1:max_index + 1]
    cluster_distribution /= len(final_lattices)

    fp = open(path.join(folder_path, plot_name + '_cluster_growth_probabilities.txt'), "w")
    output_string = ""
    for size in sizes:
        output_string += f"{size} {growth_probabilities[size - start]}\n"
    fp.write(output_string)
    fp.close()

    fp = open(path.join(folder_path, plot_name + '_changes.txt'), 'w')
    output_string = ""
    for change in changes:
        output_string += f"{change + 1} {changes_histogram[change - min(changes)]}\n"
    fp.write(output_string)
    fp.close()

    fp = open(path.join(folder_path, plot_name + '_cluster_distribution.txt'), 'w')
    output_string = ""
    for size in range(1, len(cluster_distribution)):
        output_string += f"{size} {cluster_distribution[size]}\n"
    fp.write(output_string)
    fp.close()


if __name__ == '__main__':
    compile_changes("tricritical", range(4))