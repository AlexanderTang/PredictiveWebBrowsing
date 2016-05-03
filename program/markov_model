"""
ASSUMPTIONS:
    - The dataset contains load actions only
    - The data set is the training set
"""

import numpy as np
from hmmlearn import hmm

IS_STATE_THRESHOLD = 20
states_dict = {}          # States and the number of times the user transverses them
edges_dict = {}           # Edges and the number of times the user transverses them
modifications_dict = {}   # Tuple (domain, modified_vertex) mapping the modified fragment of a path with the real name

probabilities_vertex_by_domain = {}
transition_matrix_by_domain = {}
id_dict_by_domain = {}
useless_domain = []
"""
 Increases by one the value of the transversed vertex of the given domain
"""


def increase_vertex(dictionary, domain, vertex):
    if domain in dictionary:
        if vertex in dictionary[domain]:
            dictionary[domain][vertex] += 1
        else:
            dictionary[domain].update({vertex: 1})
    else:
        dictionary[domain] = {vertex: 1}

"""
 Increases by one the value of the transversed edge of the given domain
"""


def increase_edge(dictionary, domain, outgoing, ingoing):
    if domain in dictionary:
        if outgoing in dictionary[domain]:
            if ingoing in dictionary[domain][outgoing]:
                dictionary[domain][outgoing][ingoing] += 1
            else:
                dictionary[domain][outgoing].update({ingoing: 1})
        else:
            dictionary[domain].update({outgoing: {ingoing: 1}})
    else:
        dictionary[domain] = {outgoing: {ingoing: 1}}

"""
 Compare two domains with their paths and return true if:
   - User goes back from page X to page Y in the next click
   - User changes from page X to page Y and keeps the same deep in the tree, where X and Y are different
   - User changes domain from page X in next click Y
"""


def is_useful_path(dataset, x, y):
    # We reach the last element of the dataset, we switch the latter one with the former one
    if len(dataset) == y:
        # User stayed in the same domain
        if dataset[x-1][2] == dataset[x][2]:
            # User went back in the next click
            if len(dataset[x-1][3].split("/")) < len(dataset[x][3].split("/")):
                return True
            else:
                # User might have changed to other page and kept the same deep in the tree
                if len(dataset[x-1][3].split("/")) == len(dataset[x][3].split("/")):
                    # User changed to other page and kept the same deep in the tree
                    if dataset[x-1][3] != dataset[x][3]:
                        return True
                    else:
                        return False
                else:
                    return False
        # User changed domain in next click
        else:
            return True
    else:
        # User stays in the same domain
        if dataset[x][2] == dataset[y][2]:
            # User goes back in the next click
            if len(dataset[x][3].split("/")) > len(dataset[y][3].split("/")):
                return True
            else:
                # User might change to other page and keep the same deep in the tree
                if len(dataset[x][3].split("/")) == len(dataset[y][3].split("/")):
                    # User changes to other page and keeps the same deep in the tree
                    if dataset[x][3] != dataset[y][3]:
                        return True
                    else:
                        return False
                else:
                    return False
        # User changes domain in next click
        else:
            return True


"""
 Transform the CSV file with the training data into a graph representation using the dictionaries states_dict and
 edges_dict
"""


def set_graph(uid):

    # Set states and edges for the entire dataset, no user distinction
    if uid == -1:
        # dataset = np.genfromtxt('../processed_data/dummy_data.csv', delimiter=",", dtype=None,
        dataset = np.genfromtxt('../processed_data/deep_filtered_data.csv', delimiter=",", dtype=None,
                                names=["ts", "action", "dom", "path", "uid"])
        limit = len(dataset)

        for i in range(0, limit):

            if is_useful_path(dataset, i, i+1):

                domain = dataset[i][2]
                path = filter(lambda a: a != "", dataset[i][3].split("/"))
                length_path = len(path) - 1

                increase_vertex(states_dict, domain, domain)

                if len(path) > 0:
                    increase_edge(edges_dict, domain, domain, path[0])

                    for j in range(0, length_path):
                        # Current path's fragment name is different of the next path's fragment name
                        if path[j] != path[j + 1]:
                            increase_edge(edges_dict, domain, path[j], path[j + 1])
                        # Current path's fragment name is equal to the next path's fragment name
                        else:
                            # Changing name of the next path's fragment and storing in a dictionary to reconstruct the
                            # URL
                            temporal_path = path[j + 1] + "[!]" + str(7 * j)
                            if not (domain, temporal_path) in modifications_dict:
                                modifications_dict[(domain, temporal_path)] = path[j + 1]

                            increase_edge(edges_dict, domain, path[j], temporal_path)
                            path[j + 1] = temporal_path

                        increase_vertex(states_dict, domain, path[j])

                    increase_vertex(states_dict, domain, path[length_path])


    # Set states and edges for the specific user in the dataset
    else:
        raise ValueError('Method not implemented')


"""
It's probable that we need to use the inverse_id_dict_by_domain as well
"""
def set_id_by_domain(domain):
    inverse_id_dict_by_domain = dict(enumerate(states_dict[domain].keys()))
    id_dict_by_domain[domain] = {v: k for k, v in inverse_id_dict_by_domain.items()}


# Not sure how the dictionaries is apply, I guessing it is in the same order as states_dict[domain].keys()
def set_vertices_probabilities(domain):
    visits_by_vertex = np.array(states_dict[domain].values(), dtype="float")
    total_vertices_visits = np.sum(visits_by_vertex)
    probabilities_vertex_by_domain[domain] = map(lambda x: x / total_vertices_visits, visits_by_vertex)
    return len(visits_by_vertex)


def set_edges_probabilities(domain, amount_vertices):
    visits_by_edge = np.zeros([amount_vertices, amount_vertices])

    for outgoing in edges_dict[domain]:
        for ingoing in edges_dict[domain][outgoing]:
            visits_by_edge[id_dict_by_domain[domain][outgoing], id_dict_by_domain[domain][ingoing]] = \
                edges_dict[domain][outgoing][ingoing]

    total_edges_visits = np.apply_along_axis(sum, axis=1, arr=visits_by_edge)

    for i in range(0, amount_vertices-1):
        if total_edges_visits[i] > 0:
            visits_by_edge[i, :] = map(lambda x: x / total_edges_visits[i], visits_by_edge[i, :])

    transition_matrix_by_domain[domain] = visits_by_edge


def convert_graph_to_matrix():
    for domain in states_dict:
        if states_dict[domain][domain] < IS_STATE_THRESHOLD:
            useless_domain.append(domain)

    for domain in useless_domain:
        del states_dict[domain]
        del edges_dict[domain]

    for domain in states_dict:
        set_id_by_domain(domain)
        amount_vertices_by_domain = set_vertices_probabilities(domain)
        set_edges_probabilities(domain, amount_vertices_by_domain)

set_graph(-1)

convert_graph_to_matrix()

"""
************************************************************************************************************************
"""
