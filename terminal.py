# libraries
from concurrent.futures import ThreadPoolExecutor
from matplotlib import pyplot as plt
from math import floor
from multiprocessing import cpu_count, Pool
from numpy import abs, arange, array, zeros
from skimage.measure import label
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
from cluster_coefficient import cluster_coefficient
from cluster_equivalences import establish_equivalences
from cluster_tracking import track_clusters
from plot_changes import plot_changes
from purge_data import purge_data
from utils import load_automaton_data


if __name__ == '__main__':
    num_simulations = 10
    rainfall_values = arange(300, 1000, 100)
    percolation_probablities = zeros(len(rainfall_values), dtype=float)

    for i, rainfall in enumerate(rainfall_values):
        print(f"\n---> Simulating rainfall = {rainfall} <---")
        d, p = scanlon_kalahari_spanning(rainfall, num_simulations)
        
        print(d, p)
        percolation_probablities[i] = p

    plt.title(f"Percolation probability vs birth probability for Scanlon Kalahari model")
    plt.xlabel("Rainfall")
    plt.ylabel("Percolation probability")
    plt.plot(rainfall_values, percolation_probablities)
    plt.savefig("percolation_probability.png")
    plt.show()