from matplotlib import pyplot as plt
from numpy import loadtxt, transpose
from sklearn.linear_model import LinearRegression
from os import path


if __name__ == '__main__':
    limit = 200
    p = [0.7, 0.71, 0.72, 0.73, 0.74]
    folder_names = [str(p_value).replace('.', 'p') for p_value in p]

    for i, folder_name in enumerate(folder_names):
        file_name = str(p[i]).replace('.', 'p') + '_cluster_ds.txt'
        file_path = path.join(path.dirname(__file__), folder_name, file_name)
        
        data = transpose(loadtxt(file_path, dtype=float, delimiter=' '))
        cluster_sizes, mean_ds, mean_ds_sq, num = data[0], data[1], data[2], data[3]

        model = LinearRegression()
        model.fit(X=cluster_sizes[2:limit].reshape(-1, 1), y=mean_ds_sq[2:limit])
        score = model.score(X=cluster_sizes[2:limit].reshape(-1, 1), y=mean_ds_sq[2:limit])

        print(f"for p = {p[i]}: g(x)^2 slope = {model.coef_}, intercept = {model.intercept_}, R^2 = {score}")

        plt.plot(cluster_sizes[2:limit], mean_ds_sq[2:limit])
        plt.show()