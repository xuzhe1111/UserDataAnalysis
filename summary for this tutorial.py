# -*- coding: utf-8 -*-
import pandas as pd
pd.set_option('html', False)
pd.set_option('max_columns', 30)
pd.set_option('max_rows', 20)

import numpy as np


# 0.Preparation works
baseball = pd.read_csv("baseball.csv", index_col='id')
player_unique = baseball.player + baseball.team + baseball.year.astype(str)
baseball_newind = baseball.copy()
baseball_newind.index = player_unique


# 1.Set up a series
# 1)
counts = pd.Series([632, 1638, 569, 115])

# 2)
bacteria = pd.Series([632, 1638, 569, 115], 
    index=['Firmicutes', 'Proteobacteria', 'Actinobacteria', 'Bacteroidetes'])

# 3)
bacteria_dict = {'Firmicutes': 632, 'Proteobacteria': 1638, 'Actinobacteria': 569, 'Bacteroidetes': 115}

bacteria = pd.Series(bacteria_dict)

bacteria2 = pd.Series(bacteria_dict, index=['Cyanobacteria','Firmicutes','Proteobacteria','Actinobacteria'])


# 2.Import data

# 1)CSV
pd.read_csv("microbiome.csv",header=None,index_col=['Taxon','Patient'],skiprows=[3,4,6],nrows=4,chunksize=15,na_values=['?', -99999])  
baseball = pd.read_csv("baseball.csv", index_col='id')

# 2)Excel
pd.read_excel('microbiome/MID2.xls', sheetname='Sheet 1', header=None)   

# 3)Binary
pd.read_pickle("baseball_pickle")


# 3.Set up a DataFrame
# 1)
data = pd.DataFrame({'value':[632, 1638, 569, 115, 433, 1130, 754, 555],
                     'patient':[1, 1, 1, 1, 2, 2, 2, 2],
                     'phylum':['Firmicutes', 'Proteobacteria', 'Actinobacteria', 
    'Bacteroidetes', 'Firmicutes', 'Proteobacteria', 'Actinobacteria', 'Bacteroidetes']})

# 2)
data2 = pd.DataFrame({0: {'patient': 1, 'phylum': 'Firmicutes', 'value': 632},
                    1: {'patient': 1, 'phylum': 'Proteobacteria', 'value': 1638},
                    2: {'patient': 1, 'phylum': 'Actinobacteria', 'value': 569},
                    3: {'patient': 1, 'phylum': 'Bacteroidetes', 'value': 115},
                    4: {'patient': 2, 'phylum': 'Firmicutes', 'value': 433},
                    5: {'patient': 2, 'phylum': 'Proteobacteria', 'value': 1130},
                    6: {'patient': 2, 'phylum': 'Actinobacteria', 'value': 754},
                    7: {'patient': 2, 'phylum': 'Bacteroidetes', 'value': 555}})

    
# 4.Access columns in DataFrame

# 1) by dict-like indexing
data['value']
data[['phylum','value','patient']]

# 2) by attribute
data.value


# 5.Access rows in DataFrame
    
# 1)
baseball.iloc[0]

# 2)
baseball.loc[88641]
baseball_newind.loc['womacto01CHN2006']

# 3)
baseball[0:10]
baseball_newind[2:15]

# 4)
baseball_newind[baseball_newind.ab>500]

# 5)
baseball_newind.ix['gonzalu01ARI2006', ['h','X2b', 'X3b', 'hr']]
baseball_newind.ix[['gonzalu01ARI2006','finlest01SFN2006'], 5:8]
baseball_newind.ix[:'myersmi01NYA2006', 'hr']

baseball_newind.ix['gonzalu01ARI2006']
baseball_newind.ix[['gonzalu01ARI2006','finlest01SFN2006']]

#baseball_newind.ix[['h','X2b', 'X3b', 'hr']] ----不能只extract columns

