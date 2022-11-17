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
    # num_simulations = cpu_count() - 8
    # p_values = [0.72, 0.73, 0.74]

    # for p in p_values:
    #     purge_data()
    #     print(f"\n---> Simulating p = {p} <---")
    #     file_string = str(p).replace('.', 'p')
    #     tricritical(p, 0.0, num_simulations, save_series=False, save_cluster=True)
    #     compile_changes("tricritical", range(num_simulations), plot_name=file_string)
    #     plot_changes(file_string)

    purge_data()
    num_parallel = floor(cpu_count() / 2)
    res = 0.01
    num = floor(1 / res)

    phase_diagram = zeros((num, num), dtype=float)
    output_string = ""

    for i, q in enumerate(arange(0.0, 1.0, res)):
        for j, p in enumerate(arange(0.0, 1.0, res)):
            phase_diagram[i, j] = tricritical_fast(p, q, num_parallel, save=False)
            update_string = f"p = {p:.2f}, q = {q:.2f}, eq_value = {phase_diagram[i, j]:.4f}"
            print(update_string)
            output_string += update_string + "\n"

    with open("phase_diagram.txt", 'w') as f:
        f.write(output_string)

    plt.title("Phase Diagram of TDP")
    plt.xlabel("p")
    plt.ylabel("q")
    plt.imshow(phase_diagram, extent=[0, 1, 0, 1], origin='lower')
    plt.colorbar()
    plt.savefig("phase_diagram.png")
    plt.show()