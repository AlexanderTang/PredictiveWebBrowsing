import sklearn.cross_validation as cross_val
import glob
import numpy as np
import csv


# splits the data into training and test data, based on training percentages;
# the way the data is split happens randomly (the data gets shuffled first)
def set_training_testing_data():
    csv_list = glob.glob('../ground_truth/*.csv')
    #for csv_file in csv_list:
    if True:
        csv_file = csv_list[0]

        csv_matrix = np.genfromtxt(csv_file, delimiter=",", dtype=None,
                                   names=["key", "result"])
        file_name = csv_file.rsplit('\\', 1)[1]  # get filename with extension .csv
        file_name = file_name[3:]

        write_data(0.5, "50_50", file_name, csv_matrix)
        write_data(0.6, "60_40", file_name, csv_matrix)
        write_data(0.7, "70_30", file_name, csv_matrix)
        write_data(0.8, "80_20", file_name, csv_matrix)

        # TODO first compute the good score using the cross val library, before performing stratified kfold (only one needed)
        write_data(3, "3fold", file_name, csv_matrix)
        write_data(4, "4fold", file_name, csv_matrix)
        #write_data(5, "5fold", file_name, csv_matrix)


# writing away data to .csv files for training parameters
def write_data(training_parameter, sub_folder, file_name, csv_matrix):
    if isinstance(training_parameter, int):
        #csv_matrix = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
        #new_matrix = np.array(csv_matrix)
        #new_matrix.tolist()
        #print new_matrix
        csv_matrix = [list(elem) for elem in csv_matrix]
        print csv_matrix
        a = cross_val.StratifiedKFold(csv_matrix, training_parameter)
        #print a
        for training, test in a:
            print training
            print test
        print ""
        return
    else:
        return
        #training_data, testing_data = cross_val.train_test_split(csv_matrix, train_size=training_parameter)

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


set_training_testing_data()
