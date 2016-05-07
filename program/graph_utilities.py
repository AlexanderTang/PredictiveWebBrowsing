import pickle as pk


def save_obj(obj, training_data_percentage, name):
    with open('../graphs/' + training_data_percentage + "/" + name + '.pkl', 'wb') as f:
        pk.dump(obj, f, pk.HIGHEST_PROTOCOL)


def load_obj(training_data_percentage, name):

    with open('../graphs/' + training_data_percentage + "/" + name + '.pkl', 'rb') as f:
        return pk.load(f)


def increase_vertex(states_total, dictionary, domain, vertex):

    if domain in dictionary:
        if vertex in dictionary[domain]:
            dictionary[domain][vertex] += 1
        else:
            dictionary[domain].update({vertex: 1})
        states_total[domain] += 1
    else:
        dictionary[domain] = {vertex: 1}
        states_total[domain] = 1


def increase_edge(edges_total, dictionary, domain, outgoing, ingoing):

    if domain in dictionary:
        if outgoing in dictionary[domain]:
            if ingoing in dictionary[domain][outgoing]:
                dictionary[domain][outgoing][ingoing] += 1
            else:
                dictionary[domain][outgoing].update({ingoing: 1})
                edges_total[domain][outgoing] += 1
        else:
            dictionary[domain].update({outgoing: {ingoing: 1}})
            edges_total[domain].update({outgoing: 1})
    else:
        dictionary[domain] = {outgoing: {ingoing: 1}}
        edges_total[domain] = {outgoing: 1}


def save_graph(user_id, training_data_percentage, states, edges, states_total, edges_total):

    save_obj(edges, training_data_percentage, "edges_" + str(user_id))
    save_obj(states, training_data_percentage, "states_" + str(user_id))
    save_obj(states_total, training_data_percentage, "total_states_" + str(user_id))
    save_obj(edges_total, training_data_percentage, "total_edges_" + str(user_id))


def load_graph(uid, training_data_percentage):

    edges = load_obj(training_data_percentage, "edges_" + str(uid))
    states = load_obj(training_data_percentage, "states_" + str(uid))
    edges_total = load_obj(training_data_percentage, "total_edges_" + str(uid))
    states_total = load_obj(training_data_percentage, "total_states_" + str(uid))

    return states, edges, states_total, edges_total
