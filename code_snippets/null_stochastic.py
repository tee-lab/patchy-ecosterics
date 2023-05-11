

if __name__ == '__main__':
    pass

    # set_start_method("spawn")
    # num_simulations = cpu_count() - 1

    # f_values = [0.01 * i for i in range(1, 100)]

    # for f in f_values:
    #     purge_data()
    #     print(f"\n---> Simulating f = {f} <---")
    #     file_string = str(f).replace('.', 'p')
    #     null_stochastic(f, num_simulations, save_series=False, save_cluster=True)
    #     compile_changes("null_stochastic", range(num_simulations), plot_name=file_string)
    #     plot_changes(file_string)