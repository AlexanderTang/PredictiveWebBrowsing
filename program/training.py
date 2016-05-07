import sklearn.cross_validation as cross_val
import glob
import numpy as np
import csv


# splits the data into training and test data, based on training percentages;
# the way the data is split happens randomly (the data gets shuffled first)
def set_training_testing_data():
    click_matrix = np.genfromtxt('../processed_data/clicks.csv', delimiter=",",
                                 dtype=None, names=["url", "uid"])
    csv_list = glob.glob('../ground_truth/*.csv')
    for truth_file in csv_list:
        truth_matrix = np.genfromtxt(truth_file, delimiter=",", dtype=None,
                                   names=["key", "result"])

        file_name = truth_file.rsplit('\\', 1)[1]  # get filename
        file_name = file_name[3:]

        if truth_file[-7:] == "all.csv":
            identifier = 0
        else:
            identifier = truth_file.rsplit(".",1)[0]
            identifier = identifier.rsplit("_u",1)[1]
            identifier = int(identifier)
        csv_matrix = assign_solutions(click_matrix, truth_matrix, identifier)

        write_split_data(0.5, "50_50", file_name, csv_matrix)
        write_split_data(0.6, "60_40", file_name, csv_matrix)
        write_split_data(0.7, "70_30", file_name, csv_matrix)
        write_split_data(0.8, "80_20", file_name, csv_matrix)

        write_kfold_data(3, "3fold", file_name, csv_matrix)
        write_kfold_data(4, "4fold", file_name, csv_matrix)
        write_kfold_data(5, "5fold", file_name, csv_matrix)


# assign solutions to clicks
def assign_solutions(click_matrix, truth_matrix, identifier):
    if identifier != 0:
        new_click_matrix = click_matrix[np.in1d(
            click_matrix["uid"], identifier)]
    else:
        new_click_matrix = click_matrix
    arr = []
    for row in new_click_matrix:
        arr.append((find_solution(truth_matrix, row[0])))
    return arr


# returns the key, value for a click
def find_solution(truth_matrix, click):
    for key in truth_matrix:
        if key[0] == click:
            return click, key[1]
    return click, click  # no solution found: return itself


# writing away data to .csv files for training parameters for split
# with shuffling
def write_split_data(training_parameter, sub_folder, file_name, csv_matrix):
    training_data, testing_data = \
        cross_val.train_test_split(csv_matrix, train_size=training_parameter)

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


# writing away data to .csv files for training parameters for kfold
def write_kfold_data(training_parameter, sub_folder, file_name, csv_matrix):
    kf = cross_val.KFold(len(csv_matrix), n_folds=training_parameter,
                         shuffle=True)

    iteration = 1
    for train_index, test_index in kf:
        training_path = "../training_data/" + sub_folder + "/iter" + \
                        str(iteration) + "/" + file_name
        testing_path = "../testing_data/" + sub_folder + "/iter" + \
                       str(iteration) + "/" + file_name

        with open(training_path, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            for i in train_index:
                csvwriter.writerow(csv_matrix[i])
        with open(testing_path, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            for i in test_index:
                csvwriter.writerow(csv_matrix[i])

        iteration += 1


#set_training_testing_data()
