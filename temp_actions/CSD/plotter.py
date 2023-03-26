from matplotlib import pyplot as plt
from numpy import loadtxt, zeros
from skimage.measure import label
from os import path


if __name__ == '__main__':
    current_dir = path.dirname(__file__)
    file_names = ['mat_p0.70.dat', 'mat_p0.72.dat']

    for file_name in file_names:
        file_path = path.join(current_dir, file_name)
        lattice = loadtxt(file_path)

        # change connectivity to 2 if you want to consider Moore neighborhood
        labelled_lattice = label(lattice, background=0, connectivity=1)
        num_clusters = labelled_lattice.max()

        cluster_sizes = []
        for cluster_id in range(1, num_clusters + 1):
            cluster_sizes.append((labelled_lattice == cluster_id).sum())

        cluster_size_distribution = zeros(max(cluster_sizes))
        for cluster_size in cluster_sizes:
            cluster_size_distribution[cluster_size - 1] += 1

        inverse_cdf = zeros(max(cluster_sizes))
        for cluster_size in range(max(cluster_sizes)):
            inverse_cdf[cluster_size] = (cluster_size_distribution[cluster_size:]).sum()
        inverse_cdf /= sum(cluster_size_distribution)

        plt.figure(figsize=(11, 5))
        plt.subplot(1, 2, 1)
        plt.title(f"Lattice from {file_name}")
        plt.imshow(lattice)

        plt.subplot(1, 2, 2)
        plt.title("Cluster Size Distribution")
        plt.xlabel("Cluster Size s")
        plt.ylabel("P(S > s)")
        plt.loglog(range(1, max(cluster_sizes) + 1), inverse_cdf, 'bo')
        plt.show()