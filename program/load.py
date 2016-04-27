import numpy as np

def load():
    return np.genfromtxt('transformed_data.csv', delimiter=",", dtype=None)