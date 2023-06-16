from matplotlib import pyplot as plt


if __name__ == '__main__':
    q_values = [0, 0.25, 0.5]

    diff_near_critical = [18 - 2, 29 - 2, 41 - 2]
    diff_in_between = [306 - 56, 213 - 30, 279 - 21]
    diff_near_percolation = [2667 - 383, 2105 - 171, 2983 - 247]

    plt.title("Variation of difference between fixed points of null model and TDP")
    plt.plot(q_values, diff_near_critical, '-o', label="near critical")
    plt.plot(q_values, diff_in_between, '-o', label="In between")
    plt.plot(q_values, diff_near_percolation, '-o', label="at percolation")
    plt.xlabel("q")
    plt.ylabel("difference")
    plt.legend()
    plt.show()