#!/usr/bin/env  python
# -*- coding:utf-8 -*-

import random
import sys

def load_word2id(word2id_file):
    word2id_dict = {}
    with open(word2id_file, 'r') as word2id_stream:
        for line in word2id_stream:
            fields = line.rstrip('\n').split('\t')
            if len(fields) != 2:
                continue

            doc_id = fields[0]
            try:
                id_ = int(fields[1])
            except ValueError:
                continue

            word2id_dict[doc_id] = id_

    return word2id_dict

def main():
    word2id = load_word2id('./word2id_800w.txt')
    uid_stream = open('./uid2id.txt', 'w')
    idx = 0
    pre_uid = None
    for line in sys.stdin:
        fields = line.rstrip('\n').split(' ')
        if len(fields) != 2:
            continue

        uid = fields[0]
        global_docid = fields[1]
        if global_docid not in word2id:
            continue

        docid = word2id[global_docid]

        if pre_uid != uid:
            idx += 1
            pre_uid = uid
            uid_stream.write('%s %s\n' % (uid, idx))

        print '%s,%s' % (idx, docid)

    uid_stream.close()

if __name__ == '__main__':
    main()
