from matplotlib import pyplot as plt
from numpy import loadtxt, transpose
from os import path


if __name__ == '__main__':
    current_path = path.dirname(__file__)
    results_file = path.join(current_path, "..", "..", "results", "null_static", "percolation.txt")

    data = transpose(loadtxt(results_file))
    density, percolation = data[0], data[1]

    plt.title("Percolation transition in static null model")
    plt.plot(density, percolation, "o-")
    plt.xlabel("Density")
    plt.ylabel("Percolation probability")
    plt.savefig("percolation_transition.png")
    plt.show()