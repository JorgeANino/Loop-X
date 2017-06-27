# -*- coding: utf-8 -*-
"""
Created on Sat May 27 22:49:41 2017

@author: Jorge Alberto Niño Cabal
"""
import numpy as np
import pandas as pd
import yahoo_finance
from pandas_datareader import data, wb
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.pyplot import style
import matplotlib.finance as mpf
from matplotlib.figure import Figure
import mpl_finance
from time import strftime, gmtime, time, localtime
from scipy import stats
from random import gauss, seed
from yahoo_finance import Share
from math import exp, sqrt,log
import bs4 as bs
import datetime as dt
import os
import pickle
import requests
from pandas_datareader.data import Options
from pyPdf import PdfFileWriter,PdfFileReader
import fix_yahoo_finance
import gc
import time
import threading
import subprocess
import sys
import multiprocessing as mp
import matplotlib.ticker as ticker
from matplotlib.dates import date2num
import copy_reg
import types
from scipy.stats.mstats import gmean
from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter
import pypoloniex
import poloniex


#style.use("dark_background")

