from matplotlib import pyplot as plt
from numpy import arange, loadtxt, transpose
from os import path


if __name__ == '__main__':
    current_path = path.dirname(__file__)
    results_file = path.join(current_path, "..", "..", "results", "null_stochastic", "percolation.txt")

    data = transpose(loadtxt(results_file))
    req_occupancy, density, percolation = data[0], data[1], data[2]
    density_residue = arange(0.65, 0.95, 0.01)
    percolation_residue = [1.0] * len(density_residue)

    plt.title("Percolation transition in dynamic null model")
    plt.plot(density, percolation, "bo-")
    plt.plot(density_residue, percolation_residue, "bo-")
    plt.xlabel("Density")
    plt.ylabel("Percolation probability")
    plt.savefig("percolation_transition.png")
    plt.show()