from matplotlib import pyplot as plt
from math import sqrt
from numpy import arange, exp, pi


def simpson(f, a, b, n):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n, 2):
        s += 4 * f(a + i * h)
    for i in range(2, n - 1, 2):
        s += 2 * f(a + i * h)
    return s * h / 3


if __name__ == '__main__':
    a = 0.1
    b = 50
    exponent = 2

    x = arange(a, b, 0.01)
    power_law_norm = simpson(lambda x: x ** (-exponent), a, b, 10000)
    power_law = x ** (-exponent) / power_law_norm
    exponential = exp(-x)
    gaussian = exp(-x ** 2) * 2 / sqrt(pi)

    label_size = 14
    title_size = 16

    plt.subplots(figsize=(10, 20))
    plt.subplot(3, 1, 1)
    plt.title("Comparison of Distributions", fontsize=title_size)
    plt.xlabel("x", fontsize=label_size)
    plt.ylabel("f(x)", fontsize=label_size)
    plt.plot(x, power_law, label="Power Law")
    plt.plot(x, exponential, label="Exponential")
    plt.plot(x, gaussian, label="Gaussian")
    plt.xlim(0, 5)
    plt.ylim(0, 2)
    plt.legend()
    
    plt.subplot(3, 1, 2)
    plt.title("Comparison of Distributions (log-log)", fontsize=title_size)
    plt.xlabel("x", fontsize=label_size)
    plt.ylabel("f(x)", fontsize=label_size)
    plt.loglog(x, power_law, label="Power Law")
    plt.loglog(x, exponential, label="Exponential")
    plt.loglog(x, gaussian, label="Gaussian")
    plt.legend()
    
    plt.subplot(3, 1, 3)
    plt.title("Comparison of Distributions (semilogy)", fontsize=title_size)
    plt.xlabel("x", fontsize=label_size)
    plt.ylabel("f(x)", fontsize=label_size)
    plt.semilogy(x, power_law, label="Power Law")
    plt.semilogy(x, exponential, label="Exponential")
    plt.semilogy(x, gaussian, label="Gaussian")
    plt.legend()
    plt.savefig("power_law_comparison.png", bbox_inches="tight")
    plt.show()
    plt.close()