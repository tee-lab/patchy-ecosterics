from numpy import loadtxt, transpose


def load_distribution(file_path):
    data = transpose(loadtxt(file_path))
    cluster_distribution = data[0][1:]
    return cluster_distribution