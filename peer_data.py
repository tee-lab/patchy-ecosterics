from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from numpy import array, zeros
from utils import load_automaton_data


def data_summary(model_name, simulation_index):
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


def plot_density(model_name, simulation_index):
    data = load_automaton_data(model_name, simulation_index)
    info = data["info"]
    density_data = data["density_data"]

    plt.title(f"Variation of density with time for {info}")
    plt.xlabel("Time (N^2)")
    plt.ylabel("Density")
    plt.plot(density_data)
    plt.show()


def plot_average_density(model_name, simulation_indices):
    data = load_automaton_data(model_name, simulation_indices[0])
    density_data = data["density_data"]
    data_length = len(density_data)

    average_density = zeros(data_length)
    for simulation_index in simulation_indices:
        data = load_automaton_data(model_name, simulation_index)
        density_data = data["density_data"]
        average_density += array(density_data)

    average_density /= len(simulation_indices)

    plt.title(f"Average density for {model_name}")
    plt.xlabel("Time (N^2)")
    plt.ylabel("Density")
    plt.plot(average_density)
    plt.show()


def plot_final_lattice(model_name, simulation_index):
    data = load_automaton_data(model_name, simulation_index)
    series_data = data["series_data"]
    final_lattice = series_data[-1]

    plt.title(f"Final lattice for {model_name}")
    plt.imshow(final_lattice)
    plt.show()

    for i in range(len(final_lattice)):
        for j in range(len(final_lattice[0])):
            print(int(final_lattice[i][j]), end=" ")
        print()


def print_cluster_data(model_name, simulation_index):
    data = load_automaton_data(model_name, simulation_index)
    cluster_data = data["cluster_data"]

    if cluster_data is not None:
        for iteration, update in enumerate(cluster_data):
            print(f"iteration {iteration}: {update}")
    else:
        print("Cluster data does not exist")


def visualize_series_data(model_name, simulation_index):
    global series_data, im, info
    
    data = load_automaton_data(model_name, simulation_index)
    info = data["info"]
    series_data = data["series_data"]

    if series_data is not None:
        num_frames = len(series_data)
        fig = plt.figure()
        im = plt.imshow(series_data[0])
        animation = FuncAnimation(fig, animate, frames=num_frames, interval=100, repeat=False)
        plt.show()
    else:
        print("Series data does not exist")


def animate(i):
    plt.title(f"Frame {i} of {info}")
    im.set_array(series_data[i])
    return [im]


if __name__ == "__main__":
    model = "tricritical"
    simulation_index = 0
    simulation_indices = range(0, 4)

    data_summary(model, simulation_index)
    plot_density(model, simulation_index)
    plot_average_density(model, simulation_indices)
    plot_final_lattice(model, simulation_index)
    print_cluster_data(model, simulation_index)
    visualize_series_data(model, simulation_index)