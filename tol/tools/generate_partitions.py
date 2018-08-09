import json
import csv
import sys
import random

import itertools


def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    return next(itertools.islice(iterable, n, None), default)

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def generate_partition(distance=3, nro_partitions=3, num_path_max=1):
    trials_to_use = []
    with open('clean_board_distance.csv', 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        csv_reader.next()
        for row in csv_reader:
            # print row
            src, dst, num_path, dist = row
            if int(dist)==distance and int(num_path)<=num_path_max:
                trials_to_use. append((int(src),int(dst),int(dist)))

    random.shuffle(trials_to_use)
    print len(trials_to_use)

    l =  dict(enumerate(chunks(trials_to_use, nro_partitions)))
    l =  list(chunks(trials_to_use, nro_partitions))

    return l

def generate_dump():
    parts = {3:5, 4:6, 5:6, 6: 6}

    all_trials = {}

    for k,v in parts.iteritems():
        all_trials[k] = generate_partition(k,v)

    return all_trials


def save_chuncks(trials, filename):
    with open(filename, 'w') as outfile:
        json.dump(trials, outfile, indent=2)

def load_chuncks(filename):
    json_data=open(filename)
    return json.load(json_data)



def get_trials_to_id(id_user, trials):
    res = {}
    res['trials'] = {}
    res['trials']["1"] = [17, 28, "true", 1]
    res['trials']["2"] = [ 5, 27, "true", 2]
    res['trials']["3"] = [ 0, 15, "true", 1]
    res['trials']["4"] = [14, 34, "true", 2]
    res['trials']["5"] = [25, 35, "false", 1]
    res['trials']["6"] = [10, 29, "false", 2]

    trial_count = 7
    for k in sorted(trials.keys()):
        idx = id_user % len(trials[k])
        print k ,"-> block", idx
        q = trials[k][idx]
        random.shuffle(q)
        for v in q:
            res['trials'][str(trial_count)] = [v[0], v[1], "false", v[2]]
            trial_count += 1
    return res



if __name__ == "__main__":
    pass