from utils import load_automaton_data


def print_cluster_data(model_name, simulation_index):
    automaton_data = load_automaton_data(model_name, simulation_index, "cluster")
    cluster_data, info = automaton_data["cluster_data"], automaton_data["info"]

    print(info)
    for iteration, update in enumerate(cluster_data):
        print(f"iteration {iteration}: {update}")


if __name__ == '__main__':
    print_cluster_data("contact_spatial", 0)