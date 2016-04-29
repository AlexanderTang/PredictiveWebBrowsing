import numpy as np


# loads the transformed data set and returns it as a numpy array
def load():
    return np.genfromtxt('../processed_data/transformed_data.csv', delimiter=",", dtype=str)


# load the transformed data set without 'beforeunload' and 'polling' as a numpy array
# loaded urls which are considered spam ads are also filtered
#   (urls are ads when they load the same page within 10 milliseconds of each other)
def downsized_load():
    dataset = load()
    dataset = dataset[
        np.logical_not(np.logical_or(
            dataset[:, 2] == "beforeunload",
            dataset[:, 2] == "polling"
        ))
    ]
    dataset = filter_ads(dataset)
    return dataset


def filter_ads(dataset):



a = downsized_load()
for el in a:
    print el
