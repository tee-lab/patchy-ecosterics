# libraries
from matplotlib import pyplot as plt
from numpy import abs, arange, array, zeros
# models
from models.contact_spatial.main import contact_spatial
from models.scanlon_kalahari.main import scanlon_kalahari
from models.tricritical.main import tricritical
# analysis
from cluster_dynamics import analyse_changes
from cluster_labelling import label_clusters
from cluster_tracking import track_clusters
from plot_density import plot_density
from purge_data import purge_data
from render_simulation import render_simulation
from utils import load_automaton_data


if __name__ == '__main__':
    """ Write automated scripts here """

    # phase transition
    # p_range = arange(0, 1, 0.01)
    # densities = zeros(len(p_range))

    # for i, p in enumerate(p_range):
    #     print(f"p: {p}")
    #     densities[i] = tricritical(p, 0,  save = False)

    # plt.title("Bifurcation diagram of TDP for q = 0")
    # plt.xlabel("p")
    # plt.ylabel("mean density")
    # plt.plot(p_range, densities)
    # plt.show()
    # plt.savefig("bifurcation_diagram.png")

    # phase diagram
    p_range = arange(0, 1, 0.1)
    q_range = arange(0, 1, 0.1)
    densities = zeros((len(p_range), len(q_range)))

    for i, p in enumerate(p_range):
        for j, q in enumerate(q_range):
            print(f"p: {p}, q: {q}")
            densities[j, i] = tricritical(p, q, 24, False)
    
    plt.title("Phase diagram of TDP")
    plt.xlabel("p")
    plt.ylabel("q")
    plt.imshow(densities, origin="lower", extent=[0, 1, 0, 1])
    plt.show()
    plt.savefig("phase_diagram.png")