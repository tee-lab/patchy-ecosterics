from numpy import mean, sum
from pickle import load
from os import path


def load_automaton_data(model_name, simulation_index):
    """ Loads a particular automaton data of a given model """
    model_path = path.join("models", model_name)
    file_path = path.join(path.dirname(__file__), model_path, f"simulation_{simulation_index}.pkl")

    with open(file_path, 'rb') as file:
        return load(file)
    

def perform_linear_regression(x, y):
    """ Performs a linear regression on the data """
    x_mean = mean(x)
    y_mean = mean(y)

    nume = 0
    deno = 0
    for i in range(len(x)):
        nume += (x[i] - x_mean) * (y[i] - y_mean)
        deno += (x[i] - x_mean)**2
    m = nume / deno
    c = y_mean - m * x_mean

    y_hat = m * x + c
    SSE = sum((y - y_hat)**2)
    SST = sum((y - y_mean)**2)
    r_squared = 1 - (SSE / SST)

    return m, c, r_squared