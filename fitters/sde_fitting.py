from matplotlib import pyplot as plt
from numba import njit
from numpy import arange, array, dot, loadtxt, ones, transpose, zeros
from numpy.random import random
from os import path
from tqdm import tqdm


@njit
def f(x, w, b):
    return dot(x, w) + b


@njit
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
    data_cutoff = 10000
    q_value = 0
    p_values = [round(0.65 + 0.01 * i, 2) for i in range(1, 8)]
    dataset = "100x100"

    root_path = path.join(path.dirname(__file__), "..")
    q_folder = "q" + str(q_value).replace(".", "p")

    for p_value in p_values:
        p_folder = str(p_value).replace(".", "p")
        file_name = p_folder + "_cluster_ds.txt"
        folder_path = path.join(root_path, "results", "tricritical", q_folder, dataset, p_folder)

        data = transpose(loadtxt(path.join(folder_path, file_name)))
        cluster_sizes, mean_ds, num_points = data[0], data[1], data[3]

        # cutoff_index = 0
        # for i in range(len(num_points)):
        #     if num_points[i] < data_cutoff:
        #         cutoff_index = i
        #         break

        cutoff_index = 50

        y = mean_ds[1:cutoff_index]
        x = cluster_sizes[1:cutoff_index]

        # output_string = ""
        # for i in range(len(x)):
        #     output_string += str(x[i]) + "\t" + str(y[i]) + "\n"
        
        # with open("output.txt", "w") as file:
        #     file.write(output_string)

        # _ = input()

        degree = 2
        X = []
        for i in range(len(x)):
            X.append([x[i] ** j for j in range(1, degree + 1)])
        X = array(X)

        column_means = X.mean(axis=0)
        column_stds = X.std(axis=0)

        X_scaled = (X - column_means) / column_stds

        learning_rate = 0.01
        num_iterations = 10000

        w, b = gradient_descent(X_scaled, y, learning_rate, num_iterations)
        print(b, w)
        print(get_cost(X_scaled, y, w, b))

        y_pred = f(X_scaled, w, b)

        plt.plot(x, y, "o")
        plt.plot(x, y_pred)
        plt.show()