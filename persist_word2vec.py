#!/usr/bin/env  python
# -*- coding:utf-8 -*-

import random
import sys

def load_sample_weight(weight_file):
    sample_weight = {}
    with open(weight_file, 'r') as weight_stream:
        for line in weight_stream:
            fields = line.rstrip('\n').split('\t')
            if len(fields) != 2:
                continue

            doc_id = fields[0]
            try:
                weight = float(fields[1])
            except ValueError:
                continue

            sample_weight[doc_id] = weight

    return sample_weight

def neg_sample():
    return random.randint(1, 110000)

def is_lucky(weight):
    if random.random() < weight:
        return True

    return False

def process_user_log(sample_weight, user_log):
    output = []
    output_doc_id_mark = {}
    user_log.sort(key = lambda item:item[1], reverse=True)
    for item in user_log:
        doc_map_id = item[2]
        doc_id = item[3]
        if doc_id in output_doc_id_mark:
            continue

        if doc_id not in sample_weight:
            continue

        weight = sample_weight[doc_id]
        if not is_lucky(weight):
            continue

        neg_doc_map_id = neg_sample()
        output.append([item[0], doc_map_id, neg_doc_map_id])
        output_doc_id_mark[doc_id] = True

    if len(output) < 20:
        return

    for i in range(min(200, len(output))):
        print "%s\t%s\t%s" % (output[i][0], output[i][1], output[i][2])

def main():
    sample_weight = load_sample_weight('./docid_sample_weight.txt')

    pre_user_map_id = None
    user_log = []
    for line in sys.stdin:
        fields = line.rstrip('\n').split('\t')
        if len(fields) != 4:
            continue

        user_map_id = fields[0]

        if pre_user_map_id is None:
            pre_user_map_id = user_map_id

        if pre_user_map_id == user_map_id:
            user_log.append(fields)
        else:
            process_user_log(sample_weight, user_log)
            user_log = []
            user_log.append(fields)
            pre_user_map_id = user_map_id

    process_user_log(sample_weight, user_log)

if __name__ == '__main__':
    main()
