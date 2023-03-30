from matplotlib import pyplot as plt
from numpy import arange, exp


if __name__ == '__main__':
    x = arange(0.01, 10, 0.01)
    power_law = x ** (-2)
    exponential = exp(-x)
    gaussian = exp(-x ** 2)

    plt.title("Comparison of Distributions")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.plot(x, power_law, label="Power Law")
    plt.plot(x, exponential, label="Exponential")
    plt.plot(x, gaussian, label="Gaussian")
    plt.xlim(0, 5)
    plt.ylim(0, 2)
    plt.legend()
    plt.savefig("power_law_comparison.png")
    plt.show()