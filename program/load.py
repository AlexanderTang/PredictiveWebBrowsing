import numpy as np
import csv

# The timeout in hours for a load to follow a click
LOAD_TIMEOUT = 1


# loads the transformed data set and returns it as a numpy array
def load():
    return np.genfromtxt('../processed_data/transformed_data.csv', delimiter=",", dtype=None,
                         names=["ts", "action", "dom", "path", "uid"])


# load the transformed data set without 'beforeunload' and 'polling' as a numpy array
# loaded urls which are not useful are also filtered; such urls would be:
#   - ads, which get loaded several times such as 'tap2-cdn.rubiconproject.com'
#   - widgets, such as twitter and facebook (hln.be in particular loads a lot of ads and external links)
def filtered_load():
    return np.genfromtxt('../processed_data/filtered_data.csv', delimiter=",", dtype=None,
                         names=["ts", "action", "dom", "path", "uid"])


# filter the data and write to filtered_data.csv
def filter_data():
    dataset = load()
    dataset = dataset[
        np.logical_not(np.logical_or(
            dataset["action"] == "beforeunload",
            dataset["action"] == "polling"
        ))
    ]

    dataset.sort(order=["uid", "ts"])  # order by user id, then by timestamp
    dataset = filter_junk(dataset)

    with open('../processed_data/filtered_data.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in dataset:
            csvwriter.writerow(row)


# filter useless loads and clicks
def filter_junk(dataset):
    """
    Strategy:
        1) remove all loads until a click is found
        2) remove all loads that don't have the same domain as the click until another click is found
        2a) if a click does not have any following loads with the same domain, remove the click
        3) any loads that timeout beyond the threshold after the click are
           removed regardless of the domain
    """
    rows_to_filter = []
    click_index = 0

    # search for click row, remove any rows before that
    while click_index < len(dataset):
        if dataset[click_index][1] == "click":
            break
        else:
            rows_to_filter.append(click_index)
            click_index = click_index + 1

    row_index = click_index + 1
    relevant_loads = 0
    while row_index < len(dataset):
        if dataset[row_index][1] == "load":
            td = np.datetime64(dataset[row_index][0]) - \
                 np.datetime64(dataset[click_index][0])
            if td > np.timedelta64(LOAD_TIMEOUT, 'h') or \
                            dataset[row_index][2] != dataset[click_index][2]:
                rows_to_filter.append(row_index)
            else:
                relevant_loads = relevant_loads + 1
        elif dataset[row_index][1] == "click":  # elif instead of else to be safe
            if relevant_loads == 0:
                rows_to_filter.append(click_index)
            relevant_loads = 0
            click_index = row_index
        row_index = row_index + 1

    if relevant_loads == 0:  # in case the last click doesn't have any relevant loads
        rows_to_filter.append(click_index)

    dataset = np.delete(dataset, rows_to_filter, 0)
    return dataset


filter_data()
#data = filtered_load()
#data = filter_junk(data)
