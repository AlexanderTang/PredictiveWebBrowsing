import load
import operator

"""
Notes: watch pitfalls:
- if there is no load after a click, the override the click domain: don't accidentally take the load of another (following) click!
- remove the ads and widgets between clicks (load with different domains)
- remove clicks without deeper paths (such as google.com)
- remove clicks after having generated the paths
"""


# counts the occurrences of url domains for every load indicator; it is sorted from infrequent to frequent
def count_occurrences():
    dataset = load.load()
    dom_dict = {}
    for row in dataset:
        if row[1] == "load":
            if dom_dict.has_key(row[2]):
                dom_dict[row[2]] = dom_dict[row[2]] + 1 # increase the count of the word in dictionary by 1
            else:
                dom_dict[row[2]] = 1    # if word not in dictionary, insert with count 1
    sorted_dict = sorted(dom_dict.items(), key=operator.itemgetter(1))
    return sorted_dict
