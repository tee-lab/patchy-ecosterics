from matplotlib import pyplot as plt
from numpy import loadtxt, transpose
from os import path
from tqdm import tqdm


if __name__ == '__main__':
    current_path = path.dirname(__file__)
    project_root_path = path.join(current_path, "..", "..")
    results_root_path = path.join(project_root_path, "results", "tricritical")

    q_values = [0, 0.25, 0.5, 0.75, 0.92]
    dataset = "100x100"
    file_name = "transitions.txt"

    plt.figure()
    plt.title("Change in nature of phase transition with increasing positive feedback")
    plt.xlabel("p")
    plt.ylabel("steady state density")

    for q_value in tqdm(q_values):
        subfolder = "q" + str(q_value).replace('.', 'p')
        data_path = path.join(results_root_path, subfolder, dataset, file_name)
        data = transpose(loadtxt(data_path))

        plt.plot(data[0], data[1], label=f"q = {q_value:.2f}")

    plt.legend()
    plt.savefig("phase_transitions.png")
    plt.show()