# libraries
from matplotlib import pyplot as plt
from numpy import arange, zeros
# models
from models.contact_spatial.main import contact_spatial
from models.scanlon_kalahari.main import scanlon_kalahari
from models.tricritical.main import tricritical
# analysis
from plot_density import plot_density
from purge_data import purge_data
from render_simulation import render_simulation


if __name__ == '__main__':
    """ Write automated scripts here """

    p_range = arange(0, 1, 0.025)
    q_range = arange(0, 1, 0.025)
    all_values = [[p, q] for p in p_range for q in q_range]
    n = len(p_range)

    densities = zeros((n, n), dtype=float)

    for j, p in enumerate(p_range):
        for i, q in enumerate(q_range):
            print(f"For ({p}, {q}):")
            mean_density = tricritical(p, q, 5, False)
            densities[i, j] = mean_density
            print(f"Mean density: {mean_density}")
            print("")

            with open("output.txt", "a") as file:
                file.write(f"{round(p, 2)}\t{round(q, 2)}\t{round(mean_density, 4)}\n")

    plt.title("Phase diagram of TDP")
    plt.xlabel("p")
    plt.ylabel("q")
    plt.imshow(densities, origin="lower", extent=[0, 1, 0, 1])
    plt.show()