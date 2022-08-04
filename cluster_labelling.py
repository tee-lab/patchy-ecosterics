from itertools import product
from matplotlib import pyplot as plt
from numpy import zeros
from numpy.random import randint


class ConnectedComponents:
    def __init__(self, size):
        self.root = [i for i in range(size)]

    def find(self, x):
        while x != self.root[x]:
            x = self.root[x]
        return x
		
    def join(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            self.root[rootY] = rootX

    def is_connected(self, x, y):
        return self.find(x) == self.find(y)


def minimize_labels(labels):
    labels_encountered = []

    for i, j in product(range(len(labels)), repeat=2):
        if labels[i][j] > 0 and labels[i][j] not in labels_encountered:
            labels_encountered.append(labels[i][j])

    for i, j in product(range(len(labels)), repeat=2):
        if labels[i][j] > 0:
            labels[i][j] = labels_encountered.index(labels[i][j]) + 1


def label_clusters(lattice):
    length = len(lattice)
    labels = zeros((length, length), dtype=int)
    cc = ConnectedComponents(length * length // 2)
    current_equivalence = 1

    for i, j in product(range(length), repeat=2):
        if lattice[i][j]:
            current_value = lattice[i][j]
            if j - 1 > -1:
                left_value, left_label = lattice[i][j - 1], labels[i][j - 1]
            else:
                left_value, left_label = None, None
            if i - 1 > -1:
                top_value, top_label = lattice[i - 1][j], labels[i - 1][j]
            else:
                top_value, top_label = None, None
            
            if top_value == current_value and left_value == current_value:
                if top_label == left_label:
                    labels[i][j] = top_label
                else:
                    labels[i][j] = min(top_label, left_label)
                    cc.join(top_label, left_label)
            elif top_value != current_value and left_value == current_value:
                labels[i][j] = left_label
            elif left_value != current_value and top_value == current_value:
                labels[i][j] = top_label
            elif left_value != current_value and top_value != current_value:
                labels[i][j] = current_equivalence
                current_equivalence += 1

    for i, j in product(range(length), repeat=2):
        labels[i][j] = cc.find(labels[i][j])

    minimize_labels(labels)
    return labels    


if __name__ == '__main__':
    lattice = randint(0, 2, (10, 10))
    labels = label_clusters(lattice)

    plt.subplot(1, 2, 1)
    plt.title("Lattice")
    plt.imshow(lattice)
    plt.subplot(1, 2, 2)
    plt.title("Clustered")
    plt.imshow(labels)
    plt.show()