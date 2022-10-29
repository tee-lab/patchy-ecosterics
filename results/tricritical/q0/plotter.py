from matplotlib import pyplot as plt
from numpy import loadtxt, transpose
from os import path


if __name__ == '__main__':
    folder_path = path.dirname(__file__)
    data = transpose(loadtxt(path.join(folder_path, 'critical_cluster_sizes.txt'), delimiter='\t'))
    stress, critical_cluster_sizes = 1 - data[0], data[1]

    plt.title("Variation of critical cluster size with stress")
    plt.plot(stress, critical_cluster_sizes)
    plt.xlabel("Stress (1 - p)")
    plt.ylabel("Critical cluster size")
    plt.savefig(path.join(folder_path, 'critical_cluster_sizes.png'))
    plt.show()