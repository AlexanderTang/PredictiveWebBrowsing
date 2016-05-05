"""
ASSUMPTIONS:
    - The dataset contains load actions only
    - The data set is the training set

Questions:
    - Does we really need to save the domain as a state?
    - Is it better to have precomputed the probabilities and store them in a data structure (for instance a dictionary)
        or to compute the probabilities when they are needed them (in the search method)?
"""

import numpy as np
import pickle as pk

IS_STATE_THRESHOLD = 20

states_dict = {}            # States and the number of times the user transverses them
edges_dict = {}             # Edges and the number of times the user transverses them
states_total_dict = {}      # Total amount that the user transversed the states by domain
edges_total_dict = {}       # Total amount that the user transversed the edges by domain

"""
 Increases by one the value of the transversed vertex of the given domain
"""


def increase_vertex(dictionary, domain, vertex):
    if domain in dictionary:
        if vertex in dictionary[domain]:
            dictionary[domain][vertex] += 1
        else:
            dictionary[domain].update({vertex: 1})
        states_total_dict[domain] += 1
    else:
        dictionary[domain] = {vertex: 1}
        states_total_dict[domain] = 1

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
            edges_total_dict[domain][outgoing] += 1
        else:
            dictionary[domain].update({outgoing: {ingoing: 1}})
            edges_total_dict[domain].update({outgoing: 1})
    else:
        dictionary[domain] = {outgoing: {ingoing: 1}}
        edges_total_dict[domain] = {outgoing: 1}

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


def convert_data_to_graph(uid):

    states_dict.clear()
    edges_dict.clear()
    states_total_dict.clear()
    edges_total_dict.clear()

    dataset = np.genfromtxt('../processed_data/deep_filtered_data.csv', delimiter=",", dtype=None,
                            names=["ts", "action", "dom", "path", "uid"])
    limit = len(dataset)

    for i in range(0, limit):
        if uid == dataset[i][4] or uid == -1:
            if is_useful_path(dataset, i, i + 1):
                domain = dataset[i][2]
                path = filter(lambda x: x != "", dataset[i][3].split("/"))
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
                            temporal_path = path[j + 1] + "[!" + str(7 * j) + "!]"
                            #if not (domain, temporal_path) in modifications_dict:
                                #modifications_dict[(domain, temporal_path)] = path[j + 1]

                            increase_edge(edges_dict, domain, path[j], temporal_path)
                            path[j + 1] = temporal_path

                        increase_vertex(states_dict, domain, path[j])

                    increase_vertex(states_dict, domain, path[length_path])


def convert_graph_to_matrix():
    useless_domain = []

    for domain in states_dict:
        if states_dict[domain][domain] < IS_STATE_THRESHOLD:
            useless_domain.append(domain)

    for domain in useless_domain:
        del states_dict[domain]
        del edges_dict[domain]


def save_obj(obj, name ):
    with open('../graphs/' + name + '.pkl', 'wb') as f:
        pk.dump(obj, f, pk.HIGHEST_PROTOCOL)


def set_graph(user_id):

    if user_id == -1:
        convert_data_to_graph(user_id)
        save_obj(edges_dict, "edges_all")
        save_obj(states_dict, "states_all")
        save_obj(states_total_dict, "total_states_all")
        save_obj(edges_total_dict, "total_edges_all")
    else:
        convert_data_to_graph(user_id)
        if states_dict:
            save_obj(edges_dict, "edges_" + str(user_id))
            save_obj(states_dict, "states_" + str(user_id))
            save_obj(states_total_dict, "total_states_" + str(user_id))
            save_obj(edges_total_dict, "total_edges_" + str(user_id))


set_graph(-1)
for i in range(1, 28):
    set_graph(i*1.0)

