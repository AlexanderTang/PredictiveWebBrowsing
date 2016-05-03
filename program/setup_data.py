import load
import csv
import numpy as np

# threshold for users to become eligible for the ground truth
#   (see define_truth_users() method)
USER_ROWS_THRESHOLD = 30


# generates the ground truth for all users and store it in gt_all.csv
def define_truth_all():
    dataset = load.deep_filtered_load()
    truth_list = gen_truth(dataset)

    with open('../ground_truth/gt_all.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in truth_list:
            csvwriter.writerow(row)


# generates the ground truth for each user and store it
# in separate .csv files; users with less than 30 rows are
# not processed due to too small sample size
def define_truth_users():
    dataset = load.deep_filtered_load()
    # split the dataset into submatrices by user ID
    split_dataset = np.split(dataset,
            np.where( np.diff(dataset["uid"]) )[0] + 1
        )

    uid = 1
    for data in split_dataset:
        if len(dataset["uid"]) >= USER_ROWS_THRESHOLD:
            truth_list = gen_truth(data)
            path = "../ground_truth/gt_u" + str(uid) + ".csv"

            with open(path, 'wb') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',')
                for row in truth_list:
                    csvwriter.writerow(row)
        uid += 1


# generates and returns the ground truth
def gen_truth(dataset):
    truth_list = []
    while len(dataset) > 0:
        (dataset, gen_list) = gen_truth_domain(dataset,dataset["dom"][0])
        truth_list.extend(gen_list)
    return truth_list


# generate ground truth for domain
def gen_truth_domain(dataset, dom):
    """
    assign a weight per section in the path; if a deeper path is equal to the previous subpath in count,
            prefer to deep path (that's what we look for); in fact, if deep path is >= to subpath in 80%
            of the cases or more, then prefer deep path
    """
    truth_list = []
    dom_list = dataset[np.in1d(dataset["dom"], dom)]
    dataset = dataset[np.logical_not(np.in1d(dataset["dom"], dom))]
    #TODO the count for each (sub)path implementation

    # return the downsized dataset and the list of truths respectively
    return dataset, truth_list


#define_truth_users()
define_truth_all()
