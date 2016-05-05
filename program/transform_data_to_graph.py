"""
ASSUMPTIONS:
    - The dataset contains load actions only
    - The data set is the training set

Questions:
    - Does we really need to save the domain as a state?
    - Is it better to have precomputed the probabilities and store them in a data structure (for instance a dictionary)
        or to compute the probabilities when they are needed them (in the search method)?
"""

from sklearn.cross_validation import train_test_split
import numpy as np
import pickle as pk
import csv

TESTING_DATA_PERCENTAGE = 0.66

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

        states_dict = {}
        edges_dict = {}
        states_total_dict = {}
        edges_total_dict = {}

        try:
            dataset = set_training_testing_data(uid)
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


def save_obj(obj, name ):
    with open('../graphs/' + name + '.pkl', 'wb') as f:
        pk.dump(obj, f, pk.HIGHEST_PROTOCOL)


def set_graph(user_id):
    (successful, states_dict, edges_dict, states_total_dict, edges_total_dict) = convert_data_to_graph(user_id)
    if successful:
        save_obj(edges_dict, "edges_" + str(user_id))
        save_obj(states_dict, "states_" + str(user_id))
        save_obj(states_total_dict, "total_states_" + str(user_id))
        save_obj(edges_total_dict, "total_edges_" + str(user_id))


def set_training_testing_data(user_id):

    if user_id == 0:
        raw_data = np.genfromtxt('../ground_truth/gt_all.csv', delimiter=",", dtype=None,
                                names=["ts", "action", "dom", "path", "uid"])
    else:
        file_path = "../ground_truth/gt_u" + str(user_id) + ".csv"
        raw_data = np.genfromtxt(file_path, delimiter=",", dtype=None,
                                names=["ts", "action", "dom", "path", "uid"])

    training_data, testing_data = train_test_split(raw_data, test_size=TESTING_DATA_PERCENTAGE)

    training_path = "../training_data/training_" + str(user_id) + ".csv"
    testing_path = "../testing_data/testing_" + str(user_id) + ".csv"

    with open(training_path, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in training_data:
            csvwriter.writerow(row)

    with open(testing_path, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in testing_data:
            csvwriter.writerow(row)

    return training_data


def load_obj(name):
    with open('../graphs/' + name + '.pkl', 'rb') as f:
        return pk.load(f)

#for i in range(0, 28):
#    set_graph(i)

#set_graph(0)

#test = load_obj("states_0")
#print test

raw_data = np.genfromtxt('../processed_data/testing.csv', delimiter=",", dtype=None,
                         names=["ts", "action", "dom", "path", "uid"])

limit = len(raw_data)

with open("../test/daniel.csv", 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    for i in range(0, limit):
        if is_useful_path(raw_data, i, i+1):
            text = [raw_data[i][2], raw_data[i][2] + raw_data[i][3]]
            csvwriter.writerow(text)
