from sklearn.cross_validation import train_test_split
import glob
import numpy as np
import csv


def set_training_testing_data():
    csv_list = glob.glob('../ground_truth/*.csv')
    for csv_file in csv_list:
        csv_matrix = np.genfromtxt(csv_file, delimiter=",", dtype=None,
                                   names=["key", "result"])
        file_name = csv_file.rsplit('\\', 1)[1]  # get filename with extension .csv
        file_name = file_name[3:]

        write_training_data(0.5, "50_50", file_name, csv_matrix)
        write_training_data(0.6, "60_40", file_name, csv_matrix)
        write_training_data(0.7, "70_30", file_name, csv_matrix)
        write_training_data(0.8, "80_20", file_name, csv_matrix)


def write_training_data(training_percentage, sub_folder, file_name, csv_matrix):
    training_data, testing_data = train_test_split(csv_matrix, training_size=training_percentage)

    training_path = "../training_data/" + sub_folder + "/" + file_name
    testing_path = "../testing_data/" + sub_folder + "/" + file_name

    with open(training_path, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in training_data:
            csvwriter.writerow(row)

    with open(testing_path, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in testing_data:
            csvwriter.writerow(row)

    return training_data
