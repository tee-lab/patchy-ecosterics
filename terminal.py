# libraries
from concurrent.futures import ThreadPoolExecutor
from matplotlib import pyplot as plt
from math import floor
from multiprocessing import cpu_count, Pool, set_start_method
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

    q_values = [0.0, 0.25, 0.5, 0.75, 0.92]

    for q in q_values:
        if q == 0.0:
            p_values = arange(0, 0.7, 0.01) + arange(0.7, 0.75, 0.002) + arange(0.75, 1, 0.01)
        elif q == 0.25:
            p_values = arange(0, 0.62, 0.01) + arange(0.62, 0.67, 0.002) + arange(0.67, 1, 0.01)
        elif q == 0.5:
            p_values = arange(0, 0.53, 0.01) + arange(0.53, 0.58, 0.002) + arange(0.58, 1, 0.01)
        elif q == 0.75:
            p_values = arange(0, 0.4, 0.01) + arange(0.5, 0.44, 0.002) + arange(0.44, 1, 0.01)
        elif q == 0.92:
            p_values = arange(0, 0.27, 0.01) + arange(0.27, 0.3, 0.002) + arange(0.3, 1, 0.01)

        percolation_probablities = zeros(len(p_values), dtype=float)
        avg_densities = zeros(len(p_values), dtype=float)

        for i in range(len(p_values)):
            avg_densities[i], percolation_probablities[i] = tricritical_spanning(p_values[i], q, num_simulations)

    output_string = ""
    for i in range(len(p_values)):
        output_string += f"{p_values[i]:.3f} {avg_densities[i]:.4f} {percolation_probablities[i]:.4f}\n"
    
    with open(f"{q:.2f}.txt", "w") as f:
        f.write(output_string)