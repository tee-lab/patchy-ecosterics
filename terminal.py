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
    p_values = [0.65, 0.7, 0.72, 0.74]
    q = 0

    for p in p_values:
        print(f"\n---> Simulating p = {p} <---")
        tricritical_final(p, q, num_simulations)