import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import didipack as didi
import os
from parameters import *
from data import Data


##################
# define parameters
##################
par = Params()

##################
# load the data
##################
data = Data(par)
data.load_all(reload=False)

##################
# summary stats
##################
data.opt.head()

data.opt['stock_key'] = data.opt['stock_key'].astype(int)
data.opt.head()
i = 10000
date = data.opt.iloc[i,:].loc['expiration']
id = data.opt.iloc[i,:].loc['stock_key']
ind=(data.prc.loc[:,'stock_key']==id) & (data.prc.loc[:,'date']==date )
ind.sum()

t=data.prc[['date','stock_key','S0']].sort_values(['stock_key','date']).reset_index(drop=True)
t['S_T']=t.groupby('stock_key')['S0'].shift(20)

df=data.opt.merge(t[['date','stock_key','S_T']])

ind = df['cp']=='C'
df.loc[ind,'cash']=df.loc[ind,'S_T']- df.loc[ind,'strike']
ind = df['cp']=='P'
df.loc[ind,'cash']=df.loc[ind,'strike']-df.loc[ind,'S_T']
df.loc[(df['cash']<0),'cash'] = 0

df['ret']=df['cash']/df['ask']
(df['ret']<=1.0).mean()

df.loc[(df['ret']>=1.0),'ret'].mean()
df.loc[:,'ret'].mean()


