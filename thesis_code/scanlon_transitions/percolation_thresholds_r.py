from matplotlib import pyplot as plt
from numpy import loadtxt, transpose
from os import path
from tqdm import tqdm


if __name__ == '__main__':
    current_path = path.dirname(__file__)
    project_root_path = path.join(current_path, "..", "..")
    results_root_path = path.join(project_root_path, "results", "scanlon_kalahari")

    r_values = [6, 10, 14, 18]

    plt.figure()
    plt.title("Change in percolation threshold with increasing radius of influence")
    plt.xlabel("rainfall")
    plt.ylabel("percolation probability")

    for r_value in tqdm(r_values):
        data_path = path.join(results_root_path, "transitions", "radius", f"{r_value}.txt")
        data = transpose(loadtxt(data_path))

        plt.plot(data[0], data[2], label=f"r = {r_value}", marker='o')

    plt.legend()
    plt.savefig("percolation_thresholds_r.png")
    plt.show()