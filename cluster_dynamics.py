# libraries
from matplotlib import pyplot as plt
from numpy import array
from skimage.measure import label
# analysis
from cluster_tracking import track_clusters


def analyse_changes(lattice_1, lattice_2):
    """ Looks at all the changes that have taken place, and plots P(dS) vs dS """
    labels_prev = label(lattice_1)
    labels_next = label(lattice_2)
    net_changes = array(track_clusters(labels_prev, labels_next))
    
    max_change, min_change = max(net_changes), min(net_changes)
    probabilities, changes = [], []

    for change in range(min_change, max_change + 1):
        count = 0
        for net_change in net_changes:
            if net_change == change:
                count += 1
        probabilities.append(count / len(net_changes))
        changes.append(change)

    plt.figure(figsize=(10, 3))
    plt.subplot(1, 3, 1)
    plt.title("Lattice 1")
    plt.imshow(labels_prev)
    plt.subplot(1, 3, 2)
    plt.title("Lattice 2")
    plt.imshow(labels_next)
    plt.subplot(1, 3, 3)
    plt.title("P(dS) vs dS")
    plt.xlabel("dS")
    plt.ylabel("P(dS)")
    plt.plot(changes, probabilities)
    plt.show()

    return changes, probabilities