# -*- coding: utf-8 -*-
"""
Created on Sat May 27 22:49:41 2017

@author: jorge

THIS MODULE IS CURRENTLY UNDER DEVELOPMENT
"""

from Lib import * 

class Currency():
    def __init__(self, pair, path="", start=None, end=None, fromDoc=False, figsize=(8, 6)):
        if start:
            self.start = start
        else:
            self.start = "26/7/2016"
        if end:
            self.end = end
        else:
            self.end = "26/1/2017"
        if isinstance(pair,tuple):
            self.pair = pair
        #elif isinstance(pair,str):
         #   self.pair = (pair,"USD")
        else:
            raise Exception("Error pair must be a tuple or a string.")
        if fromDoc:
            self.df = pd.read_csv("Generated\Currencies\\" + pair[0]+pair[1] + ".csv", parse_dates=True, index_col=0)
        #try:
        self.df = pypoloniex.TimeSeries().getData(self.pair,86400,self.start,self.end)
        self.data_source = "poloniex"
        print("Data downloaded from Poloniex.")
        #except:
        print("Error downloading from Poloniex.")
        #    try:
        #self.symbol = self.pair[0]+self.pair[1]
        #self.df = data.DataReader(self.symbol,"fred",self.start,self.end)
        #print("Data downloaded from FRED")
        #    except:
        #raise Exception("Error downloading from FRED")
        if len(self.df) == 0:
            raise Exception("DataFrame length is 0.")
        self.fromDoc = fromDoc
        self.filePaths = []
        self.comparedFilePaths = []
        if isinstance(figsize, tuple):
            self.figsize = figsize
        else:
            self.figsize = (8, 6)
        self.path = path

    def get_df(self):
        return self.df


sess = pypoloniex.TimeSeries()

# Parameters
pair = ('BTC', 'LTC')	 # (market, coin)
period = 86400           # candle stick period in seconds
start = '4/2/2014'		 # dd/mm/year
end =  '11/2/2014'       # dd/mm/year

# Get time series data from Poloniex and load into pandas dataframe
sess.getData(pair, period, start, end)

# Show dataframe with parameters
sess.show()
poloniex.Poloniex("")
