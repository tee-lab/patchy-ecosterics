from numpy import loadtxt, transpose, zeros
from os import path


def load_changes(file_path):
    changes_data = transpose(loadtxt(open(path.join(file_path), 'r')))
    changes, changes_histogram = list(changes_data[0]), changes_data[1]
    changes_probabilities = changes_histogram / sum(changes_histogram)

    abs_changes = list(range(0, int(max(max(changes), -min(changes)))))
    abs_changes_histogram = [0] * len(abs_changes)

    for abs_change in abs_changes:
        value = 0

        if abs_change in changes:
            value += changes_probabilities[changes.index(abs_change)]
        if -abs_change in changes:
            value += changes_probabilities[changes.index(-abs_change)]
        
        abs_changes_histogram[abs_change] = value

    return abs_changes

    probability_distribution = abs_changes_histogram / sum(abs_changes_histogram)

    # return probability_distribution

    inverse_cdf = zeros(len(probability_distribution))

    for i in range(len(probability_distribution)):
        inverse_cdf[i] = sum(probability_distribution[i:])

    inverse_cdf = inverse_cdf / sum(inverse_cdf)

    return inverse_cdf