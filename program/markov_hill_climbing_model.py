"""
ASSUMPTIONS:
    - The dataset contains load actions only
    - The data set is the training set

Questions:
    - Does we really need to save the domain as a state?
    - Is it better to have precomputed the probabilities and store them in a data structure (for instance a dictionary)
        or to compute the probabilities when they are needed them (in the search method)?
"""

import pickle as pk
import numpy as np

#DELTA_THRESHOLD = .10
#DELTA_THRESHOLD = .15
DELTA_THRESHOLD = .20

states_dict = {}            # States and the number of times the user transverses them
edges_dict = {}             # Edges and the number of times the user transverses them
states_total_dict = {}      # Total amount that the user transversed the states by domain
edges_total_dict = {}       # Total amount that the user transversed the edges by domain


def load_obj(name):
    with open('../graphs/' + name + '.pkl', 'rb') as f:
        return pk.load(f)

"""
    This search is a modification of the Hill Climbing search algorithm
"""


def hill_climbing_search(domain, visited):
    last_url = ""
    while len(visited) > 0:
        outgoing = visited.pop(0)
        last_url = outgoing[1]
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

                Right now I'm considering a delta among the probabilities of being the current state and the probability
                of being in the next state, if such delta is less that a THRESHOLD then is  more likely that the user
                goes deeper in the path, otherwise the user might stay there.
                """
                current_state_probability = states_dict[domain][outgoing[1]] / (states_total_dict[domain] * 1.0)
                next_state_probability = states_dict[domain][ingoing] / (states_total_dict[domain] * 1.0)
                confident_interval = current_state_probability - next_state_probability

                if confident_interval < DELTA_THRESHOLD:
                    edge_probability = \
                        edges_dict[domain][outgoing[1]][ingoing] / (edges_total_dict[domain][outgoing[1]] * -1.0)

                    temp.append((edge_probability, ingoing))
            if len(temp) > 0:
                temp = sorted(temp, key=lambda x: x[0])
                visited = visited + [temp[0]]
                last_url = temp[0][1]

        else:
            break
    return last_url


"""
    Predict the most likely path for the given page and the given domain
"""


def get_prediction(domain, path):
    prediction = path
    if domain in states_dict:
        visited = [(1, path)]
        prediction = hill_climbing_search(domain, visited)
    return prediction


def load_data(uid):
    global edges_dict
    global states_dict
    global edges_total_dict
    global states_total_dict

    edges_dict = load_obj("edges_" + str(uid))
    states_dict = load_obj("states_" + str(uid))
    edges_total_dict = load_obj("total_edges_" + str(uid))
    states_total_dict = load_obj("total_states_" + str(uid))


"""
    test implementation
"""


def print_results(uid):

    global states_dict
    global edges_dict
    global states_total_dict
    global edges_total_dict

    try:
        if uid == 0:
            print "********* ALL *********"

            testing_data = np.genfromtxt('../ground_truth/gt_all.csv', delimiter=",", dtype=None,
                                         names=["current_path", "prediction"])
        else:
            print "********* User ID:", uid, "*********"
            path_file = "../ground_truth/gt_u" + str(uid) + ".csv"
            testing_data = np.genfromtxt(path_file, delimiter=",", dtype=None,
                                         names=["current_path", "prediction"])

        load_data(uid)

        incorrect_prediction = 0
        correct_prediction = 0

        for row in testing_data:
            domain = row[0].split("/")[0]
            path = row[0]

            prediction = get_prediction(domain, path)
            #print prediction

            if row[1] == prediction:
                correct_prediction += 1
                #print "Correct!!!"
            else:
                incorrect_prediction += 1
                #print "Incorrect :'("
        """
            print "Prediction", prediction
            print "actual path", row[1]
            print "---------------------"
            print ""

        domain = testing_data[0][0].split("/")[0]
        path = testing_data[0][0]

        prediction = get_prediction(domain, path)
        # print prediction

        if testing_data[0][1] == prediction:
            correct_prediction += 1
            # print "Correct!!!"
        else:
            incorrect_prediction += 1
            # print "Incorrect :'("
        print "Prediction", prediction
        print "actual path", testing_data[0][1]
        print "---------------------"
        print ""
        """

        print "Threshold:", DELTA_THRESHOLD
        print incorrect_prediction / (correct_prediction + incorrect_prediction * 1.0) * 100, "% incorrect predictions"
        print correct_prediction / (correct_prediction + incorrect_prediction * 1.0) * 100, "% correct predictions"

    except IOError:
        print "USER DATA NOT FOUND"


for i in range(0, 28):
    print_results(i)
    print ""

#print_results(0)