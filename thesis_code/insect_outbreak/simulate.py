def x_dot(x, r, k):
    g = r * x * (1 - x / k)
    p = x / (1 + x ** 2)
    return g - p


def simulate(x0, r, k):
    x = x0
    for _ in range(time):
        x += x_dot(x, r, k)
    return x


if __name__ == '__main__':
    time = 10000

    r = 0.5
    k = 30

    steady_state = simulate(1, r, k)
    print(steady_state)