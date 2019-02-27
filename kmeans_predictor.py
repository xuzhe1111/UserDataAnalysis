#!/usr/bin/env python
#-*- coding:Utf-8 -*-


from sklearn.cluster import MiniBatchKMeans
from sklearn.externals import joblib

import numpy as np
import time

estimator = joblib.load("mbk_128.m")

def predict(embedding_file):
    data = []
    with open(embedding_file, 'r') as embedding_stream:
        for line in embedding_stream:
            fields = line.rstrip('\n').split('\t')
            if len(fields) != 2:
                continue

            sub_fields = fields[1].split('_')
            if len(sub_fields) != 64:
                continue

            uid_embd = np.array([float(item) for item in sub_fields])
            res=estimator.fit_predict(uid_embd)
            print fields[0]
            print res

predict("user.txt")
