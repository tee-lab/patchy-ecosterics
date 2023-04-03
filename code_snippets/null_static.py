

if __name__ == '__main__':
    pass

    # PERCOLATION
    # set_start_method("spawn")
    # num_simulations = cpu_count() - 1
    # output_path = path.join(path.dirname(__file__), "outputs")
    # makedirs(output_path, exist_ok=True)

    # occupancies = arange(0.1, 1.00, 0.1)
    # avg_densities = zeros(len(occupancies))
    # percolation_probabilities = zeros(len(occupancies))

    # for i in tqdm(range(len(occupancies))):
    #     avg_densities[i], percolation_probabilities[i] = null_static_spanning(occupancies[i], num_simulations)

    #     output_string = ""
    #     for i in range(len(occupancies)):
    #         output_string += f"{avg_densities[i]:.6f} {percolation_probabilities[i]:.6f}\n"

    #     with open(path.join(output_path, "null_static.txt"), "w") as f:
    #         f.write(output_string)