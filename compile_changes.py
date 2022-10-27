from matplotlib import pyplot as plt
from numpy import histogram
from os import path
from utils import load_automaton_data


def compile_changes(model_name, simulation_indices, plot_name='data'):
    grown_clusters = []
    decayed_clusters = []
    changes = []

    # single processing code
    print("Analyzing data")
    for i, simulation_index in enumerate(simulation_indices):
        print(f"Simulation {i + 1} of {len(simulation_indices)}", end='\r')
        data = load_automaton_data(model_name, simulation_index)
        
        info = data["info"]
        cluster_data = data["cluster_data"]

        for update in cluster_data:
            if update is None:
                changes.append(0)
            elif update["type"] == "growth":
                grown_clusters.append(update["size"])
                changes.append(1)
            elif update["type"] == "decay":
                decayed_clusters.append(update["size"])
                changes.append(-1)
            elif update["type"] == "merge":
                initial_sizes, final_size = update["initial_sizes"], update["final_size"]
                grown_clusters.append(min(initial_sizes))
                changes.append(final_size - min(initial_sizes))
            elif update["type"] == "split":
                initial_size, final_sizes = update["initial_size"], update["final_sizes"]
                decayed_clusters.append(initial_size)
                changes.append(min(final_sizes) - initial_size)

    print("Computing histogram")
    start = 2
    sizes = list(range(start, 100))
    changes = list(range(min(changes), max(changes) + 1))
    growth_sizes_histogram = histogram(grown_clusters, bins=sizes)[0]
    decay_sizes_histogram = histogram(decayed_clusters, bins=sizes)[0]
    changes_histogram = histogram(changes, bins=changes)[0]
    sizes.pop()

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

    fp = open(path.join(folder_path, plot_name + '_cluster.txt'), "w")
    output_string = ""
    for size in sizes:
        output_string += f"{size} {growth_probabilities[size - start]}\n"
    fp.write(output_string)
    fp.close()

    fp = open(path.join(folder_path, plot_name + '_changes.txt'), 'w')
    output_string = ""
    for change in changes:
        output_string += f"{change} {changes_histogram[change - min(changes)]}\n"
    fp.write(output_string)
    fp.close()


if __name__ == '__main__':
    compile_changes("tricritical", range(4))