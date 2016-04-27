import load
import operator

def count_occurrences():
    dataset = load.load()
    dom_dict = {}
    for row in dataset:
        if row[2] == "load":
            if dom_dict.has_key(row[3]):
                dom_dict[row[3]] = dom_dict[row[3]] + 1
            else:
                dom_dict[row[3]] = 1
    return dom_dict
    #for el in dom_dict:
    #    print el, ' ', dom_dict[el]

def sort_occurrences():
    dict = count_occurrences()
    sorted_x = sorted(dict.items(), key=operator.itemgetter(1))
    for el in sorted_x:
        print el

sort_occurrences()