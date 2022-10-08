from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from numpy import sum, zeros
from utils import load_automaton_data


def animate(i):
    plt.title(f"Frame {i}")
    im.set_array(time_series[i])
    return [im]


def render_simulation(model_name, simulation_index):
    """ Renders the simulation of a given automaton corresponding to the given model """
    global time_series, im

    automaton_data = load_automaton_data(model_name, simulation_index, "series")
    time_series, info = automaton_data["series_data"], automaton_data["info"]
    num_frames = len(time_series)

    density_record = zeros(num_frames, dtype=float)

    for i, lattice in enumerate(time_series):
        num_state = sum(lattice == 1)
        density_fraction = num_state / (len(lattice) * len(lattice))
        density_record[i] = density_fraction

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title(info)
    plt.xlabel("time")
    plt.ylabel("density")
    plt.plot(density_record)
    fig = plt.subplot(1, 2, 2).figure
    im = plt.imshow(time_series[0])
    animation = FuncAnimation(fig, animate, frames=num_frames, interval=100, repeat=False)
    plt.show()


if __name__ == '__main__':
    render_simulation("tricritical", 0)