import numpy as np

# loads the transformed data set and returns it as a numpy array
def load():
    return np.genfromtxt('../processed_data/transformed_data.csv', delimiter=",", dtype=None)