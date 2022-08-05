# libraries
from concurrent.futures import ThreadPoolExecutor
from matplotlib import pyplot as plt
from numpy import abs, arange, array, zeros
# models
from models.contact_spatial.main import contact_spatial
from models.scanlon_kalahari.main import scanlon_kalahari
from models.tricritical.main import tricritical
# analysis
from cluster_dynamics import analyse_changes
from cluster_equivalences import establish_equivalences
from cluster_labelling import label_clusters
from cluster_tracking import track_clusters
from plot_density import plot_density
from purge_data import purge_data
from render_simulation import render_simulation
from utils import load_automaton_data



if __name__ == '__main__':
    """ Write automated scripts here """

    p_range = arange(0, 1, 0.01)
    q_range = arange(0, 1, 0.01)
    grid = zeros((len(p_range), len(q_range)))

    for i, q in enumerate(q_range):
        for j, p in enumerate(p_range):
            print(f"p: {p:.2f}, q: {q:.2f}")
            grid[i, j] = tricritical(p, q, 24, False)

    plt.title("Phase diagram of TDP")
    plt.xlabel("p")
    plt.ylabel("q")
    plt.imshow(grid, origin="lower", extent=[0, 1, 0, 1])
    plt.colorbar()
    plt.show()
    plt.savefig("phase_diagram.png")

    # automaton_data = load_automaton_data("tricritical", 0)
    # time_series, info = automaton_data["time_series"], automaton_data["info"]
    # lattice_1, lattice_2 = label_clusters(time_series[0]), label_clusters(time_series[1])

    # track_clusters(lattice_1, lattice_2)
    # establish_equivalences(lattice_1, lattice_2)

    # plt.subplot(1, 2, 1)
    # plt.title("Lattice 1")
    # plt.imshow(lattice_1)
    # plt.subplot(1, 2, 2)
    # plt.title("Lattice 2")
    # plt.imshow(lattice_2)
    # plt.show()