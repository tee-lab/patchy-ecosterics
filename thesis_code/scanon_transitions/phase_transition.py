from matplotlib import pyplot as plt


if __name__ == '__main__':
    slope = 0.0008588
    y_intercept = -0.1702
    rainfall_values = [50 * x for x in range(0, 18)]
    
    y = [max(slope * x + y_intercept, 0) for x in rainfall_values]

    plt.title('Bifurcation diagram of Scanlon model')
    plt.xlabel('Rainfall (mm/year)')
    plt.ylabel('Steady state density')
    plt.plot(rainfall_values, y)
    plt.plot(rainfall_values[4:], [0 for _ in range(4, 18)], linestyle='dashed')
    plt.show()