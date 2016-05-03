import load
import csv
import numpy as np

# threshold for users to become eligible for the ground truth
#   (see define_truth_users() method)
USER_ROWS_THRESHOLD = 30


# generates the ground truth for all users and store it in gt_all.csv
def define_truth_all():
    dataset = load.deep_filtered_load()
    dataset = gen_truth(dataset)

    with open('../ground_truth/gt_all.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in dataset:
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
        dataset = gen_truth(data)
        if len(dataset["uid"]) >= USER_ROWS_THRESHOLD:
            path = "../ground_truth/gt_u" + str(uid) + ".csv"

            with open(path, 'wb') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',')
                for row in dataset:
                    csvwriter.writerow(row)
        uid += 1


# generates and returns the ground truth
def gen_truth(dataset):
    # TO IMPLEMENT

    return dataset

define_truth_users()

