import numpy as np
import graph_utilities as gu

TRAINING_DATA_PERCENTAGE = ["50_50", "60_40", "70_30", "80_20"]


def get_training(user_id, training_data):

    if user_id == 0:
        training_path = "../training_data/" + training_data + "/all.csv"
    else:
        training_path = "../training_data/" + training_data + "/u" + str(user_id) + ".csv"

    return np.genfromtxt(training_path, delimiter=",", dtype=None)


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

                gu.increase_vertex(states_total_dict, states_dict, domain, current_path)

                for j in range(1, length_path):
                    gu.increase_edge(edges_total_dict, edges_dict, domain, current_path, current_path + "/" + path[j])
                    gu.increase_vertex(states_total_dict, states_dict, domain, current_path + "/" + path[j])
                    current_path = current_path + "/" + path[j]

        return True, states_dict, edges_dict, states_total_dict, edges_total_dict


def set_graph(user_id, training_data_percentage):
    (successful, states, edges, states_total, edges_total) = \
        convert_data_to_graph(user_id, training_data_percentage)
    if successful:
        gu.save_graph(user_id, training_data_percentage, states, edges, states_total, edges_total)


def set_all_graphs():
    for training_data_percentage in TRAINING_DATA_PERCENTAGE:
        for i in range(0, 28):
            set_graph(i, training_data_percentage)


set_all_graphs()
