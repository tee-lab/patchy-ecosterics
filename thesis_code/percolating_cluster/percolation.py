from itertools import product
from matplotlib import pyplot as plt
from numpy import array, zeros
from numpy.random import random
from skimage.measure import label


def row_has_cluster(labelled_lattice, row, cluster):
    length = len(labelled_lattice)
    for j in range(length):
        if labelled_lattice[row, j] == cluster:
            return True
    return False


def col_has_cluster(labelled_lattice, col, cluster):
    length = len(labelled_lattice)
    for i in range(length):
        if labelled_lattice[i, col] == cluster:
            return True
    return False


def get_spanning_cluster(labelled_lattice):
    num_labels = labelled_lattice.max()
    
    sizes = []
    for i in range(1, num_labels + 1):
        size = 0
        for a, b in product(range(length), range(length)):
            if labelled_lattice[a, b] == i:
                size += 1
        sizes.append(size)

    biggest_cluster = sizes.index(max(sizes)) + 1

    return biggest_cluster


if __name__ == '__main__':
    length = 50
    density = 0.6

    lattice = zeros((length, length))
    for i, j in product(range(length), range(length)):
        if random() < density:
            lattice[i, j] = 1

    labelled_lattice = label(lattice, background=0, connectivity=1)

    cluster = get_spanning_cluster(labelled_lattice)

    percolation_lattice = zeros((length, length))

    for i, j in product(range(length), range(length)):
        if labelled_lattice[i, j] == cluster:
            percolation_lattice[i, j] = 2
        elif labelled_lattice[i, j]:
            percolation_lattice[i, j] = 1 

    plt.title("Percolating Cluster (in yellow)")
    plt.axis("off")
    plt.imshow(percolation_lattice)
    plt.savefig("percolating_cluster.png", bbox_inches="tight")
    plt.show()