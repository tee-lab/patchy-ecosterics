from matplotlib import pyplot as plt
from numpy import sum, zeros, zeros_like

from utils import load_automaton_data


if __name__ == '__main__':
    model_name = "scanlon_kalahari"
    simulation_indices = range(5)
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

    plt.plot(averaged_densities)
    plt.show()