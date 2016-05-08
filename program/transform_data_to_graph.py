#!python2

import numpy as np
import graph_utilities as gu

NAIVE_METHODS = ["50_50", "60_40", "70_30", "80_20"]

K_FOLD_METHODS = ["3fold", "4fold", "5fold"]


def learn_model(file_url):
    (successful, states, edges, states_total, edges_total) = \
        convert_data_to_graph(-1, "", file_url)
    if successful:
        gu.save_graph("", "", -1, states, edges,
                      states_total, edges_total)
    else:
        raise IOError


def get_training_data(user_id, method, parameter):
    training_path = parameter
    if user_id != -1:
        if method == "naive":
            if user_id == 0:
                training_path = "../training_data/" + parameter + "/all.csv"
            else:
                training_path = "../training_data/" + parameter + "/u" + \
                                str(user_id) + ".csv"
        else:
            if user_id == 0:
                training_path = "../training_data/" + method + "/" + parameter + \
                                "/all.csv"
            else:
                training_path = "../training_data/" + method + "/" + parameter + \
                                "/u" + str(user_id) + ".csv"

    return np.genfromtxt(training_path, delimiter=",", dtype=None)


def convert_data_to_graph(uid, method, parameter):

        states_dict = {}
        edges_dict = {}
        states_total_dict = {}
        edges_total_dict = {}

        try:
            dataset = get_training_data(uid, method, parameter)
        except IOError:
            return False, states_dict, edges_dict, states_total_dict, \
                   edges_total_dict

        limit = len(dataset)

        for i in range(0, limit):

            path = filter(lambda x: x != "", dataset[i][1].split("/"))

            domain = path[0]
            current_path = path[0]
            length_path = len(path)

            if len(path) > 0:

                gu.increase_vertex(states_total_dict, states_dict, domain,
                                   current_path)

                for j in range(1, length_path):
                    gu.increase_edge(edges_total_dict, edges_dict, domain,
                                current_path, current_path + "/" + path[j])
                    gu.increase_vertex(states_total_dict, states_dict,
                                domain, current_path + "/" + path[j])
                    current_path = current_path + "/" + path[j]

        return True, states_dict, edges_dict, states_total_dict,\
               edges_total_dict


def set_graph(user_id, method, parameter):
    (successful, states, edges, states_total, edges_total) = \
        convert_data_to_graph(user_id, method, parameter)
    if successful:
        gu.save_graph(method, parameter, user_id, states, edges,
                      states_total, edges_total)


def set_all_graphs():
    # Graph for naive method
    for naive_method in NAIVE_METHODS:
        for i in range(0, 28):
            set_graph(i, "naive", naive_method)

    # Graph for 3-fold method
    for i in range(1, 4):
        parameter = "iter"+str(i)
        for u in range(0, 28):
            set_graph(u, K_FOLD_METHODS[0], parameter)

    # Graph for 4-fold method
    for i in range(1, 5):
        parameter = "iter" + str(i)
        for u in range(0, 28):
            set_graph(u, K_FOLD_METHODS[1], parameter)

    # Graph for 5-fold method
    for i in range(1, 6):
        parameter = "iter" + str(i)
        for u in range(0, 28):
            set_graph(u, K_FOLD_METHODS[2], parameter)

# set_all_graphs()
