from matplotlib import pyplot as plt
from os import path
from utils import load_automaton_data


def plot_density(density_data):
    plt.title("Variation of density with time")
    plt.xlabel("Time (N^2)")
    plt.ylabel("Density")
    plt.plot(density_data)
    plt.show()


def peer_data(model_name, simulation_index):
    data = load_automaton_data(model_name, simulation_index)

    info_string = data["info"]
    density_data = data["density_data"]
    cluster_data = data["cluster_data"]
    series_data = data["series_data"]

    print(f"Info string: {info_string}")
    print(f"Density data length: {len(density_data)}")

    if cluster_data is not None:
        print(f"Cluster data length: {len(cluster_data)}")
    else:
        print("Cluster data does not exist")

    if series_data is not None:
        print(f"Series data shape: {series_data.shape}")
    else:
        print("Series data does not exist")

    plot_density(density_data)


if __name__ == "__main__":
    peer_data("tricritical", 0)
    