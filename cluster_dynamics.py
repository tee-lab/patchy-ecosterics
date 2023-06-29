"""
Given two lattices that differ by only one update,
the get_cluster_dynamics() function returns a status object, which contains:
1) Type of process undergone (growth, decay, appearance, disappearance, merge, split)
2) Size of cluster(s) involved in the process
3) Size of cluster(s) resulting from the process

All other functions are helper functions for get_cluster_dynamics()
"""


from matplotlib import pyplot as plt
from numba import njit
from numpy import uint64, unique, zeros
from skimage.measure import label


def apply_periodic_boundary(labels):
    length = len(labels)

    for i in range(length):
        if labels[i, 0] != 0 and labels[i, -1] != 0 and labels[i, 0] != labels[i, -1]:
            new_label = labels[i, 0]
            old_label = labels[i, -1]
            labels[labels == old_label] = new_label
    
    for j in range(length):
        if labels[0, j] != 0 and labels[-1, j] != 0 and labels[0, j] != labels[-1, j]:
            new_label = labels[0, j]
            old_label = labels[-1, j]
            labels[labels == old_label] = new_label

    return labels


def get_changed_lattice(old_labels, changed_coords):
    """
    In most cases, it is possible to get the labels of the new lattice by looking at the old latice and the change it has undergone
    Only in the case of a merge or a split, it is necessary to re-label the lattice
    This optimization resulted in a 60x speedup
    """    

    length = old_labels.shape[0]
    new_labels = old_labels.copy()

    if changed_coords[0] == 0 or changed_coords[0] == length - 1 or changed_coords[1] == 0 or changed_coords[1] == length - 1:
        boundary = True
    else:
        boundary = False

    if old_labels[changed_coords] == 0:
        # a point changed from 0 to 1
        num_neighbours = get_num_neighbours(old_labels, changed_coords, boundary)
        clusters_around = get_clusters_around(old_labels, changed_coords, boundary)

        if num_neighbours == 0:
            # appearance
            new_labels[changed_coords] = old_labels.max() + 1
        elif len(clusters_around) == 1:
            # growth
            new_labels[changed_coords] = list(clusters_around)[0]
        else:
            # merge
            new_labels[changed_coords] = min(clusters_around)
            for cluster in clusters_around:
                new_labels[old_labels == cluster] = min(clusters_around)
    else:
        # a point changed from 1 to 0
        num_neighbours = get_num_neighbours(old_labels, changed_coords, boundary)
        clusters_around = get_clusters_around(old_labels, changed_coords, boundary)

        if num_neighbours == 0:
            # disappearance
            new_labels[changed_coords] = 0
        elif num_neighbours == 1:
            # decay
            new_labels[changed_coords] = 0
        else:
            # split
            new_labels[new_labels > 0] = 1
            new_labels[changed_coords] = 0
            new_labels = label(new_labels, background=0, connectivity=1)

    return apply_periodic_boundary(new_labels)


def get_cluster_sizes(labelled_lattice, num_clusters):
    cluster_sizes = zeros(num_clusters + 1, dtype=uint64)

    for i in range(labelled_lattice.shape[0]):
        for j in range(labelled_lattice.shape[1]):
            cluster_sizes[labelled_lattice[i, j]] += 1

    return cluster_sizes


def get_clusters_around(labelled_lattice, coords, boundary):
    length = labelled_lattice.shape[0]
    i, j = coords
    clusters = set()

    if not boundary:
        if i > 0 and labelled_lattice[i - 1, j]:
            clusters.add(labelled_lattice[i - 1, j])
        if i < labelled_lattice.shape[0] - 1 and labelled_lattice[i + 1, j]:
            clusters.add(labelled_lattice[i + 1, j])
        if j > 0 and labelled_lattice[i, j - 1]:
            clusters.add(labelled_lattice[i, j - 1])
        if j < labelled_lattice.shape[1] - 1 and labelled_lattice[i, j + 1]:
            clusters.add(labelled_lattice[i, j + 1])
    else:
        if labelled_lattice[(i - 1 + length) % length, j]:
            clusters.add(labelled_lattice[(i - 1 + length) % length, j])
        if labelled_lattice[(i + 1) % length, j]:
            clusters.add(labelled_lattice[(i + 1) % length, j])
        if labelled_lattice[i, (j - 1 + length) % length]:
            clusters.add(labelled_lattice[i, (j - 1 + length) % length])
        if labelled_lattice[i, (j + 1) % length]:
            clusters.add(labelled_lattice[i, (j + 1) % length])

    return clusters


