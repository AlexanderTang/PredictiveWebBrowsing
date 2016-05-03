import numpy as np


# loads the transformed data set and returns it as a numpy array
def load():
    return np.genfromtxt('../processed_data/transformed_data.csv', delimiter=",", dtype=None,
                         names=["ts", "action", "dom", "path", "uid"])


# load the transformed data set without 'beforeunload' and 'polling' as a numpy array
# loaded urls which are not useful are also filtered; such urls would be:
#   - ads, which get loaded several times such as 'tap2-cdn.rubiconproject.com'
#   - widgets, such as twitter and facebook (hln.be in particular loads a lot of ads and external links)
#   - loads before clicks (we are only interested in the loads that follow a click)
def filtered_load():
    return np.genfromtxt('../processed_data/filtered_data.csv', delimiter=",", dtype=None,
                         names=["ts", "action", "dom", "path", "uid"])


def deep_filtered_load():
    return np.genfromtxt('../processed_data/deep_filtered_data.csv', delimiter=",", dtype=None,
                         names=["ts", "action", "dom", "path", "uid"])