from matplotlib import pyplot as plt
from numpy import loadtxt, transpose
from os import path


if __name__ == '__main__':
    data = transpose(loadtxt(path.join(path.dirname(__file__), 'critical_cluster_sizes.txt'), delimiter='\t'))
    p, critical_cluster_sizes = data[0], data[1]

    plt.title("Variation of critical cluster size with growth probability")
    plt.plot(p, critical_cluster_sizes)
    plt.xlabel("Growth probability (p)")
    plt.ylabel("Critical cluster size")
    plt.show()