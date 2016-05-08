import pickle as pk


def save_obj(method, parameter, obj, name):
    if method == "naive":
        file_url = "../graphs/" + parameter + "/" + name + ".pkl"
    else:
        file_url = "../graphs/" + method + "/" + parameter + "/" + name + ".pkl"

    with open(file_url, 'wb') as f:
        pk.dump(obj, f, pk.HIGHEST_PROTOCOL)


def load_obj(method, parameter, name):

    if method == "naive":
        file_url = "../graphs/" + parameter + "/" + name + ".pkl"
    else:
        file_url = "../graphs/" + method + "/" + parameter + "/" + name + ".pkl"

    with open(file_url) as f:
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


def save_graph(method, parameter, user_id, states, edges, states_total, edges_total):

    save_obj(method, parameter, edges, "edges_" + str(user_id))
    save_obj(method, parameter, states, "states_" + str(user_id))
    save_obj(method, parameter, states_total, "total_states_" + str(user_id))
    save_obj(method, parameter, edges_total, "total_edges_" + str(user_id))


def load_graph(method, parameter, uid):

    edges = load_obj(method, parameter, "edges_" + str(uid))
    states = load_obj(method, parameter, "states_" + str(uid))
    edges_total = load_obj(method, parameter, "total_edges_" + str(uid))
    states_total = load_obj(method, parameter, "total_states_" + str(uid))

    return states, edges, states_total, edges_total
