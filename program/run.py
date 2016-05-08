import transform_data
import preprocessing as pre
import numpy as np

def get_cleaned_files(datasets):
    transform_data.run(datasets, '../actual_run_data/transformed_data.csv')
    pre.filter_data(np.genfromtxt('../actual_run_data/transformed_data.csv',
                                delimiter=",", dtype=None,
                                names=["ts", "action", "dom", "path", "uid"]),
                    '../actual_run_data/filtered_data.csv',
                    '../actual_run_data/clicks.csv'
                    )