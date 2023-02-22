from matplotlib import pyplot as plt
from numpy import loadtxt, log, transpose
from os import path


if __name__ == '__main__':
    file_name = "input.txt"
    file_path = path.join(path.dirname(__file__), file_name)

    data = transpose(loadtxt(file_path, delimiter=' '))
    cluster_sizes, probabilities = data[0], data[1]
    
    plt.title("Cluster Size Distrubution (log-log)")
    plt.xlabel("Cluster Size")
    plt.ylabel("P(S)")
    plt.loglog(cluster_sizes, probabilities)
    plt.savefig("output.png")
    plt.show()