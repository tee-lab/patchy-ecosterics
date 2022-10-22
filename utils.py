from pickle import load
import os


def load_automaton_data(model_name, simulation_index, data_type):
    """ Loads a particular automaton data of a given model """
    model_path = os.path.join("models", model_name)
    # folder_path = os.path.join(os.path.dirname(__file__), model_path)
    file_path = os.path.join(os.path.dirname(__file__), model_path, f"{data_type}_{simulation_index}.pkl")

    with open(file_path, 'rb') as file:
        return load(file)