def get_num_neighbours(labelled_lattice, coords, boundary):
    length = labelled_lattice.shape[0]
    i, j = coords
    num_neighbours = 0

    if not boundary:
        if i > 0 and labelled_lattice[i - 1, j]:
            num_neighbours += 1
        if i < labelled_lattice.shape[0] - 1 and labelled_lattice[i + 1, j]:
            num_neighbours += 1
        if j > 0 and labelled_lattice[i, j - 1]:
            num_neighbours += 1
        if j < labelled_lattice.shape[1] - 1 and labelled_lattice[i, j + 1]:
            num_neighbours += 1
    else:
        if labelled_lattice[(i - 1 + length) % length, j]:
            num_neighbours += 1
        if labelled_lattice[(i + 1) % length, j]:
            num_neighbours += 1
        if labelled_lattice[i, (j - 1 + length) % length]:
            num_neighbours += 1
        if labelled_lattice[i, (j + 1) % length]:
            num_neighbours += 1

    return num_neighbours


def get_cluster_dynamics(old_labels, new_labels, changed_coords):
    length = old_labels.shape[0]
    num_old_clusters = unique(old_labels).size - 1
    num_new_clusters = unique(new_labels).size - 1

    if changed_coords[0] == 0 or changed_coords[0] == length - 1 or changed_coords[1] == 0 or changed_coords[1] == length - 1:
        boundary = True
    else:
        boundary = False

    status = {}

    if num_old_clusters == num_new_clusters:
        if old_labels[changed_coords] > 0:
            status['type'] = 'decay'
            status['size'] = len(old_labels[old_labels == old_labels[changed_coords]])
        elif new_labels[changed_coords] > 0:
            status['type'] = 'growth'
            status['size'] = len(new_labels[new_labels == new_labels[changed_coords]]) - 1
    elif num_old_clusters < num_new_clusters:
        split_clusters = get_clusters_around(new_labels, changed_coords, boundary)

        if len(split_clusters) > 1:
            status['type'] = 'split'
            parent_cluster = old_labels[changed_coords]
            status['initial_size'] = len(old_labels[old_labels == parent_cluster])
            status['final_sizes'] = [len(new_labels[new_labels == cluster]) for cluster in split_clusters]
        else:
            status['type'] = 'appearance'
    else:
        merging_clusters = get_clusters_around(old_labels, changed_coords, boundary)

        if len(merging_clusters) > 1:
            status['type'] = 'merge'
            merged_cluster = new_labels[changed_coords]
            status['initial_sizes'] = [len(old_labels[old_labels == cluster]) for cluster in merging_clusters]
            status['final_size'] = len(new_labels[new_labels == merged_cluster])
        else:
            status['type'] = 'disappearance'

    return status


def test_growth():
    old_lattice = zeros((4, 4), dtype=int)
    new_lattice = zeros((4, 4), dtype=int)

    old_lattice[1:3, 1:3] = 1
    new_lattice[1:3, 1:3] = 1
    new_lattice[2, 3] = 1
    changed_coords = (2, 3)

    old_labels = label(old_lattice, background=0, connectivity=1)
    new_labels = get_changed_lattice(old_labels, changed_coords)

    status = get_cluster_dynamics(old_labels, new_labels, changed_coords)
    print(status)

    plt.figure(figsize=(8, 4))
    plt.subplot(121)
    plt.title("Initial lattice")
    plt.imshow(old_labels)
    plt.axis("off")
    plt.subplot(122)
    plt.title("Grown cluster")
    plt.imshow(new_labels)
    plt.axis("off")
    # plt.savefig("growth.png", bbox_inches="tight")
    plt.show()


def test_decay():
    old_lattice = zeros((4, 4), dtype=int)
    new_lattice = zeros((4, 4), dtype=int)

    old_lattice[1:3, 1:3] = 1
    new_lattice[1:3, 1:3] = 1
    new_lattice[2, 2] = 0
    changed_coords = (2, 2)

    old_labels = label(old_lattice, background=0, connectivity=1)
    new_labels = get_changed_lattice(old_labels, changed_coords)

    status = get_cluster_dynamics(old_labels, new_labels, changed_coords)
    print(status)

    plt.figure(figsize=(8, 4))
    plt.subplot(121)
    plt.title("Initial lattice")
    plt.imshow(old_labels)
    plt.axis("off")
    plt.subplot(122)
    plt.title("Decayed cluster")
    plt.imshow(new_labels)
    plt.axis("off")
    # plt.savefig("decay.png", bbox_inches="tight")
    plt.show()


