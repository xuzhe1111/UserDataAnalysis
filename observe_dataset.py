import numpy as np
import pandas as pd

import sys

def load_dataset(file_path):
    X_digit = []
    y_digit = []
    docid_digit = []
    with open(file_path, 'r') as file_stream:
        for line in file_stream:
            fields = line.rstrip('\n').split(' ')
            if len(fields) != 3:
                continue

            doc_id = fields[0]
            try:
                label = int(fields[1])
            except:
                continue

            doc_feature = [0] * 79
            for item in fields:
                item_fields = item.split(':')
                if len(item_fields) != 2:
                    continue

                try:
                    f_id = int(item_fields[0])
                    f_value = float(item_fields[1])
                except:
                    continue

                if f_id > 78:
                    continue

                doc_feature[f_id] = f_value

            X_digit.append(doc_feature)
            y_digit.append(label)
            docid_digit.append(label)

        return X_digit

X_digit = load_dataset('final.dat')

doc_np = np.array(X_digit)
df = pd.DataFrame(doc_np)
