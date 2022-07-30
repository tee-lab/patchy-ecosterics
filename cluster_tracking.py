from itertools import product


def get_num_active(labels):
    num_active = 0
    for i, j in product(range(len(labels)), repeat=2):
        if labels[i][j] > 0:
            num_active += 1
    return num_active


def get_num_clusters(labels):
    return labels.max()


def get_cluster_size(labels, cluster_id):
    length = len(labels)
    cluster_size = 0
    for i, j in product(range(length), repeat=2):
        if labels[i][j] == cluster_id:
            cluster_size += 1
    return cluster_size


def track_clusters(labels_prev, labels_next):
    length = len(labels_prev)

    prev_num_clusters = get_num_clusters(labels_prev)
    next_num_clusters = get_num_clusters(labels_next)

    prev_considered = []
    next_considered = []
    net_change = []

    for i, j in product(range(length), repeat=2):
        if labels_prev[i][j] > 0 and labels_prev[i][j] not in prev_considered:
            if labels_next[i][j] > 0 and labels_next[i][j] not in next_considered:
                prev_considered.append(labels_prev[i][j])
                next_considered.append(labels_next[i][j])

                ancestor_cluster_size = get_cluster_size(labels_prev, labels_prev[i][j])
                descendant_cluster_size = get_cluster_size(labels_next, labels_next[i][j])
                net_change.append(descendant_cluster_size - ancestor_cluster_size)

    print(f"In lattice 1, there are {get_num_active(labels_prev)} active cells and {prev_num_clusters} clusters.")
    print(f"In lattice 2, there are {get_num_active(labels_next)} active cells and {next_num_clusters} clusters.")

    records_length = len(prev_considered)
    for i in range(records_length):
        print(f"Cluster {prev_considered[i]} = Cluster {next_considered[i]}. Net change: {net_change[i]}")