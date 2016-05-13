#!python2

import pickle as pk


def save_obj(method, parameter, obj, name):
    if parameter == -1:
        file_url = \
            "../graphs/user/" + name + ".pkl"
    else:
        if method == "naive":
            file_url = \
                "../graphs/" + parameter + "/" + name + ".pkl"
        else:
            file_url = \
                "../graphs/" + method + "/" + parameter + "/" + name + ".pkl"

    with open(file_url, 'wb') as f:
        pk.dump(obj, f, pk.HIGHEST_PROTOCOL)


def load_obj(method, parameter, name):
    if parameter == -1:
        file_url = \
            "../graphs/user/" + name + ".pkl"
    else:
        if method == "naive":
            file_url = \
                "../graphs/" + parameter + "/" + name + ".pkl"
        else:
            file_url = \
                "../graphs/" + method + "/" + parameter + "/" + name + ".pkl"
    with open(file_url, 'rb') as f:
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


def save_graph(method, parameter, user_id, ss, es, sst, est):
    if user_id == -1:
        save_obj(method, user_id, es, "edges")
        save_obj(method, user_id, ss, "states")
        save_obj(method, user_id, est, "total_edges")
        save_obj(method, user_id, sst, "total_states")
    else:
        save_obj(method, parameter, es, "edges_" + str(user_id))
        save_obj(method, parameter, ss, "states_" + str(user_id))
        save_obj(method, parameter, sst, "total_states_" + str(user_id))
        save_obj(method, parameter, est, "total_edges_" + str(user_id))


def load_graph(method, parameter, uid):

    if uid == -1:
        edges = load_obj(method, parameter, "edges")
        states = load_obj(method, parameter, "states")
        edges_total = load_obj(method, parameter, "total_edges")
        states_total = load_obj(method, parameter, "total_states")
    else:
        edges = load_obj(method, parameter, "edges_" + str(uid))
        states = load_obj(method, parameter, "states_" + str(uid))
        edges_total = load_obj(method, parameter, "total_edges_" + str(uid))
        states_total = load_obj(method, parameter, "total_states_" + str(uid))

    return states, edges, states_total, edges_total
