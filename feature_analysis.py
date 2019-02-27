import sys
import numpy


def main():
    feature_dict = dict()
    for line in sys.stdin:
        line = line.rstrip('\n')
        fields = line.split('#')
        if len(fields) != 2:
            continue

        detail = fields[0]
        detail_field = detail.split('\t')
        for pair in detail_field:
            pair = pair.strip()
            pair_field = pair.split(':')
            if len(pair_field) != 2 or pair_field[0] == "qid":
                continue

            try:
                fid = int(pair_field[0])
                score = float(pair_field[1])
            except:
                continue

            if fid not in feature_dict:
                feature_dict[fid] = []

            feature_dict[fid].append(score)

    # Compute each feature's mean and var.
    for fid, score_list in feature_dict.iteritems():
        narray = numpy.array(score_list)
        sum1 = narray.sum()
        narray2 = narray * narray
        sum2 = narray2.sum()
        N = len(score_list)
        mean = sum1 / N
        var = sum2 / N - mean**2
        print "featureid:", fid, "  mean:", mean, "   var:", var

if __name__ == '__main__':
    main()
