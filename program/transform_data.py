import glob
import numpy as np
import warnings
import csv
from urlparse import urlparse

"""
    All the .csv files get loaded and stored in data.  There are currently problems
    with 25.3.csv and 25.5.csv, which cannot be loaded since the files are empty.
    We exclude them from our dataset.
"""


# Run this to load the given datasets and save them to "transformed_data.csv".
# This new csv-file has the date and time separated and the url domain and path separated as well; other
# useless information has been removed.
def run():
    data = get_dataset()
    transform(data)


# Returns the dataset in a numpy matrix
def get_dataset():
    csv_list = glob.glob('../dataset/*.csv')
    data = np.array([[0, 0, 0, 0]])
    warnings.simplefilter("ignore")
    for csv_file in csv_list:
        try:
            csv_matrix = np.genfromtxt(csv_file, delimiter=",", usecols=(0,1,2), dtype=None)
            amount_rows = len(csv_matrix)
            id_col = np.empty(amount_rows)
            id_col.fill(get_id(csv_file))
            csv_matrix = np.c_[csv_matrix, id_col]
            data = np.concatenate([data, csv_matrix])
        except ValueError:
            pass
    data = np.delete(data, 0, 0)
    return data


# extracts the user id from the relative file path
def get_id(file_path):
    str = file_path.rsplit('\\', 1)[1]  # get filename with extension .csv
    str = str[1:]       # remove the 'u' from the string
    return str.rsplit('_', 1)[0]     # remove the underscore and everything to the right


# formats invalid rows into valid ones, split URL into relevant parts
# and write to csv file
def transform(data):
    with open('../processed_data/transformed_data.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in data:
            #(date,time) = parse_time(row[0])
            timestamp = row[0].replace("T:","T")
            (urldomain, urlpath) = parse_url(row[2])
            action = row[1].replace(" ", "")
            csvwriter.writerow([timestamp, action, urldomain, urlpath, row[3]])  # the last element is the user id


# splits timestamp in date and time and returns them
def parse_time(timestamp):
    (date,time) = timestamp.split('T')
    time = time[:-1]
    if time[0] == ":":
        time = time[1:]
    return date,time


# extract the URL domain and path;
# if the URL contains a query, remove the last part of the path
def parse_url(url):
    url = url.replace(" ", "")
    parsed_url = urlparse(url)
    urlpath = parsed_url.path
    if len(parsed_url.query) != 0:
        urlpath = urlpath.rsplit('/', 1)[0]
    return parsed_url.netloc, urlpath


# run()
