import numpy as np

AD_THRESHOLD = 15   # loads within this threshold (in ms) count as advertisements

# loads the transformed data set and returns it as a numpy array
def load():
    return np.genfromtxt('../processed_data/transformed_data.csv', delimiter=",", dtype=None, names=["ts","action","dom","path","uid"])


# load the transformed data set without 'beforeunload' and 'polling' as a numpy array
# loaded urls which are considered spam ads are also filtered
#   (urls are ads when they load the same page within 10 milliseconds of each other)
def downsized_load():
    dataset = load()
    dataset = dataset[
        np.logical_not(np.logical_or(
            dataset["action"] == "beforeunload",
            dataset["action"] == "polling"
        ))
    ]
    dataset = filter_ads(dataset)
    return dataset


def filter_ads(dataset):
    dataset.sort(order=["uid","ts"])
    t1 = 0
    i = 1
    while i < len(dataset):
        if dataset[i][1] == "load":
            td = np.datetime64(dataset[i][0]) - np.datetime64(dataset[t1][0])
            if td < np.timedelta64(AD_THRESHOLD, 'ms') and td >= np.timedelta64(0, 'ms'):
                print td
                print dataset[t1]
                print np.datetime64(dataset[t1][0])
                print dataset[i]
                print np.datetime64(dataset[i][0])
                print "ok\n"
            t1 = i
        i = i + 1
    return dataset



a = downsized_load()
"""
for el in a:
    print el
"""