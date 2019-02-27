#!/usr/bin/env python
#-*- coding:utf8 -*-
#

import sys

def run():
    comprision = []
    pre_query = None
    container = []
    for line in sys.stdin:
        fields = line.rstrip('\n').split('|')
        if len(fields) != 3:
            continue

        query = fields[0]
        try:
            test_score = int(fields[1])
            bkt_score = int(fields[2])
        except:
            continue

        if pre_query is None:
            pre_query = query

        if pre_query == query:
            container.append((test_score, bkt_score))
        else:
            container_result = parse_container(pre_query, container)
            if container_result is not None:
                comprision.append(container_result)

            pre_query = query
            container = []
            container.append((test_score, bkt_score))

    container_result = parse_container(pre_query, container)
    if container_result is not None:
        comprision.append(container_result)

    print len(comprision)
    print "test wins", sum([item[1] for item in comprision])
    print "bkt wins", sum([item[2] for item in comprision])
    print "equal times", sum([item[3] for item in comprision])

def parse_container(query, container):
    if len(container) < 3:
        return None

    test_count = 0
    bkt_count = 0
    #test_count = sum([item[0] for item in container])
    #bkt_count = sum([item[1] for item in container])
    for item in container:
        if item[0] > item[1]:
            test_count += 1
        elif item[0] < item[1]:
            bkt_count += 1
        else:
            pass

    if test_count >= 3:
        print "test:", query
        return [query, 1, 0, 0]
    elif bkt_count >= 3:
        print "bkt:", query
        return [query, 0, 1, 0]
    else:
        return [query, 0, 0, 1]
    #if test_count > bkt_count:
    #    print "test", query
    #    print container
    #    return [query, 1, 0, 0]
    #elif test_count < bkt_count:
    #    print "bkt", query, test_count, bkt_count
    #    print container
    #    return [query, 0, 1, 0]
    #else:
    #    return [query, 0, 0, 1]

if __name__ == "__main__":
    run()
