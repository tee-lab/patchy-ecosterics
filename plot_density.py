from matplotlib import pyplot as plt
from numpy import sum, zeros, zeros_like

from utils import load_automaton_data


if __name__ == '__main__':
    """ Plots the time variation of density of a particular state """
    # model_name = "contact_spatial"
    # model_name = "scanlon_kalahari"
    model_name = "tricritical"

    simulation_indices = range(10)
    measure_state = 1

    records = []

    for simulation_index in simulation_indices:
        time_series = load_automaton_data(model_name, simulation_index)
        num_frames = len(time_series)
        lattice_length = len(time_series[0])
        density_time_series = zeros(num_frames, dtype=float)

        for i, lattice in enumerate(time_series):
            num_state = sum(lattice == measure_state)
            density_fraction = num_state / (lattice_length * lattice_length)
            density_time_series[i] = density_fraction
        
        records.append(density_time_series)

    averaged_densities = zeros_like(records[0])
    for record in records:
        averaged_densities += record
    averaged_densities /= len(records)

    print("Average density at final time-step:", averaged_densities[-1])

    plt.plot(averaged_densities)
    plt.show()    