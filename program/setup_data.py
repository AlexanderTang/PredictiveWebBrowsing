import load
import csv

# generates the ground truth for all users and store it in gt_all.csv
def define_truth_all():
    dataset = load.deep_filtered_load()
    dataset = gen_truth(dataset)

    with open('../ground_truth/gt_all.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in dataset:
            csvwriter.writerow(row)


# generates the ground truth for each user and store it
# in separate .csv files
def define_truth_users():
    dataset = load.deep_filtered_load()

    # IMPLEMENT: loop over all users and call gen truth; save to different csv file


# generates and returns the ground truth
def gen_truth(dataset):
    # TO IMPLEMENT

    return dataset