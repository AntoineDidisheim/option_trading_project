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
df = data.opt

##################
# drop otm options
##################
df['K'] = (100 * df['strike'] / df['S']).round(1)
ind = (df['K'] <= 120) & (df['K'] >= 80)
df = df.loc[ind, :]
# keep otm only
ind = ((df['K'] >= 100) & (df['cp'] == 'C')) | ((df['K'] <= 100) & (df['cp'] == 'P'))
df = df.loc[ind, :]

##################
# summary stats
##################

(df['ret'] <= 1.0).mean()
(df['ret'] <= 0.0).mean()


def plt_percentile(t, title=None, y_label=r'$\log{R}$', label=None):
    t = t.quantile(np.arange(0, 1.01, 0.01))
    plt.plot(t, label=label)
    plt.yscale('log')
    plt.xlabel('Percentile')
    plt.ylabel(y_label)
    plt.grid(True)
    if title is not None:
        plt.title(title)
    plt.tight_layout()


plt_percentile(df['ret'], label='All options')
plt_percentile(df.loc[df['cp'] == 'C', 'ret'], label='Call-options')
plt_percentile(df.loc[df['cp'] == 'P', 'ret'], label='Put-options')

plt.legend()
plt.show()


def plt_ts_perc_score(t, r=1.0, title=None, label=None):
    t = t.groupby('date').apply(lambda x: stats.percentileofscore(x['ret'], r))
    t = t.rolling(20).mean()
    t.plot(label=label)
    plt.ylabel(fr'% of options with $R \geq {r}$')
    plt.xlabel('Date')
    if title is not None:
        plt.title(title)
    plt.grid(True)


plt_ts_perc_score(df, label='All options')
plt_ts_perc_score(df.loc[df['cp'] == 'C', :], label='Call-options')
plt_ts_perc_score(df.loc[df['cp'] == 'P', :], label='Put-options')
plt.legend()
plt.show()

plt_ts_perc_score(df, label='All options', r=0.0)
plt_ts_perc_score(df.loc[df['cp'] == 'C', :], label='Call-options', r=0.0)
plt_ts_perc_score(df.loc[df['cp'] == 'P', :], label='Put-options', r=0.0)
plt.legend()
plt.show()


##################
# looking a bit more firm by firm
##################

def plt_cs_perc_score(t, r=1.0, title=None, label=None):
    t = t.groupby('ticker').apply(lambda x: stats.percentileofscore(x['ret'], r))
    t = t.sort_values()
    t.plot(label=label)
    plt.ylabel(fr'% of options with $R \geq {r}$ in firm i')
    plt.xlabel('Firm')
    if title is not None:
        plt.title(title)
    plt.grid(True)


plt_cs_perc_score(df, title='All options', r=0.0)
plt.show()
plt_cs_perc_score(df.loc[df['cp'] == 'C', :], title='Call-options', r=0.0)
plt.show()
plt_cs_perc_score(df.loc[df['cp'] == 'P', :], title='Put-options', r=0.0)
plt.show()

plt_cs_perc_score(df, title='All options', r=1.0)
plt.show()
plt_cs_perc_score(df.loc[df['cp'] == 'C', :], title='Call-options', r=1.0)
plt.show()
plt_cs_perc_score(df.loc[df['cp'] == 'P', :], title='Put-options', r=1.0)
plt.show()


def plt_cs_av_ret(t, r=1.0, title=None, label=None):
    t = t.groupby('ticker')['ret'].mean()
    t = t.sort_values()
    t.plot(label=label)
    plt.ylabel(fr'% of options with $R \geq {r}$ in firm i')
    plt.xlabel('Firm')
    plt.hlines(1.0, 0, len(t), colors='red', alpha=0.5)
    if title is not None:
        plt.title(title)
    plt.grid(True)


plt_cs_av_ret(df, title='All options')
plt.show()
plt_cs_av_ret(df.loc[df['cp'] == 'C', :], title='Call-options')
plt.show()
plt_cs_av_ret(df.loc[df['cp'] == 'P', :], title='Put-options')
plt.show()


##################
# Distribution across strike
##################


def plt_strike_perc_score(t, r=1.0, title=None, label=None):
    t = t.groupby('K').apply(lambda x: stats.percentileofscore(x['ret'], r))
    t.plot(label=label)
    plt.ylabel(fr'mean % of options with $R \geq {r}$ for strike')
    plt.xlabel('Strike')
    if title is not None:
        plt.title(title)
    plt.grid(True)


plt_strike_perc_score(df.loc[df['cp'] == 'C', :], label='Call-options', r=0.0)
plt_strike_perc_score(df.loc[df['cp'] == 'P', :], label='Put-options', r=0.0)
plt.legend()
plt.show()

plt_strike_perc_score(df.loc[df['cp'] == 'C', :], label='Call-options', r=1.0)
plt_strike_perc_score(df.loc[df['cp'] == 'P', :], label='Put-options', r=1.0)
plt.legend()
plt.show()


def plt_strike_mean(t, title=None, label=None):
    t = t.groupby('K')['ret'].mean()
    t.plot(label=label)
    plt.ylabel(fr'Mean average R')
    plt.xlabel('Strike')

    plt.hlines(1.0, t.index.min(), t.index.max(), colors='red', alpha=0.5)
    if title is not None:
        plt.title(title)
    plt.grid(True)


plt_strike_mean(df.loc[df['cp'] == 'C', :], label='Call-options')
plt_strike_mean(df.loc[df['cp'] == 'P', :], label='Put-options')
plt.legend()
plt.show()


def plt_strike_quantile(t, q, title=None, label=None):
    t = t.groupby('K')['ret'].quantile(q)
    t.plot(label=label)
    plt.ylabel(fr'Percentile of R, {q * 100}')
    plt.xlabel('Strike')

    plt.hlines(1.0, t.index.min(), t.index.max(), colors='red', alpha=0.5)
    if title is not None:
        plt.title(title)
    plt.grid(True)


q = 0.99
plt_strike_quantile(df.loc[df['cp'] == 'C', :], label='Call-options', q=q)
plt_strike_quantile(df.loc[df['cp'] == 'P', :], label='Put-options', q=q)
plt.legend()
plt.show()
