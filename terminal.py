# libraries
from concurrent.futures import ThreadPoolExecutor
from matplotlib import pyplot as plt
from math import floor
from multiprocessing import cpu_count, Pool
from numpy import abs, arange, array, zeros
from os import makedirs, path
from skimage.measure import label
from tqdm import tqdm
# models
from models.contact_spatial.in_place_processing import contact_spatial
from models.null_ising.in_place_processing import null_ising
from models.null_stochastic.in_place_processing import null_stochastic
from models.null_stochastic.spanning_cluster import null_stochastic as null_stochastic_spanning
from models.scanlon_kalahari.in_place_processing import scanlon_kalahari
from models.scanlon_kalahari.spanning_cluster import scanlon_kalahari as scanlon_kalahari_spanning
from models.tricritical.in_place_processing import tricritical
from models.tricritical.dumper import tricritical as tricritical_fast
from models.tricritical.spanning_cluster import tricritical as tricritical_spanning
# analysis
from compile_changes import compile_changes
from plot_changes import plot_changes
from purge_data import purge_data
from utils import load_automaton_data


if __name__ == '__main__':
    output_path = path.join(path.dirname(__file__), "outputs")
    makedirs(output_path, exist_ok=True)
    num_simulations = cpu_count() - 1

    q_values = [0, 0.2, 0.4, 0.6, 0.8, 0.92]

    for q in q_values:
        print(f"q = {q:.2f}")

        p_values = arange(0, 1, 0.001)
        avg_densities = zeros(len(p_values), dtype=float)
        percolation_probablities = zeros(len(p_values), dtype=float)

        for i, p in tqdm(enumerate(p_values)):
            avg_densities[i], percolation_probablities[i] = tricritical_spanning(p, q, num_simulations)

        output_string = ""

        for i in range(len(p_values)):
            output_string += f"{p_values[i]:.6f}\t{avg_densities[i]:.6f}\t{percolation_probablities[i]:.6f}\n"

        file_prefix = "q" + str(q).replace('.', 'p') + "_"
        file_name = file_prefix + "percolation.txt"
        file_path = path.join(output_path, file_name)
        with open(file_path, 'w') as f:
            f.write(output_string)

        plt.figure()
        plt.title(f"Percolation probability vs birth probability for q = {q:.2f}")
        plt.xlabel("Birth probability")
        plt.ylabel("Percolation probability")
        plt.plot(p_values, percolation_probablities)
        plt.savefig(path.join(output_path, file_prefix + "percolation_threshold.png"))
        plt.show()

        plt.figure()
        plt.title(f"Percolation probability vs average density for q = {q:.2f}")
        plt.xlabel("Average density")
        plt.ylabel("Percolation probability")
        plt.plot(avg_densities, percolation_probablities)
        plt.savefig(path.join(output_path, file_prefix + "percolation_density.png"))
        plt.show()