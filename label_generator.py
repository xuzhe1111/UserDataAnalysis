#!/usr/bin/env python
# -*- coding:utf8 -*-
#

import math
import random
import sys

def compute_label(doc_list):
    # Use median samples to compute alpha and beta.
    doc_list.sort(key = lambda item:item[2], reverse = True)
    max_imp = max([item[2] for item in doc_list])
    selected_doc_list = []
    for i in range(0, len(doc_list) * 3 / 4):
        if doc_list[i][2] < max(5, max_imp * 0.02):
            continue

        good_ctr = (doc_list[i][3] / doc_list[i][2]) * (math.log(1 + doc_list[i][2]) / 3.9318)
        less_ctr = (doc_list[i][3] + doc_list[i][4]) / doc_list[i][2] * (math.log(1 + doc_list[i][2]) / 3.9318)
        selected_doc_list.append(doc_list[i].extend([good_ctr, less_ctr]))

    if len(selected_doc_list) < 5:
        return

    selected_doc_list.sort(key = lambda item:item[6], reverse = True)
    for doc in selected_doc_list:
        print '\t'.join(['%s' % item for item in doc])


    #imp_sum = sum([item[2] for item in selected_doc_list[2:]])
    #good_clk_sum = sum([item[3] for item in selected_doc_list[2:]])
    #less_clk_sum = sum([item[3] + item[4] for item in selected_doc_list[2:]])
    #if imp_sum < 100:
    #    return

    #ctr_1 = good_clk_sum / imp_sum
    #ctr_2 = less_clk_sum / imp_sum
    #beta = min(max(max_imp * 0.1, 40), 100)
    #alpha_1 = beta * ctr_1
    #alpha_2 = beta * ctr_2

    #doc_label_list = []
    #for item in selected_doc_list:
    #    label_1 = (item[3] + alpha_1) / (item[2] + beta)
    #    label_2 = (item[3] + item[4] + alpha_2) / (item[2] + beta)
    #    item.extend([label_1, label_2])
    #    doc_label_list.append(item)

    #doc_label_list.sort(key = lambda item:item[6], reverse = True)
    #if len(doc_label_list) > 20:
    #    step = len(doc_label_list) / 20.0
    #    for i in range(20):
    #        pos = int(i * step)
    #        print '\t'.join(['%s' % item for item in doc_label_list[pos]])
    #else:
    #    for doc_item in doc_label_list:
    #        print '\t'.join(['%s' % item for item in doc_item])

def run():
    pre_query = None
    doc_list = []
    for line in sys.stdin:
        fields = line.rstrip('\n').split('\001')
        if len(fields) < 6:
            continue

        query = fields[0]
        doc_id = fields[1]
        try:
            impression_count = float(fields[2])
            good_click_count = float(fields[3])
            less_click_count = float(fields[4])
            bad_click_count = float(fields[5])
        except:
            continue

        if pre_query is None:
            pre_query = query

        if query == pre_query:
            doc_list.append([query, doc_id, impression_count, good_click_count, less_click_count, bad_click_count])
        else:
            compute_label(doc_list)
            doc_list = []
            pre_query = query
            doc_list.append([query, doc_id, impression_count, good_click_count, less_click_count, bad_click_count])

    compute_label(doc_list)

if __name__ == '__main__':
    run()
