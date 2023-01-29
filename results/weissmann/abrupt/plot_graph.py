from matplotlib import pyplot as plt
from numpy import loadtxt, transpose
import os


if __name__ == '__main__':
    path = os.path.join(os.path.dirname(__file__), "critical_cluster_sizes.txt")
    data = transpose(loadtxt(path, delimiter="\t"))
    drivers, sizes = 1 - data[0], data[1]

    plt.title("Variation of Critical Cluster Size")
    plt.xlabel("1 - p")
    plt.ylabel("Critical Cluster Size")
    plt.plot(drivers, sizes)
    plt.savefig(os.path.join(os.path.dirname(__file__), "critical_cluster_sizes.png"))
    plt.show()