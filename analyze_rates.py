from matplotlib import pyplot as plt
from numpy import histogram
from utils import load_automaton_data


def analyze_rates(model_name, simulation_indices, plot_name='rates'):
    growth_sizes = []
    decay_sizes = []

    # single processing code
    print("Analyzing data")
    for i, simulation_index in enumerate(simulation_indices):
        print(f"Simulation {i + 1} of {len(simulation_indices)}", end='\r')
        automaton_data = load_automaton_data(model_name, simulation_index, "cluster")
        cluster_data, info = automaton_data["cluster_data"], automaton_data["info"]

        for update in cluster_data:
            if update is None:
                continue
            elif update["type"] == "growth":
                growth_sizes.append(update["size"])
            elif update["type"] == "decay":
                decay_sizes.append(update["size"])

    print("Computing histogram")
    start = 2
    sizes = list(range(start, 100))
    growth_sizes_histogram = histogram(growth_sizes, bins=sizes)[0]
    decay_sizes_histogram = histogram(decay_sizes, bins=sizes)[0]
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

    for size in sizes:
        print(f"{size}: {growth_probabilities[size - start]}")

    plt.title("Cluster Growth and Decay Probabilities")
    plt.xlabel("Cluster size")
    plt.ylabel("Probability")
    plt.plot(sizes, growth_probabilities, label="Growth")
    plt.plot(sizes, decay_probabilities, label="Decay")
    plt.legend()
    plt.savefig(plot_name + '.png')

    fp = open(plot_name + '.txt', "w")
    output_string = ""
    for size in sizes:
        output_string += f"{size}: {growth_probabilities[size - start]}\n"
    fp.write(output_string)
    fp.close()


if __name__ == '__main__':
    analyze_rates("tricritical", range(6))