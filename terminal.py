# libraries
from concurrent.futures import ThreadPoolExecutor
from matplotlib import pyplot as plt
from numpy import abs, arange, array, zeros
from skimage.measure import label
# models
from models.contact_spatial.main import contact_spatial
from models.null.main import null
from models.scanlon_kalahari.main import scanlon_kalahari
from models.tricritical.main import tricritical
# analysis
from cluster_coefficient import cluster_coefficient
from cluster_dynamics import analyse_changes
from cluster_equivalences import establish_equivalences
from cluster_tracking import track_clusters
from plot_density import plot_density
from purge_data import purge_data
from render_simulation import render_simulation
from utils import load_automaton_data



if __name__ == '__main__':
    """ Write automated scripts here """

    automaton_data = load_automaton_data("contact_spatial", 0)
    time_series, info = automaton_data["time_series"], automaton_data["info"]
    lattice_1, lattice_2 = time_series[0], time_series[10]
    analyse_changes(lattice_1, lattice_2)

    track_clusters(lattice_1, lattice_2)
    establish_equivalences(lattice_1, lattice_2)

    plt.subplot(1, 2, 1)
    plt.title("Lattice 1")
    plt.imshow(lattice_1)
    plt.subplot(1, 2, 2)
    plt.title("Lattice 2")
    plt.imshow(lattice_2)
    plt.show()