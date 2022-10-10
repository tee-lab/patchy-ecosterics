from matplotlib import pyplot as plt
from utils import load_automaton_data


def analyze_rates(model_name, simulation_indices, plot_name='rates.png'):
    growth_sizes = []
    decay_sizes = []

    for simulation_index in simulation_indices:
        automaton_data = load_automaton_data(model_name, simulation_index, "cluster")
        cluster_data, info = automaton_data["cluster_data"], automaton_data["info"]

        for update in cluster_data:
            if update is None:
                continue
            elif update["type"] == "growth":
                growth_sizes.append(update["size"])
            elif update["type"] == "decay":
                decay_sizes.append(update["size"])

    sizes = list(range(2, 100))
    growth_probabilities = []
    decay_probabilities = []

    for size in sizes:
        num_growths = growth_sizes.count(size)
        num_decays = decay_sizes.count(size)
        total_events = num_growths + num_decays

        if total_events != 0:
            growth_probabilities.append(num_growths / total_events)
            decay_probabilities.append(num_decays / total_events)
        else:
            growth_probabilities.append(0)
            decay_probabilities.append(0)

    print("Growth probabilities:")
    for i, prob in enumerate(growth_probabilities):
        print(f"{i + 1}: {prob}")

    plt.title("Cluster Growth and Decay Probabilities")
    plt.plot(sizes, growth_probabilities, label="Growth")
    plt.plot(sizes, decay_probabilities, label="Decay")
    plt.legend()
    plt.savefig(plot_name)


if __name__ == '__main__':
    analyze_rates("tricritical", range(20))