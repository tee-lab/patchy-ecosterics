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
    pass

    ##################################
    # generating bifurcation diagram #
    ##################################
    # num_simulations = 8
    # p_range = arange(0, 1, 0.01)
    # q = 0.0
    # densities = zeros(len(p_range), dtype=float)

    # for i, p in enumerate(p_range):
    #     print(f"Simulation p = {p:.3f}")
    #     densities[i] = tricritical_fast(p, q, num_parallel=num_simulations, save=False)

    # plt.title(f"Bifurction diagram of TDP model at q = {q:.2f}")
    # plt.xlabel("p")
    # plt.ylabel("Steady State Density")
    # plt.plot(p_range, densities)
    # plt.savefig("bifurcation.png")
    # plt.show()

    ########################################
    # generating P(dS) vs dS plots for TDP #
    ########################################
    # num_simulations = cpu_count() - 1
    # p_values = [0.70, 0.71]
    # q = 0.25

    # for p in p_values:
    #     purge_data()
    #     print(f"\n---> Simulating p = {p} <---")
    #     file_string = str(p).replace('.', 'p')
    #     tricritical(p, q, num_simulations, save_series=False, save_cluster=True)
    #     compile_changes("tricritical", range(num_simulations), plot_name=file_string)
    #     plot_changes(file_string)

    ############################################
    # generating P(dS) vs dS plots for Scanlon #
    ############################################
    # num_simulations = 4
    # rainfall_values = [500]
    # q = 0.92

    # for rainfall in rainfall_values:
    #     purge_data()
    #     print(f"\n---> Simulating rainfall = {rainfall} <---")
    #     file_string = str(rainfall).replace('.', 'p')
    #     scanlon_kalahari(rainfall, num_simulations, save_series=False, save_cluster=True)
    #     compile_changes("scanlon_kalahari", range(num_simulations), plot_name=file_string)
    #     plot_changes(file_string)

    ############################
    # generating phase diagram #
    ############################
    # num_simulations = 16
    # h = 0.005
    # p_range = arange(0, 1, h)
    # q_range = arange(0, 1, h)
    # densities = zeros((len(q_range), len(p_range)), dtype=float)
    # output_string = ""

    # for i, q in enumerate(q_range):
    #     print(f"---> Started q = {q:.4f} <---")
    #     for j, p in enumerate(p_range):
    #         print(f"Simulating p = {p:.3f}")
    #         densities[i, j] = tricritical_fast(p, q, num_parallel=num_simulations, save=False)
    #         output_string += f"{p:.4f} {q:.4f} {densities[i, j]:.6f}\n"

    # with open("phase_diagram.txt", "w") as f:
    #     f.write(output_string)

    # plt.title(f"Phase diagram of TDP model")
    # plt.xlabel("p")
    # plt.ylabel("q")
    # plt.imshow(densities, extent=[0, 1, 0, 1], origin="lower")
    # plt.colorbar()
    # plt.savefig("phase_diagram.png")
    # plt.show()