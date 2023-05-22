from matplotlib import pyplot as plt
from os import path


if __name__ == '__main__':
    results_folder = path.join(path.dirname(path.dirname(__file__)), "results")

    model = "tricritical"
    subfolder = "q0"
    dataset = "100x100_residue"
    param = "0p7"

    file_name = param + "_residue_info.txt"
    file_path = path.join(results_folder, model, subfolder, dataset, param)

    residue_data = open(path.join(file_path, file_name), "r").readlines()
    for data in residue_data[:-1]:
        size, bins, freq = data.split(':')
        min_bin, max_bin = bins.split(',')
        freqs = list(map(int, freq.split(',')))

        if int(size) in [10, 50, 100, 200, 500, 700]:
            zero_index = -int(min_bin) if int(min_bin) < 0 else int(min_bin)
            freqs = freqs[zero_index:]
            residues = range(0, len(freqs))

            mean = sum([residue * freq for residue, freq in zip(residues, freqs)]) / sum(freqs)
            variance = sum([freq * (residue - mean) ** 2 for residue, freq in zip(residues, freqs)]) / sum(freqs)
            gaussian = [freq * (1 / (variance * 2 * 3.14159) ** 0.5) * 2.71828 ** (-((residue - mean) ** 2) / (2 * variance)) for residue, freq in zip(residues, freqs)]

            plt.subplots(1, 3, figsize=(15, 5))
            plt.subplot(1, 3, 1)
            plt.title("Residue distribution for cluster size " + size)
            plt.xlabel("Residue")
            plt.ylabel("Frequency")
            plt.bar(residues, freqs)
            
            plt.subplot(1, 3, 2)
            plt.title("log-log graph")
            plt.xlabel("Residue")
            plt.ylabel("Frequency")
            plt.loglog(residues, freqs, 'o', label='data')
            plt.loglog(residues, gaussian, 'o', label='gaussian with same mean and variance')
            plt.ylim(1e-2, max(freqs))
            plt.legend()

            plt.subplot(1, 3, 3)
            plt.title("semilog-y graph")
            plt.xlabel("Residue")
            plt.ylabel("Frequency")
            plt.semilogy(residues, freqs, 'o', label='data')
            plt.semilogy(residues, gaussian, 'o', label='gaussian with same mean and variance')
            plt.ylim(1e-2, max(freqs))
            plt.legend()

            plt.savefig(size[:-1] + "_residue_distribution.png", bbox_inches='tight')