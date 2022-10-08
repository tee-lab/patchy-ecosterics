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

    p_values = arange(0.2, 0.4, 0.01)
    f_values = zeros(len(p_values), dtype=float)
    
    q = 0.92
    for i, p in enumerate(p_values):
        print(p)
        f_values[i] = tricritical(p, q, 5, False)

    plt.plot(p_values, f_values)
    plt.show()