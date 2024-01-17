from numpy import array
from pickle import load


def load_lattices(path):
    bool_lattices = []
    with open(path, 'rb') as file:
        lattices = load(file)
        for lattice in lattices:
            bool_lattices.append(array(lattice, dtype=bool))
    
    return bool_lattices


# if __name__ == '__main__':
#     path = "C://Code//Github//vegetation-dynamics//results//tricritical//q0//paper//0p616//0p616_final_lattices.pkl"
#     lattices = load_lattices(path)
    # print(lattices)