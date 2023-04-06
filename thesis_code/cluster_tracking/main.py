from matplotlib import pyplot as plt
from numpy.random import randint


if __name__ == '__main__':
    length = 30
    initial_lattice = randint(0, 2, (length, length))
    initial_lattice[length // 2:length // 2 + 4, length // 2:length // 2 + 5] = 0
    initial_lattice[length // 2 + 1: length // 2 + 3, length // 2 + 1: length // 2 + 3] = 2

    final_lattice = initial_lattice.copy()
    final_lattice[length // 2 + 2, length // 2 + 3] = 2

    plt.subplot(1, 2, 1)
    plt.title("Initial lattice")
    plt.imshow(initial_lattice)
    plt.subplot(1, 2, 2)
    plt.title("Updated lattice")
    plt.imshow(final_lattice)
    plt.savefig('cluster_tracking.png', bbox_inches='tight')
    plt.show()