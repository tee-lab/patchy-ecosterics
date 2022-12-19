# libraries
from concurrent.futures import ThreadPoolExecutor
from matplotlib import pyplot as plt
from math import floor
from multiprocessing import cpu_count, Pool
from numpy import abs, arange, array, zeros
from skimage.measure import label
# models
from models.contact_spatial.in_place_processing import contact_spatial
from models.null.main import null
from models.scanlon_kalahari.in_place_processing import scanlon_kalahari
from models.tricritical.in_place_processing import tricritical
from models.tricritical.dumper import tricritical as tricritical_fast
from models.tricritical.spanning_cluster import tricritical as tricritical_spanning
# analysis
from compile_changes import compile_changes
from cluster_coefficient import cluster_coefficient
from cluster_equivalences import establish_equivalences
from cluster_tracking import track_clusters
from plot_changes import plot_changes
from purge_data import purge_data
from utils import load_automaton_data


if __name__ == '__main__':
    num_simulations = 16
    p_range = arange(0, 1, 0.01)
    q = 0.92
    densities = zeros(len(p_range))
    probabilities = zeros(len(p_range))

    for i, p in enumerate(p_range):
        print(f'p = {p:.2f}')
        density, probability = tricritical_spanning(p, q, num_parallel=num_simulations)
        densities[i] = density
        probabilities[i] = probability

    plt.title(f"Bifurcation diagram of TDP at q = {q:.2f}")
    plt.xlabel("p")
    plt.ylabel("mean density")
    plt.plot(p_range, densities)
    plt.show()

    plt.title(f"Percolation probability vs birth probability for q = {q:.2f}")
    plt.xlabel("Birth probability")
    plt.ylabel("Percolation probability")
    plt.plot(p_range, probabilities)
    plt.show()

    plt.title(f"Percolation probability vs density for q = {q:.2f}")
    plt.xlabel("Density")
    plt.ylabel("Percolation probability")
    plt.plot(densities, probabilities, 'o')
    plt.show()