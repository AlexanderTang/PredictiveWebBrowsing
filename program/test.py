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

#count_occurrences()

def get_file_name(file):
    str = file.rsplit('\\', 1)[1]
    str = str[1:]
    return str.rsplit('_',1)[0]

def numpywheretest():
    str1 = np.array(["test", "yes"])
    str2 = "abc"
    str3 = "something"
    str4 = "yes"

    a = np.where(str1 == str4) and np.where(str1 == str2)
    print a


def testdict():
    dict = {}
    dict["yes"] = 5
    dict["no"] = 2
    print dict
    for key,v in dict.items():
        print key, ' + ', v

testdict()


"""

def print_all_results():

    for uid in range(0, 28):

        try:

            for testing_data_percentage in TESTING_DATA_PERCENTAGE:

                if uid == 0:
                    testing_url = "../testing_data/" + testing_data_percentage + "/all.csv"
                else:
                    testing_url = "../testing_data/" + testing_data_percentage + "/u" + str(uid) +".csv"

                testing_data = np.genfromtxt(testing_url, delimiter=",", dtype=None, names=["current_path", "prediction"])

                incorrect_prediction = 0
                correct_prediction = 0

                load_graph(uid)

                for row in testing_data:
                    domain = row[0].split("/")[0]
                    path = row[0]

                    prediction = get_prediction(domain, path, confident_interval)

                    if row[1] == prediction:
                        correct_prediction += 1
                    else:
                        incorrect_prediction += 1

                print correct_prediction / (correct_prediction + incorrect_prediction * 1.0) * 100

        except IOError:
            test = ""

#print_results(0)


teams_list = ["Man Utd", "Man City", "T Hotspur"]
data = np.array([[1, 2, 1],
                 [0, 1, 0],
                 [2, 4, 2]])

row_format ="{:>15}" * (len(teams_list) + 1)

print row_format.format("", *teams_list)

for team, row in zip(teams_list, data):
    print row_format.format(team, *row)
"""
