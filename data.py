import numpy as np
import pandas as pd
from parameters import *
import os
import didipack as didi

class Data:
    def __init__(self, par : Params):
        self.par = par
        self.opt = None
        if not os.path.exists(self.par.data.dir+'merge'):
            os.makedirs(self.par.data.dir+'merge')

    def load_all(self, reload = False):
        self.opt = self.load_opt(reload)

    def opt_clean_year(self, year):
        df = pd.read_pickle(self.par.data.dir+f'raw/opt_{year}.p')

        ##################
        # rename columns and format dates
        ##################

        df.columns= [x.lower() for x in df.columns]
        df['date'] = pd.to_datetime(df['date'])
        df['expiration'] = pd.to_datetime(df['expiration'])
        del df['gv_key'], df['total_volume'], df['total_open_interest'],df['dw']

        df = df.rename(columns={'s_close':'S', 'adjustment_factor_2':'adj','shares_outstanding':'share',
                                'implied_volatility':'iv','best_offer':'ask','best_bid':'bid','call_put':'cp',
                                'option_id':'id','t':'T'})
        ##################
        # remove 0 open interest
        ##################

        ind=df['open_interest']>0
        df = df.loc[ind,:]

        ##################
        # fix strike
        ##################

        df['strike'] /= 1000

        return df

    def load_opt(self, reload =False):
        if reload:
            df = None
            for y in range(self.par.data.start_year,self.par.data.end_year+1):
                print('start year', y)
                t = self.opt_clean_year(y)
                if df is None:
                    df = t
                else:
                    df = df.append(t)
            df.to_pickle(self.par.data.dir+f'merge/opt.p')
        else:
            df = pd.read_pickle(self.par.data.dir + f'merge/opt.p')
        return df


# par = Params()
# self = Data(par)
# year = 2000

