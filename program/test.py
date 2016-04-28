import glob
import numpy as np
import warnings

def get_file_name(file):
    str = file.rsplit('\\', 1)[1]
    str = str[1:]
    return str.rsplit('_',1)[0]

csv_list = glob.glob('../dataset/*.csv')

data = np.array([[0,0,0]])
warnings.simplefilter("ignore")
for csv_file in csv_list:
    try:
        print get_file_name(csv_file)
        print csv_file
        csv_matrix = np.genfromtxt(csv_file,delimiter=",",usecols=(0,1,2),dtype=None)
        data = np.concatenate([data,csv_matrix])
    except ValueError:
        pass

data = np.delete(data, 0, 0)

#print data