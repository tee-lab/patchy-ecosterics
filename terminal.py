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

    tricritical(0.5, 0.5, 1, True)
    automaton_data = load_automaton_data("tricritical", 0)
    time_series_data, info = automaton_data["time_series"], automaton_data["info"]

    analyse_changes(time_series_data[0], time_series_data[1])

    purge_data()