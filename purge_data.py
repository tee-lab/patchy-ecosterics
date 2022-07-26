import os


if __name__ == '__main__':
    model_name = "scanlon_kalahari"

    model_path = "models\\" + model_name
    folder_path = os.path.join(os.path.dirname(__file__), model_path)
    file_names = os.listdir(folder_path)

    for file_name in file_names:
        if file_name.endswith(".pkl") or file_name.endswith(".txt"):
            os.remove(os.path.join(folder_path, file_name))
            print(f"Removed {file_name}")