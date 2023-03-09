from matplotlib import pyplot as plt
from multiprocessing import Pool
from numpy import histogram, zeros
from os import makedirs, path
from tqdm import tqdm

from depth_first_clustering import depth_first_clustering
from utils import load_automaton_data


def analyze_data(model_name, simulation_index):
    grown_clusters = []
    decayed_clusters = []

    changes_list = []
    cluster_ds = [[] for _ in range(10000)]

    data = load_automaton_data(model_name, simulation_index) 
    info = data["info"]
    
    cluster_data = data["cluster_data"]
    final_lattice = data["final_lattice"]
    final_density = data["density_data"][-1]

    if simulation_index == 0:
        print("Analyzing data ...")
        iterator = tqdm(cluster_data)
    else:
        iterator = cluster_data

    for update in iterator:
        if update is None:
            change = 0
            changes_list.append(change)

        elif update["type"] == "growth":
            change = 1
            changes_list.append(change)
            cluster_ds[update["size"]].append(change)
            grown_clusters.append(update["size"])

        elif update["type"] == "decay":
            change = -1
            changes_list.append(change)
            cluster_ds[update["size"]].append(change)
            decayed_clusters.append(update["size"])

        elif update["type"] == "appearance":
            change = 1
            changes_list.append(change)
            cluster_ds[0].append(change)
            grown_clusters.append(0)

        elif update["type"] == "disappearance":
            change = -1
            changes_list.append(change)
            cluster_ds[1].append(change)
            decayed_clusters.append(1)

        elif update["type"] == "merge":
            initial_sizes, final_size = update["initial_sizes"], update["final_size"]
            change = int(final_size - max(initial_sizes))
            changes_list.append(change)
            cluster_ds[int(max(initial_sizes))].append(change)
            grown_clusters.append(int(max(initial_sizes)))

        elif update["type"] == "split":
            initial_size, final_sizes = update["initial_size"], update["final_sizes"]
            change = int(max(final_sizes) - int(initial_size))
            changes_list.append(change)
            cluster_ds[initial_size].append(change)
            decayed_clusters.append(initial_size)

    analysed_data = [grown_clusters, decayed_clusters, changes_list, cluster_ds, final_lattice, final_density]
    return analysed_data


def compile_changes(model_name, simulation_indices, plot_name='data'):
    grown_clusters = []
    decayed_clusters = []

    changes_list = []
    cluster_ds = [[] for _ in range(10000)]

    final_lattices = []
    final_densities = []

    with Pool(len(simulation_indices)) as pool:
        data = list(pool.starmap(analyze_data, [(model_name, simulation_index) for simulation_index in simulation_indices]))

    for analysed_data in data:
        grown_clusters += analysed_data[0]
        decayed_clusters += analysed_data[1]
        changes_list += analysed_data[2]
        cluster_ds = [cluster_ds[i] + analysed_data[3][i] for i in range(len(cluster_ds))]
        final_lattices.append(analysed_data[4].copy())
        final_densities.append(analysed_data[5])

    print("Computing histogram")
    start = 2
    sizes = list(range(start, 200))
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
        cluster_distribution += depth_first_clustering(lattice, False)

    max_index = -1
    for i in range(len(cluster_distribution) - 1, -1, -1):
        if cluster_distribution[i] != 0:
            max_index = i
            break

    cluster_distribution = cluster_distribution[:max_index + 1]

    print("Saving cluster growth probabilities ...")
    fp = open(path.join(folder_path, plot_name + '_cluster_growth_probabilities.txt'), "w")
    output_string = ""
    for size in sizes:
        output_string += f"{size} {growth_probabilities[size - start]}\n"
    fp.write(output_string)
    fp.close()

    # duct-taping the multiple changes issue
    min_positive_value = float("inf")
    for value in changes_histogram:
        if value > 0 and value < min_positive_value:
            min_positive_value = value
    
    if min_positive_value == float("inf"):
        min_positive_value = 1

    multiple_true = True
    for value in changes_histogram:
        if value % min_positive_value != 0:
            multiple_true = False
            break

    if multiple_true:
        changes_histogram = changes_histogram / min_positive_value

    print("Saving dS values undergone by each cluster ...")
    fp = open(path.join(folder_path, plot_name + '_cluster_ds.txt'), "w")
    output_string = ""
    for i in range(len(cluster_ds)):
        if len(cluster_ds[i]) == 0:
            continue
        mean = sum(cluster_ds[i]) / len(cluster_ds[i])
        mean_sq = sum([value ** 2 for value in cluster_ds[i]]) / len(cluster_ds[i])
        output_string += f"{i} {mean} {mean_sq} {len(cluster_ds[i])}\n"
    fp.write(output_string)
    fp.close()

    print("Saving cluster change values ...")
    fp = open(path.join(folder_path, plot_name + '_changes.txt'), 'w')
    output_string = ""
    for change in changes:
        output_string += f"{change + 1} {int(changes_histogram[change - min(changes)])}\n"
    fp.write(output_string)
    fp.close()

    print("Saving cluster distribution ...")
    fp = open(path.join(folder_path, plot_name + '_cluster_distribution.txt'), 'w')
    output_string = ""
    for i, num in enumerate(cluster_distribution):
        output_string += f"{i} {num}\n"
    fp.write(output_string)
    fp.close()

    print("Saving final densities ...")
    fp = open(path.join(folder_path, plot_name + '_densities.txt'), "w")
    output_string = ""
    for i, density in enumerate(final_densities):
        output_string += f"{i} {density}\n"
    fp.write(output_string)
    fp.close()


if __name__ == '__main__':
    compile_changes("tricritical", [0], plot_name="0p73")