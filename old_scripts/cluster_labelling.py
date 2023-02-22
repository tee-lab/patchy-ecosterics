from matplotlib import pyplot as plt
from numpy.random import randint
from skimage.measure import label


# class ConnectedComponents:
#     """ Union-find disjoint set data structure """
#     def __init__(self, size):
#         self.root = [i for i in range(size)]

#     def find(self, x):
#         while x != self.root[x]:
#             x = self.root[x]
#         return x
		
#     def join(self, x, y):
#         rootX = self.find(x)
#         rootY = self.find(y)
#         if rootX != rootY:
#             self.root[rootY] = rootX

#     def is_connected(self, x, y):
#         return self.find(x) == self.find(y)


# def minimize_labels(labels):
#     labels_encountered = []

#     for i, j in product(range(len(labels)), repeat=2):
#         if labels[i][j] > 0 and labels[i][j] not in labels_encountered:
#             labels_encountered.append(labels[i][j])

#     for i, j in product(range(len(labels)), repeat=2):
#         if labels[i][j] > 0:
#             labels[i][j] = labels_encountered.index(labels[i][j]) + 1


# @njit
# def replace_labels(lattice, old_label, new_label):
#     for i in range(len(lattice)):
#         for j in range(len(lattice[i])):
#             if lattice[i][j] == old_label:
#                 lattice[i][j] = new_label


# @njit
# def label_clusters_proper(lattice, labels):
#     """ Associates a unique label with each cluster """
#     length = len(lattice)
#     current_equivalence = 1

#     for i in range(length):
#         for j in range(length):
#             if lattice[i][j]:
#                 current_value = lattice[i][j]
#                 if j - 1 > -1:
#                     left_value, left_label = lattice[i][j - 1], labels[i][j - 1]
#                 else:
#                     left_value, left_label = -1, -1
#                 if i - 1 > -1:
#                     top_value, top_label = lattice[i - 1][j], labels[i - 1][j]
#                 else:
#                     top_value, top_label = -1, -1
                
#                 if top_value == current_value and left_value == current_value:
#                     if top_label == left_label:
#                         labels[i][j] = top_label
#                     else:
#                         new_label = min(top_label, left_label)
#                         old_label = max(top_label, left_label)
#                         replace_labels(labels, old_label, new_label)
#                         labels[i][j] = new_label
#                 elif top_value != current_value and left_value == current_value:
#                     labels[i][j] = left_label
#                 elif left_value != current_value and top_value == current_value:
#                     labels[i][j] = top_label
#                 elif left_value != current_value and top_value != current_value:
#                     labels[i][j] = current_equivalence
#                     current_equivalence += 1   


# def label_clusters(lattice):
#     labels = zeros((len(lattice), len(lattice[0])), dtype=int)
#     label_clusters_proper(lattice, labels)
#     return labels


if __name__ == '__main__':
    size = 100
    lattice = randint(0, 2, (size, size), dtype=int)
    labels = label(lattice, connectivity=1)

    plt.subplot(1, 2, 1)
    plt.title("Lattice")
    plt.imshow(lattice)
    plt.subplot(1, 2, 2)
    plt.title("Clustered")
    plt.imshow(labels)
    plt.show()