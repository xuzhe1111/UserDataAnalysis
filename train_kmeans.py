#!/usr/bin/env python
#-*- coding:Utf-8 -*-


from sklearn.cluster import MiniBatchKMeans
from sklearn.externals import joblib

import numpy as np
import time

def load_uid_embedding(embedding_file):
    data = []
    with open(embedding_file, 'r') as embedding_stream:
        for line in embedding_stream:
            fields = line.rstrip('\n').split('\t')
            if len(fields) != 2:
                continue

            sub_fields = fields[1].split('_')
            if len(sub_fields) != 64:
                continue

            data.append([float(item) for item in sub_fields])

    return np.array(data)

data = load_uid_embedding("user_embedding.part")

mbk = MiniBatchKMeans(init='k-means++', n_clusters=128, batch_size=45,
                      n_init=10, max_no_improvement=10, verbose=0)

t0 = time.time()
mbk.fit(data)
t_mini_batch = time.time() - t0
print t_mini_batch

joblib.dump(mbk,"mbk_128.m")
