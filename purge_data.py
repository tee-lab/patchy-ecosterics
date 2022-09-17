import os


def purge_data(model_name = None):
    """ Clears all simulation data in the given model's directory """

    if model_name == None:
        purge_data("contact_spatial")
        purge_data("scanlon_kalahari")
        purge_data("tricritical")
        purge_data("null")
        return

    model_path = "models\\" + model_name
    folder_path = os.path.join(os.path.dirname(__file__), model_path)
    file_names = os.listdir(folder_path)

    for file_name in file_names:
        if file_name.endswith(".pkl") or file_name.endswith(".txt"):
            os.remove(os.path.join(folder_path, file_name))
            print(f"Removed {file_name}")


if __name__ == '__main__':
    purge_data()