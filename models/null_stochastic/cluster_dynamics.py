from matplotlib import pyplot as plt
from numpy import uint64, zeros
from skimage.measure import label


def get_cluster_sizes(labelled_lattice):
    num_clusters = labelled_lattice.max()
    cluster_sizes = zeros(num_clusters + 1, dtype=uint64)

    for i in range(labelled_lattice.shape[0]):
        for j in range(labelled_lattice.shape[1]):
            cluster_sizes[labelled_lattice[i, j]] += 1

    return cluster_sizes


def get_clusters_around(labelled_lattice, coords):
    i, j = coords
    clusters = set()

    if i > 0 and labelled_lattice[i - 1, j]:
        clusters.add(labelled_lattice[i - 1, j])
    if i < labelled_lattice.shape[0] - 1 and labelled_lattice[i + 1, j]:
        clusters.add(labelled_lattice[i + 1, j])
    if j > 0 and labelled_lattice[i, j - 1]:
        clusters.add(labelled_lattice[i, j - 1])
    if j < labelled_lattice.shape[1] - 1 and labelled_lattice[i, j + 1]:
        clusters.add(labelled_lattice[i, j + 1])

    return clusters


def get_cluster_dynamics(old_lattice, new_lattice, changed_coords):
    old_labels = label(old_lattice, background=0, connectivity=1)
    new_labels = label(new_lattice, background=0, connectivity=1)

    num_old_clusters = old_labels.max()
    num_new_clusters = new_labels.max()

    old_cluster_sizes = get_cluster_sizes(old_labels)
    new_cluster_sizes = get_cluster_sizes(new_labels)

    status = {}

    if num_old_clusters == num_new_clusters:
        if old_lattice[changed_coords] == 1:
            status['type'] = 'decay'
            status['size'] = old_cluster_sizes[old_labels[changed_coords]]
        elif new_lattice[changed_coords] == 1:
            status['type'] = 'growth'
            status['size'] = old_cluster_sizes[new_labels[changed_coords]]
    elif num_old_clusters < num_new_clusters:
        split_clusters = get_clusters_around(new_labels, changed_coords)

        if len(split_clusters) > 1:
            status['type'] = 'split'
            parent_cluster = old_labels[changed_coords]
            status['initial_size'] = old_cluster_sizes[parent_cluster]
            status['final_sizes'] = [new_cluster_sizes[cluster] for cluster in split_clusters]
        else:
            status['type'] = 'appearance'
    else:
        merging_clusters = get_clusters_around(old_labels, changed_coords)

        if len(merging_clusters) > 1:
            status['type'] = 'merge'
            merged_cluster = new_labels[changed_coords]
            status['initial_sizes'] = [old_cluster_sizes[cluster] for cluster in merging_clusters]
            status['final_size'] = new_cluster_sizes[merged_cluster]
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
    status = get_cluster_dynamics(old_lattice, new_lattice, changed_coords)
    print(status)

    plt.subplot(121)
    plt.title("Initial lattice")
    plt.imshow(old_lattice)
    plt.subplot(122)
    plt.title("Grown cluster")
    plt.imshow(new_lattice)
    plt.show()


def test_decay():
    old_lattice = zeros((4, 4), dtype=int)
    new_lattice = zeros((4, 4), dtype=int)

    old_lattice[1:3, 1:3] = 1
    new_lattice[1:3, 1:3] = 1

    new_lattice[2, 2] = 0
    changed_coords = (2, 2)
    status = get_cluster_dynamics(old_lattice, new_lattice, changed_coords)
    print(status)

    plt.subplot(121)
    plt.title("Initial lattice")
    plt.imshow(old_lattice)
    plt.subplot(122)
    plt.title("Decayed cluster")
    plt.imshow(new_lattice)
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
    status = get_cluster_dynamics(old_lattice, new_lattice, changed_coords)
    print(status)

    plt.subplot(121)
    plt.title("Initial lattice")
    plt.imshow(old_lattice)
    plt.subplot(122)
    plt.title("Merged cluster")
    plt.imshow(new_lattice)
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
    status = get_cluster_dynamics(old_lattice, new_lattice, changed_coords)
    print(status)

    plt.subplot(121)
    plt.title("Initial lattice")
    plt.imshow(old_lattice)
    plt.subplot(122)
    plt.title("Split cluster")
    plt.imshow(new_lattice)
    plt.show()

def test_appearance():
    old_lattice = zeros((4, 4), dtype=int)
    new_lattice = zeros((4, 4), dtype=int)

    old_lattice[1:3, 1:3] = 1
    new_lattice[1:3, 1:3] = 1

    new_lattice[0, 0] = 1
    changed_coords = (0, 0)
    status = get_cluster_dynamics(old_lattice, new_lattice, changed_coords)
    print(status)

    plt.subplot(121)
    plt.title("Initial lattice")
    plt.imshow(old_lattice)
    plt.subplot(122)
    plt.title("Appeared cluster")
    plt.imshow(new_lattice)
    plt.show()


def test_disappearance():
    old_lattice = zeros((4, 4), dtype=int)
    new_lattice = zeros((4, 4), dtype=int)

    old_lattice[1:3, 1:3] = 1
    old_lattice[0, 0] = 1
    new_lattice[1:3, 1:3] = 1

    changed_coords = (0, 0)
    status = get_cluster_dynamics(old_lattice, new_lattice, changed_coords)
    print(status)

    plt.subplot(121)
    plt.title("Initial lattice")
    plt.imshow(old_lattice)
    plt.subplot(122)
    plt.title("Disappeared cluster")
    plt.imshow(new_lattice)
    plt.show()



if __name__ == '__main__':
    test_growth()
    test_decay()
    test_merge()
    test_split()
    test_appearance()
    test_disappearance()