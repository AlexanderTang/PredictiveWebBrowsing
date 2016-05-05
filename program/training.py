from sklearn.cross_validation import train_test_split
import glob
import numpy as np
import csv





    if user_id == 0:
        raw_data = np.genfromtxt('../ground_truth/gt_all.csv', delimiter=",", dtype=None,
                                names=["ts", "action", "dom", "path", "uid"])
    else:
        file_path = "../ground_truth/gt_u" + str(user_id) + ".csv"
        raw_data = np.genfromtxt(file_path, delimiter=",", dtype=None,
                                names=["ts", "action", "dom", "path", "uid"])

    training_data, testing_data = train_test_split(raw_data, test_size=TRAINING_DATA_PERCENTAGE)

    traning_path = "../training_data/training_" + str(user_id) + ".csv"
    testing_path = "../testing_data/testing_" + str(user_id) + ".csv"

    with open(traning_path, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in training_data:
            csvwriter.writerow(row)

    with open(testing_path, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in testing_data:
            csvwriter.writerow(row)

    return training_data
