from matplotlib import pyplot as plt
from numpy import loadtxt, transpose
from os import path


if __name__ == '__main__':
    folder_path = path.dirname(__file__)
    data = transpose(loadtxt(path.join(folder_path, 'critical_cluster_sizes.txt'), delimiter='\t'))
    p, critical_cluster_sizes = data[0], data[1]

    plt.title("Variation of critical cluster size with growth probability")
    plt.plot(p, critical_cluster_sizes)
    plt.xlabel("Growth probability (p)")
    plt.ylabel("Critical cluster size")
    plt.savefig(path.join(folder_path, 'critical_cluster_sizes.png'))
    plt.show()