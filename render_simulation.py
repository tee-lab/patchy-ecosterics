from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from utils import load_automaton_data


def animate(i):
    im.set_array(time_series[i])
    return [im]


if __name__ == '__main__':
    """ Renders the simulation of a given automaton corresponding to the given model """
    model_name = "scanlon_kalahari"
    simulation_index = 0
    time_series = load_automaton_data(model_name, simulation_index)
    num_frames = len(time_series)

    fig = plt.figure()
    im = plt.imshow(time_series[0])

    animate = FuncAnimation(fig, animate, frames=num_frames, interval=100, repeat=False)
    plt.show()