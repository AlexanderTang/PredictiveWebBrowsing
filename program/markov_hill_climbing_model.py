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

IS_STATE_THRESHOLD = 20
#DELTA_THRESHOLD = .10
#DELTA_THRESHOLD = .15
DELTA_THRESHOLD = .20

states_dict = {}            # States and the number of times the user transverses them
edges_dict = {}             # Edges and the number of times the user transverses them
modifications_dict = {}     # Tuple (domain, modified_vertex) mapping the modified fragment of a path with the real name
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


def set_graph(uid):

    # Set states and edges for the entire dataset, no user distinction
    if uid == -1:

        dataset = np.genfromtxt('../processed_data/deep_filtered_data.csv', delimiter=",", dtype=None,
                                names=["ts", "action", "dom", "path", "uid"])
        limit = len(dataset)

        for i in range(0, limit):

            if is_useful_path(dataset, i, i+1):

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
                            temporal_path = path[j + 1] + "[!" + str(7 * j) + "]"
                            if not (domain, temporal_path) in modifications_dict:
                                modifications_dict[(domain, temporal_path)] = path[j + 1]

                            increase_edge(edges_dict, domain, path[j], temporal_path)
                            path[j + 1] = temporal_path

                        increase_vertex(states_dict, domain, path[j])

                    increase_vertex(states_dict, domain, path[length_path])


    # Set states and edges for the specific user in the dataset
    else:
        raise ValueError('Method not implemented')


def convert_graph_to_matrix():
    useless_domain = []

    for domain in states_dict:
        if states_dict[domain][domain] < IS_STATE_THRESHOLD:
            useless_domain.append(domain)

    for domain in useless_domain:
        del states_dict[domain]
        del edges_dict[domain]


"""
    This search is a modification of the Hill Climbing search algorithm
"""


def search(domain, visited):
    last_url = ""
    while next and len(visited) > 0:
        outgoing = visited.pop(0)

        # we verify with the current node has edges, if that is not case we have reached the deepest path
        if outgoing[1] in edges_dict[domain]:
            temp = []
            for ingoing in edges_dict[domain][outgoing[1]]:
                """
                Here we need a threshold to see if it possible to advance or if it is better to stay in the node and
                don't go deeper in the path because could be the following case.
                This can also sole the problem where we have for example many a path a/b/c that is frequently visited,
                but the actual last pages are a/b/c/z, a/b/c/x and a/b/c/y but maybe the user only visited them once each
                while path a/b/c was visited 20 times. So I think the best prediction should be path a/b/c instead of
                the deepest one (either a/b/c/z, a/b/c/x or a/b/c/y).

                Right now I'm considering a delta among the probability of being the current state and the probability of
                being in the next state, if such delta is less that a THRESHOLD then is  more likely that the user goes
                deeper in the path, otherwise the user might stay there.
                """
                current_state_probability = states_dict[domain][outgoing[1]] / (states_total_dict[domain] * 1.0)
                next_state_probability = states_dict[domain][ingoing] / (states_total_dict[domain] * 1.0)
                delta = current_state_probability - next_state_probability
                print "current: ", outgoing[1], current_state_probability
                print "next: ", ingoing, next_state_probability
                if delta < DELTA_THRESHOLD:
                    edge_probability = \
                        edges_dict[domain][outgoing[1]][ingoing] / (edges_total_dict[domain][outgoing[1]] * -1.0)
                    new_path = outgoing[2] + "/" + ingoing
                    temp.append((edge_probability, ingoing, new_path))
            if len(temp) > 0:
                temp = sorted(temp, key=lambda x: x[0])
                visited = visited + [temp[0]]
                last_url = temp[0][2]
            else:
                last_url = outgoing[2]
        else:
            break
    return last_url

"""
    predict the most likely path for the given page and the given domain
"""


def get_prediction(domain, fragment_url):
    visited = [(0, fragment_url, fragment_url)]
    raw_url = search(domain, visited)
    return raw_url


set_graph(-1)

convert_graph_to_matrix()

print get_prediction("onderwijsaanbod.kuleuven.be", "opleidingen")


