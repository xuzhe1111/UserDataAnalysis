import lightgbm as lgb
import pandas as pd
import numpy as np

try:
    import matplotlib.pyplot as plt
except ImportError:
    raise ImportError('You need to install matplotlib for plot_example.py.')

# load or create your dataset
print('Load data...')
df_train = pd.read_csv('rank.train', header=None, sep='\t')
df_test = pd.read_csv('rank.test', header=None, sep='\t')

y_train = df_train[0].values
y_test = df_test[0].values
#X_train = df_train.drop(0, axis=1).values
#X_test = df_test.drop(0, axis=1).values
X_train = df_train.iloc[:,1:26].values
X_test = df_test.iloc[:,1:26].values
# create dataset for lightgbm


new_X_train = np.zeros((len(X_train), len(X_train[0])), dtype='float')
for i in range(len(X_train)):
    for j in range(len(X_train[0])):
        new_X_train[i][j] = float(X_train[i][j].split(':')[1])
        
new_X_test = np.zeros((len(X_test), len(X_test[0])), dtype='float')
for i in range(len(X_test)):
    for j in range(len(X_test[0])):
        new_X_test[i][j] = float(X_test[i][j].split(':')[1])


lgb_train = lgb.Dataset(new_X_train, y_train)
lgb_test = lgb.Dataset(new_X_test, y_test, reference=lgb_train)

# specify your configurations as a dict
params = {
    'num_leaves': 31,
    'metric': ('binary_error'),
    'num_trees':100,
    'verbose': 0
}

evals_result = {}  # to record eval results for plotting
print('load success')

print('Start training...')
# train
gbm = lgb.train(params,
                lgb_train,
                num_boost_round=100,
                valid_sets=[lgb_train, lgb_test],
                feature_name=['f' + str(i + 1) for i in range(25)],
                #categorical_feature=[21],
                evals_result=evals_result,
                verbose_eval=10)

print('Plot metrics during training...')
ax = lgb.plot_metric(evals_result, metric='binary_error')
plt.show()

print('Plot feature importances...')
ax = lgb.plot_importance(gbm, max_num_features=10)
plt.show()

print('Plot 84th tree...')  # one tree use categorical feature to split
ax = lgb.plot_tree(gbm, tree_index=83, figsize=(20, 8), show_info=['split_gain'])
plt.show()

print('Plot 84th tree with graphviz...')
graph = lgb.create_tree_digraph(gbm, tree_index=83, name='Tree84')
graph.render(view=True)
