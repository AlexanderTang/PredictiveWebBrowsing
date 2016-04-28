import numpy as np


# loads the transformed data set and returns it as a numpy array
def load():
    return np.genfromtxt('../processed_data/transformed_data.csv', delimiter=",", dtype=None)


# load the transformed data set without 'beforeunload' and 'polling' as a numpy array
def downsized_load():
    dataset = load()
    dataset = dataset[
        np.logical_not(np.logical_or(
            dataset[:, 2] == "beforeunload",
            dataset[:, 2] == "polling"
        ))
    ]
    return dataset
