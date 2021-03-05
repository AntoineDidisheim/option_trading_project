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
df = data.opt

df['K'] = (100*df['strike']/df['S']).round(2)
df = df.loc[df['iv']!=-99.99,:]
df = df.loc[df['iv']>0.0,:]

df = df.loc[(df['K']<=150) & (df['K']>=50),:]

df.groupby('K')['iv'].mean().plot()
plt.show()
df


