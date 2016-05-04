import load
import csv
import numpy as np
import operator

# threshold for users to become eligible for the ground truth
#   (see define_truth_users() method)
USER_ROWS_THRESHOLD = 30


# generates the ground truth for all users and store it in gt_all.csv
def define_truth_all():
    dataset = load.deep_filtered_load()
    truth_list = gen_truth(dataset)

    with open('../ground_truth/gt_all.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in truth_list:
            csvwriter.writerow(row)


# generates the ground truth for each user and store it
# in separate .csv files; users with less than 30 rows are
# not processed due to too small sample size
def define_truth_users():
    dataset = load.deep_filtered_load()
    # split the dataset into submatrices by user ID
    split_dataset = np.split(dataset,
            np.where( np.diff(dataset["uid"]) )[0] + 1
        )

    uid = 1
    for data in split_dataset:
        if len(data["uid"]) >= USER_ROWS_THRESHOLD:
            truth_list = gen_truth(data)
            path = "../ground_truth/gt_u" + str(uid) + ".csv"

            with open(path, 'wb') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',')
                for row in truth_list:
                    csvwriter.writerow(row)
        uid += 1


# generates and returns the ground truth
def gen_truth(dataset):
    truth_list = []
    while len(dataset) > 0:
        (dataset, gen_list) = gen_truth_domain(dataset,dataset["dom"][0])
        truth_list.extend(gen_list)
    return truth_list


# generate ground truth for domain
def gen_truth_domain(dataset, dom):
    """
    assign a weight per section in the path; if a deeper path is equal to the previous subpath in count,
            prefer to deep path (that's what we look for); in fact, if deep path is >= to subpath in 80%
            of the cases or more, then prefer deep path
    """
    truth_list = []
    dom_list = dataset[np.in1d(dataset["dom"], dom)]
    dataset = dataset[np.logical_not(np.in1d(dataset["dom"], dom))]

    # count the occurrence of each (sub)path
    path_dict = {}
    for row in dom_list:
        path = row["path"]
        path = path.split('/')
        if path[0] == "":  # remove empty string at the beginning
            del path[0]
        if path[len(path)-1] == "":  # remove empty string at the end
            del path[len(path)-1]

        depth = 1
        current_path = dom
        for p in path:
            current_path += "/" + p
            if path_dict.has_key((current_path,depth)):
                path_dict[(current_path,depth)] += 1
            else:
                path_dict[(current_path,depth)] = 1
            depth += 1

    # REMOVE THIS LATER
    #sorted_dict = sorted(path_dict.items(), key=operator.itemgetter(1))
    #print sorted_dict

    truth_list.append((dom, search_truth(dom, path_dict)))
    for key in path_dict:
        truth = search_truth(key[0], path_dict)
        if truth != key[0]:
            truth_list.append((key[0], truth))

    # return the downsized dataset and the list of truths respectively
    return dataset, truth_list


# returns the truth for the given path
#   cp stands for 'current path'
def search_truth(cp, path_dict):
    truth = cp
    depth = 0
    count = 0
    for key, value in path_dict.items():
        # check if it's the same substring (path)
        if key[0][:len(cp)] == cp:
            if is_better_prediction(key[1],value,depth,count):
                truth = key[0]
                depth = key[1]
                count = value
    return truth


# Returns true if 1 gives a better prediction than 2,
# based on depth and score comparison
def is_better_prediction(d1,c1,d2,c2):
    """
    We don't want deep paths with very few occurrences relative to
        to the subpath to overshadow the rest, so depth must play
        a role in computing the score.
    We also prefer to find as deep a path as possible, within reasonable
        count levels, so the count of deeper paths will have a higher
        weight.

    This will be the algorithm that we use:
    ( The algorithm was invented based on feeling and observing the data.
            It can definitely be improved. )
    - If the difference in count is 2 or less, use the deeper path,
        regardless of the difference in depth levels.
      Reasoning: For very small count levels, both the subpath and
        the end path don't provide much info, so we might as well provide
        the user with an end path he's visited before. If the count is
        high, then the deep path is basically always preferrable.
    - For a count difference > 2, if the deeper path has a count of
        1/5 of that of the subpath or less, then choose the shorter
        path. Due to the way our counts work, it's very natural for sub
        paths to have a (much) higher count than the end paths, but we
        are generally more interested in the end paths themselves unless
        the end paths are very sparse. In that case, it might be more
        interesting to go for a shorter path with a much higher accuracy.
      * For every extra depth difference between the shorter and longer path,
        we add a difference of 4%. So starting from a difference of 6 depth
        levels, the longer path will always be chosen. Such long URLs are not
        only rare, but the shorter path would be a meaningless prediction.
    """
    if d1 == d2:
        if c1 > c2:
            return True
    elif abs(c1-c2) < 3:
        if d1 > d2:
            return True
    else:
        depth_diff = abs(d1-d2) - 1
        if depth_diff > 5:
            depth_diff = 5
        if d1 > d2:
            if c1 > c2 * ((20-4*depth_diff)/100):
                return True
        else:
            if c2 <= c1 * ((20 - 4 * depth_diff) / 100):
                return True
    return False


define_truth_users()
#define_truth_all()
