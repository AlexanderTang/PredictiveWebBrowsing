import load
import operator
import numpy as np
"""
Notes: watch pitfalls:
- if there is no load after a click, the override the click domain: don't accidentally take the load of another (following) click!
- if there are loads within 0.1 seconds of each other, then it's most likely ads. (there are some within 4-6 milliseconds of each other...)
- Polling refers to call to external source, not made by user, so probably it is not necessary???
"""

SESSION_TIMEOUT_THRESHOLD = 1000

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

# get the session of the user
def get_sessions():
    # In this case I was loading the rows with load actions of the transformed_data file, now load is loading the
    # transformed_data as it is.
    dataset = load.downsized_load()

    for i in range(len(dataset)):
        rowTime1 = dataset[i][0]
        rowTime2 = dataset[i+1][0]

        deltaTime = np.datetime64(dataset[i+1][0]+"T"+rowTime2) - np.datetime64(dataset[i][0]+"T"+rowTime1)

        if deltaTime > SESSION_TIMEOUT_THRESHOLD:
            #dataset[i+1] should be start the new session
        else:
            #dataset[i] remains in the session
