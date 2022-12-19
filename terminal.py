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
    num_simulations = 100
    p_range = arange(0, 1, 0.0025)
    q = 0.50
    densities = zeros(len(p_range), dtype=float)

    for i, p in enumerate(p_range):
        print(f"Simulation p = {p:.4f}")
        densities[i] = tricritical_fast(p, q, num_parallel=num_simulations, save=False)

    plt.title(f"Bifurcation diagram of TDP model at q = {q:.2f}")
    plt.xlabel("p")
    plt.ylabel("Steady State Density")
    plt.plot(p_range, densities)
    plt.savefig("bifurcation.png")
    plt.show()