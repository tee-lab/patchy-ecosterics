from numpy import array, dot, zeros
from tqdm import tqdm


def f(x, w, b):
    return dot(x, w) + b


def get_cost(x, y, w, b):
    m = len(x)
    return sum((f(x, w, b) - y) ** 2) / (2 * m)


def get_grad(X, y, w, b):
    db = 0
    dw = zeros(len(w))
    m = len(X)

    for i in range(m):
        db += (f(X[i], w, b) - y[i])
        for j in range(len(w)):
            dw[j] += (f(X[i], w, b) - y[i]) * X[i][j]

    return dw / m, db / m
               

def gradient_descent(x, y, learning_rate, num_iterations):
    w = zeros(len(x[0]))
    b = 0

    for _ in tqdm(range(num_iterations)):
        dw, db = get_grad(x, y, w, b)
        w -= learning_rate * dw
        b -= learning_rate * db

    return w, b


if __name__ == '__main__':
    degree = 2
    x = array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    poly_func = lambda x: 1 + 2 * x + 3 * x * x
    y = poly_func(x)

    X = []
    for i in range(len(x)):
        X.append([x[i] ** j for j in range(1, degree + 1)])

    learning_rate = 0.0001
    num_iterations = 100000

    w, b = gradient_descent(X, y, learning_rate, num_iterations)
    print(w, b)
    print(get_cost(X, y, w))