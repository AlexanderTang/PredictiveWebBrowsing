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

def run():
    data = get_dataset()
    transform(data)

# Returns the dataset in a numpy matrix
def get_dataset():
    csv_list = glob.glob('../dataset/*.csv')

    data = np.array([[0,0,0]])
    warnings.simplefilter("ignore")
    for csv_file in csv_list:
        try:
            csv_matrix = np.genfromtxt(csv_file,delimiter=",",usecols=(0,1,2),dtype=None)
            data = np.concatenate([data,csv_matrix])
        except ValueError:
            pass

    data = np.delete(data, 0, 0)
    return data

def transform(data):
    with open('transformed_data.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in data:
            (date,time) = parse_time(row[0])
            (urldomain, urlpath) = parse_url(row[2])
            action = row[1].replace(" ", "")
            csvwriter.writerow([date, time, action, urldomain, urlpath])

def parse_time(timestamp):
    (date,time) = timestamp.split('T')
    time = time[:-1]
    return date,time

def parse_url(url):
    url = url.replace(" ", "")
    parsed_url = urlparse(url)
    urlpath = parsed_url.path
    if len(parsed_url.query) != 0:
        urlpath = urlpath.rsplit('/', 1)[0]
    return parsed_url.netloc, urlpath

run()