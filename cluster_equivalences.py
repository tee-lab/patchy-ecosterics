from itertools import product


def establish_equivalences(lattice_1, lattice_2):
    """ returns (and prints) equivalences between clusters of two lattices """
    relationships = get_relationships(lattice_1, lattice_2)
    ancestries = get_common_ancestors(relationships)
    descents = get_common_descendents(relationships)

    print("\n---> Cluster splits <---")
    for ancestry in ancestries:
        if len(ancestry[1]) > 1:
            ancestor = f"Cluster {ancestry[0]} in lattice 1 split into to clusters"
            descendents = " ".join([f"{descendant}" for descendant in ancestry[1]]) + " in lattice 2"
            print(f"{ancestor} {descendents}")

    print("\n---> Cluster mergers <---")
    for descent in descents:
        if len(descent[1]) > 1:
            descendent = f"merged to form cluster {descent[0]} in lattice 2"
            ancestors = "Clusters " + " ".join([f"{ancestor}" for ancestor in descent[1]]) + " in lattice 1"
            print(f"{ancestors} {descendent}")

    return ancestors, descendents


def get_relationships(lattice_1, lattice_2):
    relationships = []

    for i, j in product(range(len(lattice_1)), repeat=2):
        if lattice_1[i][j] and lattice_2[i][j]:
            relationship = (lattice_1[i][j], lattice_2[i][j])
            if relationship not in relationships:
                relationships.append(relationship)

    return relationships


def get_common_ancestors(relationships):
    relationships = sorted(relationships, key=lambda x: x[0])
    ancestries = []
    for i, relationship in enumerate(relationships):
        if len(ancestries) and ancestries[-1][0] == relationship[0]:
            continue
        else:
            ancestor = relationship[0]
            descendents = []

            j = i
            while relationships[j][0] == ancestor:
                descendents.append(relationships[j][1])
                j += 1
                if j == len(relationships):
                    break

            ancestries.append([ancestor, descendents])

    return ancestries


def get_common_descendents(relationships):
    relationships = sorted(relationships, key=lambda x: x[1])
    descents = []
    for i, relationship in enumerate(relationships):
        if len(descents) and descents[-1][0] == relationship[1]:
            continue
        else:
            descendent = relationship[1]
            ancestors = []

            j = i
            while relationships[j][1] == descendent:
                ancestors.append(relationships[j][0])
                j += 1
                if j == len(relationships):
                    break

            descents.append([descendent, ancestors])

    return descents