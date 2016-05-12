import transform_data
import preprocessing as pre
import numpy as np
import setup_data
import training
import csv
import transform_data_to_graph as to_graph
import sys


def main(argv=None):
    if argv is not None:
        get_cleaned_training_files(argv)


# does filtering, pruning and generates the truth and returns the result;
# a lot of IO operations happen since we wish to keep a log of sorts in
#       between; this causes some delay when training the data. Data may
#       be directly passed between methods when this delay becomes too big
def get_cleaned_training_files(datasets):
    transform_data.run(datasets, '../actual_run_data/transformed_data.csv')
    pre.filter_data(np.genfromtxt('../actual_run_data/transformed_data.csv',
                                delimiter=",", dtype=None,
                                names=["ts", "action", "dom", "path", "uid"]),
                    '../actual_run_data/filtered_data.csv',
                    '../actual_run_data/clicks.csv'
                    )
    setup_data.define_truth_all(
        np.genfromtxt(
                '../actual_run_data/filtered_data.csv',
                delimiter=",", dtype=None,
                names=["ts", "action", "dom", "path", "uid"]),
        '../actual_run_data/ground_truth.csv'
    )
    training_data = training.assign_solutions(
        np.genfromtxt('../actual_run_data/clicks.csv', delimiter=",",
                      dtype=None, names=["url", "uid"]),
        np.genfromtxt('../actual_run_data/ground_truth.csv', delimiter=",",
                      dtype=None),
        0
    )
    with open('../actual_run_data/training_data.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in training_data:
            csvwriter.writerow(row)

    to_graph.learn_model('../actual_run_data/training_data.csv')

    print len(training_data)

if __name__ == "__main__":
    main(sys.argv)
