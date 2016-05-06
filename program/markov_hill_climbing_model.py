"""
"""

import pickle as pk

TRAINING_TESTING_DATA_PERCENTAGE = "80_20"   #"60_40", "70_30", "80_20"]
CONFIDENT_INTERVAL = .20            #.10, .15, .20

states_dict = {}                    # States and the number of times the user transverses them
edges_dict = {}                     # Edges and the number of times the user transverses them
states_total_dict = {}              # Total amount that the user transversed the states by domain
edges_total_dict = {}               # Total amount that the user transversed the edges by domain


def load_obj(name):
    with open('../graphs/' + TRAINING_TESTING_DATA_PERCENTAGE + "/" + name + '.pkl', 'rb') as f:
        return pk.load(f)


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


def load_graph(uid):
    global edges_dict
    global states_dict
    global edges_total_dict
    global states_total_dict

    edges_dict = load_obj("edges_" + str(uid))
    states_dict = load_obj("states_" + str(uid))
    edges_total_dict = load_obj("total_edges_" + str(uid))
    states_total_dict = load_obj("total_states_" + str(uid))


def get_prediction(domain, path):
    prediction = path
    if domain in states_dict:
        visited = [(1, path)]
        prediction = hill_climbing_search(domain, visited)
    return prediction
