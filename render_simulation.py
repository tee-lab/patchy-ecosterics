from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from utils import load_automaton_data


def animate(i):
    im.set_array(time_series[i])
    return [im]


def render_simulation(model_name, simulation_index):
    """ Renders the simulation of a given automaton corresponding to the given model """
    global time_series, im

    time_series = load_automaton_data(model_name, simulation_index)
    num_frames = len(time_series)

    fig = plt.figure()
    im = plt.imshow(time_series[0])

    animation = FuncAnimation(fig, animate, frames=num_frames, interval=100, repeat=False)
    plt.show()


if __name__ == '__main__':
    render_simulation("contact_spatial", 0)