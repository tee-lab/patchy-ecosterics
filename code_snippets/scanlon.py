

if __name__ == '__main__':
    pass

    # CLUSTER DYNAMICS
    # set_start_method("spawn")
    # num_simulations = 4
    # rainfall_values = [500]

    # for rainfall in rainfall_values:
    #     purge_data()
    #     print(f"\n---> Simulating rainfall = {rainfall} <---")
    #     file_string = str(rainfall).replace('.', 'p')
    #     scanlon_kalahari(rainfall, num_simulations, save_series=False, save_cluster=True)
    #     compile_changes("scanlon_kalahari", range(num_simulations), plot_name=file_string)
    #     plot_changes(file_string)



    # DETAILED PERCOLATION (FUNCTION OF R)
    # set_start_method("spawn")
    # num_simulations = cpu_count() - 1

    # radius_values = [6, 10, 14, 18, 22]
    # immediacy = 24

    # output_path = path.join(path.dirname(__file__), "outputs")
    # makedirs(output_path, exist_ok=True)

    # for radius in radius_values:
    #     rainfall_values = arange(400, 1000, 10)

    #     percolation_probablities = zeros(len(rainfall_values), dtype=float)
    #     avg_densities = zeros(len(rainfall_values), dtype=float)

    #     for i in range(len(rainfall_values)):
    #         avg_densities[i], percolation_probablities[i] = scanlon_kalahari_spanning(rainfall_values[i], radius, immediacy, num_simulations)

    #     output_string = ""
    #     for i in range(len(rainfall_values)):
    #         output_string += f"{rainfall_values[i]} {avg_densities[i]:.6f} {percolation_probablities[i]:.6f}\n"

    #     with open(path.join(output_path, f"{radius}.txt"), "w") as f:
    #         f.write(output_string)



    # DETAILED PERCOLATION (FUNCTION OF IMMEDIACY)
    # set_start_method("spawn")
    # num_simulations = cpu_count() - 1

    # immediacy_values = [6, 12, 18, 24]
    # r_value = 12

    # output_path = path.join(path.dirname(__file__), "outputs")
    # makedirs(output_path, exist_ok=True)

    # for immediacy in immediacy_values:
    #     rainfall_values = arange(700, 1000, 10)

    #     percolation_probablities = zeros(len(rainfall_values), dtype=float)
    #     avg_densities = zeros(len(rainfall_values), dtype=float)

    #     for i in range(len(rainfall_values)):
    #         avg_densities[i], percolation_probablities[i] = scanlon_kalahari_spanning(rainfall_values[i], r_value, immediacy, num_simulations)

    #     output_string = ""
    #     for i in range(len(rainfall_values)):
    #         output_string += f"{rainfall_values[i]} {avg_densities[i]:.6f} {percolation_probablities[i]:.6f}\n"

    #     with open(path.join(output_path, f"{immediacy}.txt"), "w") as f:
    #         f.write(output_string)