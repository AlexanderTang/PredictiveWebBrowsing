import glob
import numpy as np
import warnings

"""
    All the .csv files get loaded and stored in data.  There are currently problems
    with 25.3.csv and 25.5.csv, which cannot be loaded since the files are empty.
    We exclude them from our dataset.
"""

# Returns the dataset in a numpy matrix
def get_dataset():
    csv_list = glob.glob('../dataset/*.csv')

    data = np.array([[0,0,0]])
    warnings.simplefilter("ignore")
    for csv_file in csv_list:
        with open(csv_file, 'rb') as csvfile:
            try:
                csv_matrix = np.genfromtxt(csv_file,delimiter=",",usecols=(0,1,2),dtype=None)
                data = np.concatenate([data,csv_matrix])
            except ValueError:
                pass

    data = np.delete(data, 0, 0)
    return data