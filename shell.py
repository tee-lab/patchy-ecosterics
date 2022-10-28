# libraries
from matplotlib import pyplot as plt
# models
from models.contact_spatial.in_place_processing import contact_spatial
from models.scanlon_kalahari.in_place_processing import scanlon_kalahari
from models.tricritical.in_place_processing import tricritical
# analysis
from cluster_dynamics import analyse_changes
from cluster_equivalences import establish_equivalences
from cluster_labelling import label_clusters
from cluster_tracking import track_clusters
from purge_data import purge_data
# utils
from utils import load_automaton_data


def show_help():
    print("---> Models <---")
    print("contact_spatial(p, num_parallel, save)")
    print("scanlon_kalahari(rainfall, num_parallel, save)")
    print("tricritical(p, q, num_parallel, save)")
    print("!!! All the above functions return the final (averaged) density !!!")
    print("")

    print("---> Analysis <---")
    print("analyse_changes(labelled_lattice_1, labelled_lattice_2) -> P(dS) vs dS graph")
    print("establish_equivalences(labelled_lattice_1, labelled_lattice_2) -> equivalences")
    print("label_clusters(lattice) -> labelled lattice")
    print("track_clusters(labelled_lattice_1, labelled_lattice_2) -> net changes in cluster sizes")
    print("plot_density(model_name, range) -> density vs time graph")
    print("purge_data(model_name)")
    print("render_simulation(model_name, simulation_index) -> animation")
    print("!!! The above functions require some saved data to operate on !!!")
    print("")

    print("---> Utils <---")
    print("load_automaton_data(model_name, simulation_index) -> {time_series, info}")


if __name__ == '__main__':
    print("---> Cluster dynamics in Semi-Arid Vegetation <---")
    print("Project by: Chandan Relekar | Fork me at GitHub (chanrt)")
    print("GitHub organization: TEE-Lab")
    print("GitHub repository name: vegetation-dynamics")
    print("\nType 'help' to see the list of available commands.\n")

    while True:
        input_string = input(">> ")

        if input_string in ["quit", "exit"]:
            break
        elif input_string == "help":
            show_help()

        try:
            exec(input_string)
        except:
            print("Some error encountered")