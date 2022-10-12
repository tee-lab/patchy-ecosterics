# libraries
from concurrent.futures import ThreadPoolExecutor
from matplotlib import pyplot as plt
from multiprocessing import cpu_count
from numpy import abs, arange, array, zeros
from skimage.measure import label
# models
from models.contact_spatial.in_place_processing import contact_spatial
from models.null.main import null
from models.scanlon_kalahari.in_place_processing import scanlon_kalahari
from models.tricritical.in_place_processing import tricritical
# analysis
from analyze_rates import analyze_rates
from cluster_coefficient import cluster_coefficient
from cluster_equivalences import establish_equivalences
from cluster_tracking import track_clusters
from plot_density import plot_density
from purge_data import purge_data
from render_simulation import render_simulation
from utils import load_automaton_data


if __name__ == '__main__':
    purge_data()
    num_simulations = cpu_count() - 2
    tricritical(0.32, 0.92, num_simulations, save_series=False, save_cluster=True)
    analyze_rates("tricritical", range(num_simulations), plot_name="0p32")