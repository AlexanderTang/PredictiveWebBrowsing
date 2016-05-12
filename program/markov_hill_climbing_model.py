#!python2

import numpy as np
import graph_utilities as gu

NAIVE_METHOD = "70_30"   # "50_50", "60_40", "70_30", "80_20"
K_FOLD_METHOD = "5fold"  # "3fold", "4fold", "5fold"
CONFIDENT_INTERVAL = .20 # .10, .15, .20
INCREMENTAL_LEARNING = False

states_dict = {}
edges_dict = {}
states_total_dict = {}
edges_total_dict = {}

class MarkovModel:

    def load_model(self):
        global states_dict, edges_dict, states_total_dict, edges_total_dict

        states_dict, edges_dict, states_total_dict, edges_total_dict = \
            gu.load_graph("", -1, -1)


    def hill_climbing_search(self, domain, visited):
        last_url = ""
        while len(visited) > 0:
            outgoing = visited.pop(0)
            last_url = outgoing[1]

            if domain in edges_dict:
                if outgoing[1] in edges_dict[domain]:
                    temp = []
                    for ingoing in edges_dict[domain][outgoing[1]]:

                        current_state_probability = \
                            states_dict[domain][outgoing[1]] / \
                            (states_total_dict[domain] * 1.0)
                        next_state_probability = \
                            states_dict[domain][ingoing] / \
                            (states_total_dict[domain] * 1.0)
                        delta = current_state_probability - next_state_probability

                        if delta < CONFIDENT_INTERVAL:
                            edge_probability = \
                                edges_dict[domain][outgoing[1]][ingoing] / \
                                (edges_total_dict[domain][outgoing[1]] * -1.0)

                            temp.append((edge_probability, ingoing))

                    if len(temp) > 0:
                        temp = sorted(temp, key=lambda x: x[0])
                        visited = visited + [temp[0]]
                        last_url = temp[0][1]
                else:
                    break
            else:
                break
        return last_url


    def get_prediction(self, domain, path):
        print domain
        print path
        prediction = path
        if domain in states_dict:
            visited = [(1, path)]
            prediction = self.hill_climbing_search(domain, visited)
        return prediction


def incremental_learning(domain, path):

    length_path = len(path)
    current_path = path[0]

    gu.increase_vertex(states_total_dict, states_dict, domain, current_path)

    for j in range(1, length_path):
        gu.increase_edge(edges_total_dict, edges_dict, domain, current_path,
                         current_path + "/" + path[j])
        gu.increase_vertex(states_total_dict, states_dict, domain,
                           current_path + "/" + path[j])
        current_path = current_path + "/" + path[j]

    
def naive_test(uid, with_incremental_learning):
    global states_dict, edges_dict, states_total_dict, edges_total_dict

    if uid == 0:
        file_path = "../testing_data/" + NAIVE_METHOD + "/" + "all.csv"
    else:
        file_path = "../testing_data/" + NAIVE_METHOD + "/u" + \
                    str(uid) + ".csv"

    try:

        states_dict, edges_dict, states_total_dict, edges_total_dict = \
            gu.load_graph("naive", NAIVE_METHOD, uid)

        testing_data = np.genfromtxt(file_path, delimiter=",", dtype=None)

        correct_predictions = 0
        incorrect_predictions = 0

        for testing_datum in testing_data:

            path = filter(lambda x: x != "", testing_datum[1].split("/"))

            domain = path[0]

            prediction = MarkovModel.get_prediction(domain, testing_datum[0])

            if prediction == testing_datum[1]:
                correct_predictions += 1
            else:
                incorrect_predictions += 1

            if with_incremental_learning:
                incremental_learning(domain, path)

        return (correct_predictions / (correct_predictions +
                                       incorrect_predictions * 1.0)) * 100
    except IOError:
        return 0


def k_fold_test(uid, iteration, with_incremental_learning):

    global states_dict, edges_dict, states_total_dict, edges_total_dict

    if uid == 0:
        file_path = "../testing_data/" + K_FOLD_METHOD + "/" + iteration \
                    + "/" + "all.csv"
    else:
        file_path = "../testing_data/" + K_FOLD_METHOD + "/" + iteration \
                    + "/" + "/u" + str(uid) + ".csv"

    try:

        states_dict, edges_dict, states_total_dict, edges_total_dict = \
            gu.load_graph(K_FOLD_METHOD, iteration, uid)

        testing_data = np.genfromtxt(file_path, delimiter=",", dtype=None)

        correct_predictions = 0
        incorrect_predictions = 0

        for testing_datum in testing_data:

            path = filter(lambda x: x != "", testing_datum[1].split("/"))

            domain = path[0]

            prediction = get_prediction(domain, testing_datum[0])

            if prediction == testing_datum[1]:
                correct_predictions += 1
            else:
                incorrect_predictions += 1

            if with_incremental_learning:
                incremental_learning(domain, path)
        return (correct_predictions / (correct_predictions +
                                       incorrect_predictions * 1.0)) * 100
    except IOError:
        return 0


# Get results of naive test
def get_results_naive_test():
    print "Cross validation setup:", NAIVE_METHOD
    print "Confident interval (%):", CONFIDENT_INTERVAL * 100
    print "Incremental learning:", INCREMENTAL_LEARNING
    results_by_user = {}
    for user_id in range(0, 28):
        results_by_user[user_id] = naive_test(user_id, INCREMENTAL_LEARNING)

    for user in results_by_user:
        if results_by_user[user] > 0:
            print "user", user, "-", results_by_user[user]


# Get results of k-fold method
def get_results_k_fold_test():

    number_iterations = 0
    accuracy_sum_users = [0] * 28

    # Results for 3-fold method
    if K_FOLD_METHOD == "3fold":
        number_iterations = 3
        for i in range(1, 4):
            parameter = "iter" + str(i)
            for user_id in range(0, 28):
                accuracy_sum_users[user_id] += \
                    k_fold_test(user_id, parameter, INCREMENTAL_LEARNING)

    # Results for 4-fold method
    if K_FOLD_METHOD == "4fold":
        number_iterations = 4
        for i in range(1, 5):
            parameter = "iter" + str(i)
            for user_id in range(0, 28):
                accuracy_sum_users[user_id] += \
                    k_fold_test(user_id, parameter, INCREMENTAL_LEARNING)

    # Results for 5-fold method
    if K_FOLD_METHOD == "5fold":
        number_iterations = 5
        for i in range(1, 6):
            parameter = "iter" + str(i)
            for user_id in range(0, 28):
                accuracy_sum_users[user_id] += \
                    k_fold_test(user_id, parameter, INCREMENTAL_LEARNING)

    print "K-folder setup:", K_FOLD_METHOD
    print "Confident interval (%):", CONFIDENT_INTERVAL * 100
    print "Incremental learning:", INCREMENTAL_LEARNING
    for sum_accuracy_user in accuracy_sum_users:
        if sum_accuracy_user > 0:
            print "user", accuracy_sum_users.index(sum_accuracy_user), \
                "-", sum_accuracy_user / number_iterations

# get_results_naive_test()
# get_results_k_fold_test()


