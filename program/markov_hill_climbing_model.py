import numpy as np
import graph_utilities as gu

TRAINING_DATA_PERCENTAGE = "80_20"   #"60_40", "70_30", "80_20"]
CONFIDENT_INTERVAL = .20            #.10, .15, .20

states_dict = {}                    # States and the number of times the user transverses them
edges_dict = {}                     # Edges and the number of times the user transverses them
states_total_dict = {}              # Total amount that the user transversed the states by domain
edges_total_dict = {}               # Total amount that the user transversed the edges by domain


def hill_climbing_search(domain, visited):
    last_url = ""
    while len(visited) > 0:
        outgoing = visited.pop(0)
        last_url = outgoing[1]

        if outgoing[1] in edges_dict[domain]:
            temp = []
            for ingoing in edges_dict[domain][outgoing[1]]:

                current_state_probability = states_dict[domain][outgoing[1]] / (states_total_dict[domain] * 1.0)
                next_state_probability = states_dict[domain][ingoing] / (states_total_dict[domain] * 1.0)
                delta = current_state_probability - next_state_probability

                if delta < CONFIDENT_INTERVAL:
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


def get_prediction(domain, path):
    prediction = path
    if domain in states_dict:
        visited = [(1, path)]
        prediction = hill_climbing_search(domain, visited)
    return prediction


def incremental_learning(domain, path):

    length_path = len(path)
    current_path = path[0]

    gu.increase_vertex(states_total_dict, states_dict, domain, current_path)

    for j in range(1, length_path):
        gu.increase_edge(edges_total_dict, edges_dict, domain, current_path, current_path + "/" + path[j])
        gu.increase_vertex(states_total_dict, states_dict, domain, current_path + "/" + path[j])
        current_path = current_path + "/" + path[j]


def test_model():

    global states_dict, edges_dict, states_total_dict, edges_total_dict

    states_dict, edges_dict, states_total_dict, edges_total_dict = gu.load_graph(0, TRAINING_DATA_PERCENTAGE)

    file_path = "../testing_data/" + TRAINING_DATA_PERCENTAGE + "/" + "all.csv"
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

        incremental_learning(domain, path)

    print "Correct:", (correct_predictions / (correct_predictions + incorrect_predictions * 1.0)) * 100


test_model()

