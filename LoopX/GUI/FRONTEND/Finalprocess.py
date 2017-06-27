from Lib import *
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 00:28:40 2017

@author: Jorge Alberto Niño Cabal
version: 0.1

THIS MODULE IS CURRENTLY UNDER DEVELOPMENT
"""

class SP500Final():
    def __init__(self,path,start="2000-01-01",end=dt.datetime.now()):
        self.path = path
        self.start = start
        self.end = end
        self.progressp = 0
        print("Running final")
        self.sp500analysis()



    def sp500analysis(self):
        try:
            with open(self.path + "\sp500\sp500tickers.pickle", "rb") as f:
                tickers = pickle.load(f)
        except:
            print("S&P500 data has not been loaded.")
        progress = 0
        Stock.check_if_log_exists(self.path)
        Stock.check_if_progress_exists(self.path)
        startg = time()
        with open(self.path + "\Logs\\" + strftime("%b-%d-%Y_%H%M%S", localtime()) + "__S&P500_log.txt", "a") as f:
            for ticker in tickers:
                 try:
                    f.write(strftime("%b %d %Y %H:%M:%S", localtime()) + "- Starting analysis of: " + ticker + "\n")
                    print("Starting analysis of: " + ticker)
                    self.current_stock = Stock(ticker, self.path, self.start, self.end, figsize=(15, 15))
                    self.analysis()
                    progress += 1
                    f.write(strftime("%b %d %Y %H:%M:%S", localtime()) + "- " + str(
                        progress) + ". " + ticker + " analyzed." + "\n")
                    print(str(progress) + ". " + ticker + " analyzed.")
                    strprogress = str(round(float(progress) * 100 / len(tickers), 2))
                    self.progressp = int(progress * 100 / len(tickers))
                    with open(self.path + "\Progress\Progress.txt","w") as aux:
                        aux.write(str(self.progressp))
                    f.write(strftime("%b-%d-%Y %H:%M:%S", localtime()) + "- " + "Progress: " + strprogress + "%.\n\n")
                    print("Progress: " + strprogress + "%.\n\n")
                    if progress == len(tickers):
                        f.write(strftime("%b %d %Y %H:%M:%S", localtime()) + "- " + "Analysis completed successfully.")
                        print("Analysis completed successfully.")
                        os.remove(self.path+"\Progress\Progress.txt")
                        os.removedirs(self.path+"\Progress\\")
                    del self.current_stock
                 except:
                    f.write(strftime("%b %d %Y %H:%M:%S", localtime()) + "- " + ticker + " not found." + "\n\n")
                    print(ticker + " not found.")
                    progress += 1
            endg = time()
            f.write(
                "\n\n" + strftime("%b-%d-%Y %H:%M:%S", localtime()) + "- Overall time:" + str(endg - startg))
        print(str(endg - startg))

    def analysis(self):
        self.current_stock.full_analysis_no_MC()

if len(sys.argv) == 4:
    app = SP500Final(path=str(sys.argv[1]),start=str(sys.argv[2]),end=str(sys.argv[3]))
elif len(sys.argv) == 3:
    app = SP500Final(path=str(sys.argv[1]), start=str(sys.argv[2]))
elif len(sys.argv) == 2:
    app = SP500Final(path=str(sys.argv[1]))
else:
    app = SP500Final(path=str("C:\\Users\\jorge\\Midas"))