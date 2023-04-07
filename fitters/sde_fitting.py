from matplotlib import pyplot as plt
from numpy import loadtxt, transpose
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from os import path


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

        cutoff_index = 0
        for i in range(len(num_points)):
            if num_points[i] < data_cutoff:
                cutoff_index = i
                break

        data = mean_ds[1:cutoff_index]
        x = cluster_sizes[1:cutoff_index]

        poly = PolynomialFeatures(degree=3)
        x_poly = poly.fit_transform(x.reshape(-1, 1))
        model = LinearRegression()
        model.fit(x_poly, data)
        print(f"p = {p_value}: {model.intercept_} {model.coef_[1:]}")
        print("R^2 = " + str(model.score(x_poly, data)))

        data_fit = model.predict(x_poly)

        plt.title(f"Mean dS vs Cluster Size for p = {p_value}")
        plt.plot(x, data, label="p = " + str(p_value))
        plt.plot(x, data_fit, label="Fit")
        plt.plot([0, cluster_sizes[cutoff_index - 1]], [0, 0])
        plt.legend()
        plt.show()