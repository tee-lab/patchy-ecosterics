"""
This program takes a lattice as input and calculates the number of clusters of each size present in it
If one only wants the sizes of clusters (explicit labelling of cluster is not required)
then depth first search is faster
"""


from itertools import product
from matplotlib import pyplot as plt
from numpy import random, zeros
from skimage.measure import label

from cluster_dynamics import apply_periodic_boundary


def depth_first_clustering(lattice, connectivity = 1, periodic=True, trim=True):
    """ Calculates number of clusters of each size, in the given lattce """
    n = len(lattice)
    cluster_sizes = zeros((n * n + 1), dtype=(int))
    visited = zeros((n, n), dtype=(int, int))

    for i, j in product(range(n), repeat=2):
        if not visited[i][j]:
            visited[i][j] = 1

            if lattice[i][j] == 0:
                cluster_sizes[0] += 1
                continue

            current_cluster_size = 1
            stack = [(i, j)]

            while len(stack) > 0:
                i, j = stack.pop()
                neighbours = []

                if periodic:
                    if connectivity == 1:
                        top = (i - 1, j) if i > 0 else (n - 1, j)
                        bottom = (i + 1, j) if i < n - 1 else (0, j)
                        left = (i, j - 1) if j > 0 else (i, n - 1)
                        right = (i, j + 1) if j < n - 1 else (i, 0)
                        neighbours = [top, bottom, left, right]
                    elif connectivity == 2:
                        top_left = ((i - 1 + n) % n, (j - 1 + n) % n)
                        top = ((i - 1 + n) % n, j)
                        top_right = ((i - 1 + n) % n, (j + 1) % n)
                        left = (i, (j - 1 + n) % n)
                        right = (i, (j + 1) % n)
                        bottom_left = ((i + 1) % n, (j - 1 + n) % n)
                        bottom = ((i + 1) % n, j)
                        bottom_right = ((i + 1) % n, (j + 1) % n)
                        neighbours = [top_left, top, top_right, left, right, bottom_left, bottom, bottom_right]
                else:
                    if connectivity == 1:
                        neighbours = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
                    elif connectivity == 2:
                        neighbours = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1), 
                                      (i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), (i + 1, j + 1)]

                for i, j in neighbours:
                    if 0 <= i < n and 0 <= j < n:
                        if lattice[i][j] == 1 and not visited[i][j]:
                            visited[i][j] = True
                            stack.append((i, j))
                            current_cluster_size += 1
            cluster_sizes[current_cluster_size] += 1

    if trim:
        max_cluster_size = -1
        for i in range(n * n, 0, -1):
            if cluster_sizes[i] > 0:
                max_cluster_size = i
                break

        return cluster_sizes[:max_cluster_size + 1]
    else:
        return cluster_sizes
    

def make_random_lattice(n, p):
    lattice = zeros((n, n), dtype=(int))

    for i, j in product(range(n), repeat=2):
        lattice[i][j] = 1 if random.random() < p else 0

    return lattice
    

if __name__ == '__main__':
    periodic = True
    connectivity = 2
    n = 10
    p = 0.3

    random_lattice = make_random_lattice(n, p)
    cluster_distribution = depth_first_clustering(random_lattice, connectivity=connectivity, periodic=periodic, trim=True)

    for i in range(len(cluster_distribution)):
        print(f"Cluster size {i}: {cluster_distribution[i]} clusters")

    if periodic:
        plt.imshow(apply_periodic_boundary(label(random_lattice, background=0, connectivity=connectivity)))
    else:
        plt.imshow(label(random_lattice, background=0, connectivity=connectivity))
    plt.show()