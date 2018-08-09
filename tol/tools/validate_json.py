import json
import csv
import sys




def check(trials):
    trial_def = {}
    with open('clean_board_distance.csv', 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        csv_reader.next()
        for row in csv_reader:
            # print row
            src, dst, _, dist = row
            if trial_def.has_key((int(src),int(dst))):
                print "Error", src, dst, dist
            else:
                trial_def[(int(src),int(dst))] = int(dist)

    vals_to_test = sorted([ (int(k), v) for (k,v) in trials.iteritems()])

    feed_back = 0
    no_feed_back = 0

    for i in range(len(vals_to_test)):
        current = vals_to_test[i]
        if i+1!= current[0]:
            "Bad naming trial", i, current

        src, dst, feed, dist = current[1]
        feed = json.loads(feed)
        if trial_def[(src,dst)] != dist:
            print "Bad distance trial", current[0], "distance should be", trial_def[(src,dst)],
            print "but instead it says:", dist

        feed_back += 1 if feed else 0
        no_feed_back += 1 if not feed else 0

    print "Test ", feed_back + no_feed_back, "trials"
    print "Feedback trials: ", feed_back
    print "No feedback trials: ", no_feed_back


if __name__ == "__main__":
    if len(sys.argv)!=2:
        print "Run with: python validate_json.py source_to_json", len(sys.argv)
    else:
        src = sys.argv[1]

        json_data=open(src).read()
        experiment = json.loads(json_data)

        check(experiment["trials"])