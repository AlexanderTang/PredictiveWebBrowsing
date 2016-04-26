import glob
import csv

csv_list =  glob.glob('../dataset/*.csv')

for csv_file in csv_list:
    with open(csv_file, 'rb') as csvfile:
        csv_matrix = csv.reader((x.replace('\0','') for x in csvfile),
                                delimiter=',')
        for row in csv_matrix:
            print row
            if len(row) != 0:
                print 'el:', row[0], row[1]
            # add to numpy array