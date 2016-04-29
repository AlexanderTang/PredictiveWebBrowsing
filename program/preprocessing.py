import load
import operator

threshold = 1000

def count_occurrences():
    dataset = load.load()
    dom_dict = {}
    for row in dataset:
        if row[2] == "load":
            if dom_dict.has_key(row[3]):
                dom_dict[row[3]] = dom_dict[row[3]] + 1
            else:
                dom_dict[row[3]] = 1
    return dom_dict
    #for el in dom_dict:
    #    print el, ' ', dom_dict[el]

def sort_occurrences():
    dict = count_occurrences()
    sorted_x = sorted(dict.items(), key=operator.itemgetter(1))
    for el in sorted_x:
        print el

def get_sessions():
    # In this case I was loading the rows with load actions of the transformed_data file, now load is loading the
    # transformed_data as it is.
    dataset = load.load()

    l = len(dataset)

    for i in range(0,l-1):
        rowTime1 = dataset[i][1]
        rowTime2 = dataset[i+1][1]

        # The following two lines are use to remove the extra colon at the beginning of the some times
        if rowTime1[0] == ":":
            rowTime1 = rowTime1[1:]

        if rowTime2[0] == ":":
            rowTime2 = rowTime2[1:]

        deltaTime = np.datetime64(dataset[i+1][0]+"T"+rowTime2) - np.datetime64(dataset[i][0]+"T"+rowTime1)

        if deltaTime > threshold:
            #dataset[i+1] should be start the new session
        else
            # dataset[i] remains in the session

sort_occurrences()


"""
Prolling referes to call to external source, not made by user, so probably it is not necessary
"""