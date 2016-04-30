import numpy as np
import csv

AD_THRESHOLD = 15   # loads within this threshold (in ms) count as advertisements

# loads the transformed data set and returns it as a numpy array
def load():
    return np.genfromtxt('../processed_data/transformed_data.csv', delimiter=",", dtype=None, names=["ts","action","dom","path","uid"])


# load the transformed data set without 'beforeunload' and 'polling' as a numpy array
# loaded urls which are not useful are also filtered; such urls would be:
#   - ads, which get loaded several times such as 'tap2-cdn.rubiconproject.com'
#   - widgets, such as twitter and facebook (hln.be in particular loads a lot of ads and external links)
def downsized_load():
    dataset = load()
    dataset = dataset[
        np.logical_not(np.logical_or(
            dataset["action"] == "beforeunload",
            dataset["action"] == "polling"
        ))
    ]
    dataset.sort(order=["uid", "ts"])
    #dataset = filter_junk(dataset)
    return dataset


def filter_junk(dataset):
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


def filter_data():
    data = downsized_load()
    with open('../processed_data/filtered_data.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in data:
            csvwriter.writerow(row)
    filter_junk(data)


filter_data()
