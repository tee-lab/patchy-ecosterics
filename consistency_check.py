from numpy import randint
from skimage.measure import label


def get_random_cluster_sizes(lattice_size = 100):
    lattice = randint(0, 2, (lattice_size, lattice_size))
    labelled_lattice = label(lattice, background=0, connectivity=1)

    cluster_sizes = []
    for i in range(1, labelled_lattice.max() + 1):
        cluster_sizes.append(len(labelled_lattice[labelled_lattice == i]))

    return cluster_sizes


if __name__ == '__main__':
    lattice_size = 100
    cluster_sizes = get_random_cluster_sizes(lattice_size)

    # x dot = a x^2 - b x + c
    a = 10
    b = 1
    c = 0
    