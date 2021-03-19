import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import didipack as didi
import os
from parameters import *
from data import Data
from scipy import stats

##################
# define parameters
##################
par = Params()

##################
# load the data
##################
data = Data(par)
data.load_all(reload=False)
df = data.opt.copy()

##################
# drop otm options
##################
df['K'] = (100*df['strike']/df['S']).round(1)
ind = (df['K']<=120) & (df['K']>=80)
df = df.loc[ind,:]
# keep otm only
ind = ((df['K']>=100) & (df['cp']=='C')) |  ((df['K']<=100) & (df['cp']=='P'))
df = df.loc[ind,:]

##################
# compute momentum
##################
pr = data.prc.copy()
# keep only friday prices
pr = pr.loc[pr['date'].dt.dayofweek==4,:]
# keep only date in the option dataframe
pr = pr.loc[pr['date']>=df['date'].min(),:]

pr = data.prc.sort_values(['stock_key','date']).reset_index(drop=True)
pr['ST']=pr.groupby('ticker')['S0'].shift(-1)
pr['adj_t']=pr.groupby('ticker')['adj'].shift(-1)
pr['ret'] = np.log((pr['ST']*pr['adj'])/(pr['S0']*pr['adj']))
pr=pr.dropna()


nb_week  = 3
pr['r_lag']=pr['ret'].rolling(nb_week).sum().shift(1)

Q_max = 10
pr = pr.loc[pr['date']>=df['date'].min(),:]
pr['q']=pr.groupby('date')['r_lag'].transform(lambda x: pd.qcut(x, Q_max, np.arange(0, Q_max, 1), duplicates='drop'))
pr = pr.dropna()
pr.groupby('q')['ret'].mean().plot()
plt.show()