def test_merge():
    old_lattice = zeros((4, 4), dtype=int)
    new_lattice = zeros((4, 4), dtype=int)

    old_lattice[0, 1:3] = 1
    old_lattice[:2, 2] = 1
    old_lattice[2:, 1] = 1
    old_lattice[2:, 3] = 1
    new_lattice = old_lattice.copy()
    new_lattice[2, 2] = 1
    changed_coords = (2, 2)

    old_labels = label(old_lattice, background=0, connectivity=1)
    new_labels = get_changed_lattice(old_labels, changed_coords)

    status = get_cluster_dynamics(old_labels, new_labels, changed_coords)
    print(status)

    plt.figure(figsize=(8, 4))
    plt.subplot(121)
    plt.title("Initial lattice")
    plt.imshow(old_labels)
    plt.axis("off")
    plt.subplot(122)
    plt.title("Merged cluster")
    plt.imshow(new_labels)
    plt.axis("off")
    # plt.savefig("merge.png", bbox_inches="tight")
    plt.show()


def test_split():
    old_lattice = zeros((4, 4), dtype=int)
    new_lattice = zeros((4, 4), dtype=int)

    old_lattice[0, 1:3] = 1
    old_lattice[:3, 2] = 1
    old_lattice[2:, 1] = 1
    old_lattice[2:, 3] = 1
    new_lattice = old_lattice.copy()
    new_lattice[2, 2] = 0
    changed_coords = (2, 2)

    old_labels = label(old_lattice, background=0, connectivity=1)
    new_labels = get_changed_lattice(old_labels, changed_coords)
    
    status = get_cluster_dynamics(old_labels, new_labels, changed_coords)
    print(status)

    plt.figure(figsize=(8, 4))
    plt.subplot(121)
    plt.title("Initial lattice")
    plt.axis("off")
    plt.imshow(old_labels)
    plt.subplot(122)
    plt.title("Split cluster")
    plt.axis("off")
    plt.imshow(new_labels)
    # plt.savefig("split.png", bbox_inches="tight")
    plt.show()

def test_appearance():
    old_lattice = zeros((4, 4), dtype=int)
    new_lattice = zeros((4, 4), dtype=int)

    old_lattice[1:3, 1:3] = 1
    new_lattice[1:3, 1:3] = 1
    new_lattice[0, 0] = 1
    changed_coords = (0, 0)

    old_labels = label(old_lattice, background=0, connectivity=1)
    new_labels = get_changed_lattice(old_labels, changed_coords)

    status = get_cluster_dynamics(old_labels, new_labels, changed_coords)
    print(status)

    plt.figure(figsize=(8, 4))
    plt.subplot(121)
    plt.title("Initial lattice")
    plt.axis("off")
    plt.imshow(old_labels)
    plt.subplot(122)
    plt.title("Appeared cluster")
    plt.axis("off")
    plt.imshow(new_labels)
    # plt.savefig("appearance.png", bbox_inches="tight")
    plt.show()


def test_disappearance():
    old_lattice = zeros((4, 4), dtype=int)
    new_lattice = zeros((4, 4), dtype=int)

    old_lattice[1:3, 1:3] = 1
    old_lattice[0, 0] = 1
    new_lattice[1:3, 1:3] = 1
    changed_coords = (0, 0)

    old_labels = label(old_lattice, background=0, connectivity=1)
    new_labels = get_changed_lattice(old_labels, changed_coords)
    
    status = get_cluster_dynamics(old_labels, new_labels, changed_coords)
    print(status)

    plt.figure(figsize=(8, 4))
    plt.subplot(121)
    plt.title("Initial lattice")
    plt.imshow(old_labels)
    plt.axis('off')
    plt.subplot(122)
    plt.title("Disappeared cluster")
    plt.imshow(new_labels)
    plt.axis('off')
    # plt.savefig("disappearance.png", bbox_inches="tight")
    plt.show()


if __name__ == '__main__':
    test_growth()
    test_decay()
    test_merge()
    test_split()
    test_appearance()
    test_disappearance()