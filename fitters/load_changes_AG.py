from numpy import array, loadtxt, transpose, zeros
from os import path


def load_changes(file_path):
    changes_data = transpose(loadtxt(open(path.join(file_path), 'r')))
    changes, changes_histogram = list(changes_data[0]), changes_data[1]

    abs_changes = list(range(0, int(max(max(changes), -min(changes)))))
    abs_changes_histogram = [0] * len(abs_changes)

    for abs_change in abs_changes:
        value = 0

        if abs_change in changes:
            value += changes_histogram[changes.index(abs_change)]
        if -abs_change in changes:
            value += changes_histogram[changes.index(-abs_change)]

        abs_changes_histogram[abs_change] = value

    # Here we do not compute the inverse cumulative distribution, but return
    # the number of times each dS appears (the raw histogram)

    # icdf_histogram = zeros(len(abs_changes_histogram))
    # for i in range(len(abs_changes_histogram)):
        # icdf_histogram[i] = sum(abs_changes_histogram[i:])

    return array(abs_changes_histogram, dtype=int)


# if __name__ == '__main__':
#     output = load_changes("C://Code//Github//vegetation-dynamics//results/tricritical/q0/100x100_residue/0p616/0p616_changes.txt")
#     print(output)
