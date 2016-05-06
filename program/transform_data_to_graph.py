"""

"""

import numpy as np
import pickle as pk

TRAINING_DATA_PERCENTAGE = ["50_50", "60_40", "70_30", "80_20"]


def get_training(user_id, training_data):

    if user_id == 0:
        training_path = "../training_data/" + training_data + "/all.csv"
    else:
        training_path = "../training_data/" + training_data + "/u" + str(user_id) + ".csv"

    return np.genfromtxt(training_path, delimiter=",", dtype=None)

"""
 Increases by one the value of the transversed vertex of the given domain
"""


def increase_vertex(states_total_dict, dictionary, domain, vertex):
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


def increase_edge(edges_total_dict, dictionary, domain, outgoing, ingoing):
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
 Transform the CSV file with the training data into a graph representation using the dictionaries states_dict and
 edges_dict
"""


def convert_data_to_graph(uid, training_data_percentage):

        states_dict = {}
        edges_dict = {}
        states_total_dict = {}
        edges_total_dict = {}

        try:
            dataset = get_training(uid, training_data_percentage)
        except IOError:
            return False, states_dict, edges_dict, states_total_dict, edges_total_dict

        limit = len(dataset)

        for i in range(0, limit):

            path = filter(lambda x: x != "", dataset[i][1].split("/"))

            domain = path[0]
            current_path = path[0]
            length_path = len(path)

            if len(path) > 0:

                increase_vertex(states_total_dict, states_dict, domain, current_path)

                for j in range(1, length_path):
                    increase_edge(edges_total_dict, edges_dict, domain, current_path, current_path + "/" + path[j])
                    increase_vertex(states_total_dict, states_dict, domain, current_path + "/" + path[j])
                    current_path = current_path + "/" + path[j]

        return True, states_dict, edges_dict, states_total_dict, edges_total_dict


def save_obj(obj, training_data_percentage, name):
    with open('../graphs/' + training_data_percentage + "/" + name + '.pkl', 'wb') as f:
        pk.dump(obj, f, pk.HIGHEST_PROTOCOL)


def set_graph(user_id, training_data_percentage):
    (successful, states_dict, edges_dict, states_total_dict, edges_total_dict) = \
        convert_data_to_graph(user_id, training_data_percentage)
    if successful:
        save_obj(edges_dict, training_data_percentage, "edges_" + str(user_id))
        save_obj(states_dict, training_data_percentage, "states_" + str(user_id))
        save_obj(states_total_dict, training_data_percentage, "total_states_" + str(user_id))
        save_obj(edges_total_dict, training_data_percentage, "total_edges_" + str(user_id))


def set_all_graphs():
    for training_data_percentage in TRAINING_DATA_PERCENTAGE:
        for i in range(0, 28):
            set_graph(i, training_data_percentage)


set_all_graphs()
