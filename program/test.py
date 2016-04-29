import load
import numpy as np
import glob
import numpy as np
import warnings

def test_method():
    dataset = load.load()
    test = []
    dom_dict = {}
    for row in dataset:
        if row[2] == "load":
            test.append(row)
    return test

thresholder = 1000

def count_occurrences():
    dataset = test_method()
    l = len(dataset)

    for i in range(0,l-1):
        rowTime1 = dataset[i][1]
        rowTime2 = dataset[i+1][1]

        if rowTime1[0] == ":":
            rowTime1 = rowTime1[1:]

        if rowTime2[0] == ":":
            rowTime2 = rowTime2[1:]

        deltaTime = np.datetime64(dataset[i+1][0]+"T"+rowTime2) - np.datetime64(dataset[i][0]+"T"+rowTime1)

        if deltaTime > thresholder:
            print dataset[i]

count_occurrences()

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
