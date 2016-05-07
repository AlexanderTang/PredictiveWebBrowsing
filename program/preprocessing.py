import load
import operator
import numpy as np
import csv

# The timeout in hours for a load to follow a click
LOAD_TIMEOUT = 1


# counts the occurrences of url domains for every load indicator; it is
#   sorted from infrequent to frequent
def count_occurrences():
    dataset = load.load()
    dom_dict = {}
    for row in dataset:
        if row[1] == "load":
            if dom_dict.has_key(row[2]):
                # increase the count of the word in dictionary by 1
                dom_dict[row[2]] += 1
            else:
                # if word not in dictionary, insert with count 1
                dom_dict[row[2]] = 1
    sorted_dict = sorted(dom_dict.items(), key=operator.itemgetter(1))
    return sorted_dict


# filter the data and write to filtered_data.csv
def filter_data():
    dataset = load.load()
    dataset = dataset[
        np.logical_not(np.logical_or(
            dataset["action"] == "beforeunload",
            dataset["action"] == "polling"
        ))
    ]

    dataset.sort(order=["uid", "ts"])  # order by user id, then by timestamp
    dataset = filter_junk(dataset)
    dataset = filter_clicks(dataset)
    dataset = filter_documents(dataset)
    dataset = deep_cleaning_data(dataset)

    with open('../processed_data/filtered_data.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in dataset:
            csvwriter.writerow(row)


# further filter the dataset; filter the following:
#  - loads that don't lead to a deeper path of at least depth 1:
#      we are only interested in the deepest end paths;
#      homepages are meaningless to us
#  - loads with deeper paths, but that occur only once in the entire file:
#      a load that only occurs once has a small confidence interval:
#      the load could be a one-time only path which is meaningless to train on
def deep_cleaning_data(dataset):
    dataset = clean_homepages(dataset)
    dataset = remove_single_occurrences(dataset)
    return dataset


# filter useless loads and clicks:
#  - loads that follow a click but have a different domain
#  - loads after a click that timeout before the next click
#    (this implies a new session)
#  - clicks without any following loads of the same domain are regarded
#       as useless clicks
def filter_junk(dataset):
    """
    Strategy:
        1) initially remove all loads until a click is found
        2) remove all loads that don't have the same domain as the click
            until another click is found
        2a) if a click does not have any following loads with the same domain,
                remove the click
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
            click_index += 1

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
                relevant_loads += 1
        elif dataset[row_index][1] == "click":
            if relevant_loads == 0:
                rows_to_filter.append(click_index)
            relevant_loads = 0
            click_index = row_index
        row_index += 1

    # in case the last click doesn't have any relevant loads
    if relevant_loads == 0:
        rows_to_filter.append(click_index)

    dataset = np.delete(dataset, rows_to_filter, 0)
    return dataset


# run this when the clicks are no longer necessary in the dataset;
# the clicks are saved in a clicks.csv
def filter_clicks(dataset):
    clicks = dataset[dataset["action"] == "click"]
    click_paths = []
    for c in clicks:
        path = c["path"].split('/')
        if len(path) != 0 and path[0] == "":  # remove empty string
            del path[0]
        if len(path) != 0 and path[len(path) - 1] == "":  # remove empty string
            del path[len(path) - 1]
        url = c["dom"]
        for p in path:
            url += "/" + p
        click_paths.append((url, c["uid"]))
    with open('../processed_data/clicks.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in click_paths:
            csvwriter.writerow(row)

    dataset = dataset[np.logical_not(
            dataset["action"] == "click"
    )]
    return dataset


# truncate paths with the top 12 common documents (such as .pdf, .png, .jpg)
def filter_documents(dataset):
    for row in dataset:
        for doc_ext in get_top_docs():
            if row["path"].endswith(doc_ext):
                row["path"] = row["path"].rsplit('/', 1)[0]
                break
    return dataset


# return the top 12 common documents (such as .pdf, .png, .jpg)
# extensions borrowed from:
# duff-johnson.com/2014/02/17/the-8-most-popular-document-formats-on-the-web
def get_top_docs():
    return [".pdf",".xlsx",".xls",".docx",".doc",".ppt",".pptx",
            ".epub",".od",".odx",".txt",".rtf"]


# clean rows with path of depth 0
def clean_homepages(dataset):
    rows_to_filter = []
    row_index = 0
    while row_index < len(dataset):
        # path of depth 0
        if dataset[row_index]["path"] == "" or \
                        dataset[row_index]["path"] == "/":
            rows_to_filter.append(row_index)
        row_index += 1
    dataset = np.delete(dataset, rows_to_filter, 0)
    return dataset


# remove rows with paths of single occurrence (user id is not compared!)
def remove_single_occurrences(dataset):
    rows_to_filter = []
    row_index = 0
    while row_index < len(dataset):
        row = dataset[row_index]
        occurrences = np.where(dataset["dom"] == row["dom"]) and \
                      np.where(dataset["path"] == row["path"])  # and \
                     # np.where(dataset["uid"] == row["uid"])
        if len(occurrences[0]) == 1:
            rows_to_filter.append(occurrences[0])
        row_index += 1
    dataset = np.delete(dataset, rows_to_filter, 0)
    return dataset


filter_data()