# 6)
baseball_newind.xs('gonzalu01ARI2006')
#baseball_newind.xs(['gonzalu01ARI2006','finlest01SFN2006']) ----只能extract a SINGLE row;不能extract more than ONE row

baseball_newind.xs('h',axis=1)
baseball_newind.xs(['h','hr'],axis=1)


# 6.Add or Delete columns & Rows in DataFrame
baseball.shape

# 1)Add columns
data['year'] = 2013

treatment = pd.Series([0]*4 + [1]*2)
data['treatment'] = treatment

#month = ['Jan', 'Feb', 'Mar', 'Apr']
#data['month'] = month
data['month'] = ['Jan']*len(data)

# 2)Delete columns
del data['month']
baseball.drop(['ibb','hbp'], axis=1)

# 3)Delete rows
baseball.drop([89525, 89526])


# 7.Operations

hr2006 = baseball[baseball.year==2006].xs('hr', axis=1)
hr2006.index = baseball.player[baseball.year==2006]
hr2007 = baseball[baseball.year==2007].xs('hr', axis=1)
hr2007.index = baseball.player[baseball.year==2007]

# 1）
hr2006 * 2
hr2006 ** 2

# 2)
hr_total = hr2006 + hr2007
hr2007.add(hr2006, fill_value=0)

# 3)
stats = baseball[['h','X2b', 'X3b', 'hr']]
diff = stats - stats.ix[89521]
diff2 = stats - [1,2,3,4]
#diff3 = stats - [1,2,3]

# 4)
stats.apply(np.median)

stat_range = lambda x: x.max() - x.min()
stats.apply(stat_range)

  
# 8.Sorting and Ranking

# 1)Sorting
baseball_newind.sort_index(ascending=False)

baseball_newind.sort_index(axis=1)

baseball.hr.order(ascending=False)

baseball[['player','sb','cs']].sort_index(ascending=[False,True], by=['sb', 'cs'])   
    
# 2)Ranking

baseball.hr.rank()
baseball.hr.rank(method='first')

baseball.rank(ascending=False).head(10)
baseball[['r','h','hr']].rank(ascending=False).head()


# 9.Hierarchical Index

mb = pd.read_csv("microbiome.csv", index_col=['Taxon','Patient']) # Preparation work

baseball_h = baseball.set_index(['year', 'team', 'player'])

baseball_h.ix[(2007, 'ATL', 'francju01')]
mb.ix['Proteobacteria']

frame = pd.DataFrame(np.arange(12).reshape(( 4, 3)), 
                  index =[['a', 'a', 'b', 'b'], [1, 2, 1, 2]], 
                  columns =[['Ohio', 'Ohio', 'Colorado'], ['Green', 'Red', 'Green']])
frame.index.names = ['key1', 'key2']
frame.columns.names = ['state', 'color']
frame.ix['a']['Ohio']
frame.ix['b', 2]['Colorado']

mb.swaplevel('Patient', 'Taxon').head()

mb.sortlevel('Patient', ascending=False).head()


# 10.Missing Data

bacteria2.dropna()
data.dropna(how='all')

bacteria2[bacteria2.notnull()]

data.ix[7, 'year'] = nan
data.dropna(thresh=4)

data.dropna(axis=1)

bacteria2.fillna(0)
data.fillna({'year': 2013, 'treatment':2})
data.year.fillna(2013, inplace=True)

bacteria2.fillna(method='bfill')
bacteria2.fillna(bacteria2.mean())


# 11.Data summarization

baseball.sum()
baseball.mean()
bacteria2.mean(skipna=False)

extra_bases = baseball[['X2b','X3b','hr']].sum(axis=1)

baseball.describe()
baseball.player.describe()

baseball.hr.cov(baseball.X2b)
baseball.hr.corr(baseball.X2b)
baseball.corr()

mb.sum(level='Taxon')


# 12.Writing data to files

mb.to_csv("mb.csv", sep='', na_rep='', index='', header='')

baseball.to_pickle("baseball_pickle")



