from copy import copy
from matplotlib import pyplot as plt
from multiprocessing import Pool, cpu_count, set_start_method, get_context
from utils import load_automaton_data


def get_sizes(model_name, simulation_index):
    growth_sizes, decay_sizes = [], []
    automaton_data = load_automaton_data(model_name, simulation_index, "cluster")
    cluster_data, info = automaton_data["cluster_data"], automaton_data["info"]

    for update in cluster_data:
        if update is None:
            continue
        elif update["type"] == "growth":
            growth_sizes.append(update["size"])
        elif update["type"] == "decay":
            decay_sizes.append(update["size"])

    data = {"growth": growth_sizes, "decay": decay_sizes}
    return data


def get_cluster_dynamics(growth_sizes, decay_sizes, size):
    growth_probability, decay_probability = 0, 0

    num_growths = growth_sizes.count(size)
    num_decays = decay_sizes.count(size)
    total_events = num_growths + num_decays

    if total_events != 0:
        growth_probability = num_growths / total_events
        decay_probability = num_decays / total_events
    
    data = {"growth": growth_probability, "decay": decay_probability}
    return data


def analyze_rates(model_name, simulation_indices, plot_name='rates'):
    num_cpus = cpu_count()
    set_start_method("spawn")

    growth_sizes = []
    decay_sizes = []

    # multiprocessing code
    # print("Obtaining size data...")    
    # with Pool(num_cpus) as p:
    #     size_data = p.starmap(get_sizes, [(model_name, i) for i in simulation_indices])

    # single processing code
    print("Obtaining size data...")
    for i, simulation_index in enumerate(simulation_indices):
        print(f"Analyzing simulation {i + 1} of {len(simulation_indices)}")
        automaton_data = load_automaton_data(model_name, simulation_index, "cluster")
        cluster_data, info = automaton_data["cluster_data"], automaton_data["info"]

        for update in cluster_data:
            if update is None:
                continue
            elif update["type"] == "growth":
                growth_sizes.append(update["size"])
            elif update["type"] == "decay":
                decay_sizes.append(update["size"])

    # print("Collating size data...")
    # for d in size_data:
    #     growth_sizes.extend(d["growth"])
    #     decay_sizes.extend(d["decay"])

    print("Obtaining cluster dynamics...")
    sizes = list(range(2, 100))
    with get_context("spawn").Pool(num_cpus) as p:
        cluster_data = p.starmap(get_cluster_dynamics, [(copy(growth_sizes), copy(decay_sizes), size) for size in sizes])

    print("Stringing together probabilities")
    growth_probabilities = [d["growth"] for d in cluster_data]
    decay_probabilities = [d["decay"] for d in cluster_data]

    # single threaded code
    # for i, simulation_index in enumerate(simulation_indices):
    #     print(f"Analyzing simulation {i + 1} of {len(simulation_indices)}")
    #     automaton_data = load_automaton_data(model_name, simulation_index, "cluster")
    #     cluster_data, info = automaton_data["cluster_data"], automaton_data["info"]

    #     for update in cluster_data:
    #         if update is None:
    #             continue
    #         elif update["type"] == "growth":
    #             growth_sizes.append(update["size"])
    #         elif update["type"] == "decay":
    #             decay_sizes.append(update["size"])

    # sizes = list(range(2, 100))
    # growth_probabilities = []
    # decay_probabilities = []

    # for i, size in enumerate(sizes):
    #     print(f"Calculating cluster dynamics for size {i + 1} of {len(sizes)}")
    #     num_growths = growth_sizes.count(size)
    #     num_decays = decay_sizes.count(size)
    #     total_events = num_growths + num_decays

    #     if total_events != 0:
    #         growth_probabilities.append(num_growths / total_events)
    #         decay_probabilities.append(num_decays / total_events)
    #     else:
    #         growth_probabilities.append(0)
    #         decay_probabilities.append(0)

    print("Growth probabilities:")
    for i, prob in enumerate(growth_probabilities):
        print(f"{i + 1}: {prob}")

    plt.title("Cluster Growth and Decay Probabilities")
    plt.xlabel("Cluster size")
    plt.ylabel("Probability")
    plt.plot(sizes, growth_probabilities, label="Growth")
    plt.plot(sizes, decay_probabilities, label="Decay")
    plt.legend()
    plt.savefig(plot_name + '.png')

    fp = open(plot_name + '.txt', "w")
    output_string = ""
    for i, size in enumerate(sizes):
        output_string += f"{size}: {growth_probabilities[i]}\n"
    fp.write(output_string)
    fp.close()


if __name__ == '__main__':
    analyze_rates("tricritical", range(48))