# libraries
from concurrent.futures import ThreadPoolExecutor
from matplotlib import pyplot as plt
from math import floor
from multiprocessing import cpu_count, Pool, set_start_method
from numpy import abs, arange, array, concatenate, zeros
from os import makedirs, path
from skimage.measure import label
from tqdm import tqdm
# models
from models.contact_spatial.in_place_processing import contact_spatial
from models.null_ising.in_place_processing import null_ising
from models.null_static.spanning_cluster import null_static as null_static_spanning
from models.null_stochastic.in_place_processing import null_stochastic
from models.null_stochastic.spanning_cluster import null_stochastic as null_stochastic_spanning
from models.scanlon_kalahari.in_place_processing import scanlon_kalahari
from models.scanlon_kalahari.spanning_cluster import scanlon_kalahari as scanlon_kalahari_spanning
from models.tricritical.dumper import tricritical as tricritical_fast
from models.tricritical.final_lattice import tricritical as tricritical_final
from models.tricritical.in_place_processing import tricritical
from models.tricritical.spanning_cluster import tricritical as tricritical_spanning
# analysis
from compile_changes import compile_changes
from plot_changes import plot_changes
from purge_data import purge_data
from utils import load_automaton_data


if __name__ == '__main__':
    set_start_method("spawn")
    num_simulations = cpu_count() - 1

    immediacy_values = [4, 6, 8, 10]
    r_value = 12

    output_path = path.join(path.dirname(__file__), "outputs")
    makedirs(output_path, exist_ok=True)

    for immediacy in immediacy_values:
        rainfall_values = arange(700, 1200, 10)

        percolation_probablities = zeros(len(rainfall_values), dtype=float)
        avg_densities = zeros(len(rainfall_values), dtype=float)

        for i in range(len(rainfall_values)):
            avg_densities[i], percolation_probablities[i] = scanlon_kalahari_spanning(rainfall_values[i], r_value, immediacy, num_simulations)

        output_string = ""
        for i in range(len(rainfall_values)):
            output_string += f"{rainfall_values[i]} {avg_densities[i]:.6f} {percolation_probablities[i]:.6f}\n"

        with open(path.join(output_path, f"{immediacy}.txt"), "w") as f:
            f.write(output_string)