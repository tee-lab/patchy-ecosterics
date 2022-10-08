from itertools import product
from numpy import zeros


def depth_first_clustering(lattice, trim=False):
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
                von_neumann_neighbours = [(i - 1, j), (i + 1, j),
                                            (i, j - 1), (i, j + 1)]

                for i, j in von_neumann_neighbours:
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