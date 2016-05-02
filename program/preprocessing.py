import load
import operator
import numpy as np
import csv

"""
Notes: watch pitfalls:
- if there is no load after a click, the override the click domain: don't accidentally take the load of another (following) click!
- remove the ads and widgets between clicks (load with different domains)
- remove clicks without deeper paths (such as google.com)
- remove clicks after having generated the paths
"""

# The timeout in hours for a load to follow a click
LOAD_TIMEOUT = 1


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


# generates the ground truth for:
#  - all users and stores it in ground_truth_all.csv
#  - each user and stores it in ground_truth_user.csv
def define_truths():
    data = load.filtered_load()


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

    with open('../processed_data/filtered_data.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in dataset:
            csvwriter.writerow(row)


# filter useless loads and clicks:
#  - loads that follow a click but have a different domain
#  - loads after a click that timeout before the next click
#    (this implies a new session)
#  - clicks without any following loads of the same domain are regarded as useless clicks
def filter_junk(dataset):
    """
    Strategy:
        1) initially remove all loads until a click is found
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


# run this when the clicks are no longer necessary in the dataset
def filter_clicks(dataset):
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


#filter_data()
