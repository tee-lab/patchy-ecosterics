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
# analysis
from compile_changes import compile_changes
from cluster_coefficient import cluster_coefficient
from cluster_equivalences import establish_equivalences
from cluster_tracking import track_clusters
from plot_changes import plot_changes
from purge_data import purge_data
from utils import load_automaton_data


if __name__ == '__main__':
    num_simulations = cpu_count()
    p_range = arange(0, 1, 0.01)
    densities = zeros(len(p_range), dtype=float)
    q = 0

    for i, p in enumerate(p_range):
        print(f"Simulating p = {p}...")
        density = tricritical_fast(p, q, num_simulations, save = False)
        densities[i] = density

    plt.title(f"Bifurcation diagram of TDP at q = {q}")
    plt.xlabel("p")
    plt.ylabel("mean density")
    plt.plot(p_range, densities)
    plt.show()