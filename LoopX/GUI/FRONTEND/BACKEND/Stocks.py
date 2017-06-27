# -*- coding: utf-8 -*-
"""
Created on Sat May 27 22:49:41 2017

@author: Jorge Alberto Niño Cabal
"""

from Lib import *



class Stock():
    """
                            CLASS ONLY
    """

    def __init__(self, symbol,path="",start=None, end=None, fromDoc=False, figsize=(8, 6)):
        if start:
            self.start = start
        else:
            self.start = "2000-01-01"
        if end:
            self.end = end
        else:
            self.end = dt.datetime.now()
        if fromDoc:
            self.df = pd.read_csv("Generated\Stocks\stock_dfs\\" + symbol + ".csv", parse_dates=True, index_col=0)
        else:
            try:
                self.df = data.DataReader(symbol, data_source="google", start=self.start, end=self.end)
                if len(self.df) == 0:
                    raise Exception
                self.data_source = "google"
                print("Data downloaded from Google.")
            except:
                print("Error downloading from Google.")
                try:
                    self.df = data.get_data_yahoo(symbol, data_source="yahoo", start=self.start, end=self.end)
                    self.data_source = "yahoo"
                    if len(self.df) == 0:
                        raise Exception
                    print("Data downloaded from Yahoo.")
                except:
                    print("Error downloading from Yahoo.")
                    raise Exception("Symbol not found.")
        self.symbol = symbol
        if self.data_source == "google":
            self.SD = self.df['Close'][-1] * 0.05
        else:
            self.SD = self.df['Adj Close'][-1] * 0.05
        self.fromDoc = fromDoc
        self.filePaths = []
        self.comparedFilePaths=[]
        if isinstance(figsize, tuple):
            self.figsize = figsize
        else:
            self.figsize = (8, 6)
        self.path = path
        self.set_privates()
            
    def __str__(self):
        if isinstance(self.start,type(self.end)):    
            return "Symbol: " + self.symbol + "\nStart: " + self.start.strftime("%Y-%m-%d") + "\nEnd: "+\
            self.end.strftime("%Y-%m-%d") + "\nFigsize: " + self.figsize + "\nSD: " + self.SD\
            + "\n\n" + str(self.df.tail())
        else:
            return "Symbol: " + self.symbol + "\nStart: " + self.start + "\nEnd: "+\
            self.end.strftime("%Y-%m-%d") + "\nFigsize: " + str(self.figsize[0]) + "\nSD: " + str(self.SD)\
            + "\n\n" + str(self.df.tail())
    
    """
                                MISC
    """

    def change_stock_dates(self, start, end):
        self.df = data.DataReader(self.symbol, data_source="google", start=start, end=end)

    def transfer_data_to_csv(self):
        self.check_if_analysis_dir_exists()
        self.df.to_csv(self.get_analysis_file_location() +  ".csv")


    def merge_analysis_files_into_one(self):
        output = PdfFileWriter()
        out = open(self.path + "\\" + self.symbol + "\Analysis\\" \
                   + self.symbol + "_FullAnalysis.pdf","wb")
        l = []
        for fpath in self.filePaths:
            aux = open(fpath, "rb")
            l.append(aux)
            output.addPage(PdfFileReader(aux).getPage(0))
        output.write(out)
        out.close()
        for i in range(len(l)):
            l[i].close()
            os.remove(self.filePaths[i])
        
        
    def merge_comparison_files_into_one(self,Stock1):
        output = PdfFileWriter()
        out = open(
            self.path + "\\" +self.symbol + "\Comparisons\\" \
                    + Stock1.get_symbol() + "\\" +self.symbol + " and " + Stock1.get_symbol()\
                    + "_FullComparison.pdf","wb")
        l = []
        for fpath in self.comparedFilePaths:
            aux = open(fpath, "rb")
            l.append(aux)
            output.addPage(PdfFileReader(aux).getPage(0))
        output.write(out)
        out.close()
        for x in l:
            x.close()
        for fpath in self.comparedFilePaths:
            os.remove(fpath)

    def compare_ret_model(self,Stock1):
        cor = pd.DataFrame({self.symbol: self.df["Close"]})
        cor = cor.join(pd.DataFrame({Stock1.get_symbol(): Stock1.get_df()["Close"]}))
        rets = np.log(cor / cor.shift(1))
        xdat = rets[self.symbol]
        ydat = rets[Stock1.get_symbol()]
        model = pd.ols(y=ydat, x=xdat)
        regression = [model,str(model.beta)]
        return regression

    def compare_ret_correlation(self, Stock1):
        cor = pd.DataFrame({self.symbol: self.df["Close"]})
        cor = cor.join(pd.DataFrame({Stock1.get_symbol(): Stock1.get_df()["Close"]}))
        rets = np.log(cor / cor.shift(1))
        return rets.corr()
    
    def check_if_analysis_dir_exists(self):
        if not os.path.exists(self.path + "\\"  + self.symbol + "\Analysis\\"):
            os.makedirs(self.path + "\\"  + self.symbol + "\Analysis\\")
    
    def check_if_comparison_dir_exists(self,Stock1):
        if not os.path.exists(self.path + "\\"  + self.symbol + "\Comparisons\\" + Stock1.get_symbol() + "\\"):
            os.makedirs(self.path + "\\" + self.symbol + "\Comparisons\\" + Stock1.get_symbol() + "\\")
    
        
    def generate_analysis_result_file(self):
        self.check_if_analysis_dir_exists()
        with open(self.path + "\\" + self.symbol + "\Analysis\\"+ self.symbol+"_Results.txt","w") as f:
            aux = [self.symbol," results.","\nLast close price: ",self.get_current_close_price(),"\nProbability to go up: "\
                   ,str(self.probability_up),"\nProbability to go down: ",str(self.probability_down), "\nExpected value tomorrow: "\
                   ,str(self.expected_value),"\nCAGR= " + str(round(self.mu,4)*100)+"%"\
                   ,"\nAnnual Volatility= ", str(round(self.vol,4)*100)+"%","\nStatus: "]
            if self.df["Regime"][-1]==1:
                aux.append("Buy.")
            elif self.df["Regime"][-1] == 0:
                aux.append("Wait.")
            else:
                aux.append("Sell.")
            try:
                aux.append("\nExpected value tomorrow N Simulations: " + str(self.expected_value2))
                aux.append("\n5th Percentile: " + str(self.fifthquantile))
                aux.append("\n95th Percentile: " + str(self.ninetyfifthquantile))
            except:
                print("Hist Plot N Monte Carlo Simulations have not been run yet.")
            for i in aux:
                f.write(str(i))
                
    def generate_comparison_result_file(self,Stock1):
        self.check_if_comparison_dir_exists(Stock1)
        with open(self.path + "\\" + self.symbol + "\Comparisons\\"+Stock1.get_symbol()\
                  + "\\"+Stock1.get_symbol()+"_ComparisonResults.txt","w") as f:
            aux = ["Results of: ",self.symbol," comparison with: ",Stock1.get_symbol(),"\n",self.compare_ret_model(Stock1)[0]\
                   ,"\n\n",self.compare_ret_model(Stock1)[1],"\n\n",self.compare_ret_correlation(Stock1)]
            for i in aux:
                f.write(str(i))
                
    
    def look_for_correlated_stocks_sp500(self):
        try:
            with open(self.path + "\sp500\sp500tickers.pickle","rb") as f:
                tickers = pickle.load(f)
        except:
            print("S&P500 data has not been loaded.")
        start = dt.datetime(2000,1,1)
        end = dt.datetime.now()
        progress=0
        for ticker in tickers:
            if ticker == self.symbol:
                pass
            else:
                try:
                    s = Stock(ticker, start, end, figsize=(15, 15))
                    print("Starting comparison of: " + self.symbol + " with " \
                          + s.get_symbol()  + "\n\n")
                    self.compare_with(s,stype)
                    del self.comparedFilePaths
                    self.comparedFilePaths=[]
                    del s
                    progress +=1
                    print(ticker + " compared.\n")
                    strprogress = str(round(float(progress) * 100 / len(tickers),2))
                    print("Progress: " + strprogress + "%\n\n")
                    if progress==len(tickers):
                        print("Comparisons completed successfully.")
                except:
                    progress+=1
                    print(ticker + " not found.")
                    
    
    def full_analysis(self, I=10000, T=252, MA1=42, MA2=252):
        self.set_privates(MA1,MA2)
        self.save_close_chart_to_pdf()
        self.save_mcs_hist_to_pdf(I)
        self.save_n_mcs_chart_to_pdf(I,T)
        self.save_n_mcs_hist_daily_returns(I,T)
        self.save_market_return_and_strategy_chart_to_pdf()
        self.save_log_return_chart_to_pdf()
        self.save_volatility_chart_to_pdf()
        self.save_ma_regime_strategy_marketr_charts_to_pdf(MA1, MA2)
        self.save_market_return_chart_to_pdf()
        self.save_strategy_chart_to_pdf()
        self.save_multiple_mas_charts_to_pdf(MA1, MA2)
        self.save_close_boxplot_to_pdf()
        self.save_multiple_mas_boxplots_to_pdf(MA1,MA2)
        #self.__set_Adj_Close()
        self.transfer_data_to_csv()
        self.generate_analysis_result_file()
        self.merge_analysis_files_into_one()
        
    def full_analysis_no_MC(self,MA1=42,MA2=252):
        self.set_privates()
        self.save_close_chart_to_pdf()
        self.save_market_return_and_strategy_chart_to_pdf()
        self.save_log_return_chart_to_pdf()
        self.save_volatility_chart_to_pdf()
        self.save_ma_regime_strategy_marketr_charts_to_pdf(MA1, MA2)
        self.save_market_return_chart_to_pdf()
        self.save_strategy_chart_to_pdf()
        self.save_multiple_mas_charts_to_pdf(MA1, MA2)
        self.save_close_boxplot_to_pdf()
        self.save_multiple_mas_boxplots_to_pdf(MA1,MA2)
        #self.__set_Adj_Close()
        self.transfer_data_to_csv()
        self.generate_analysis_result_file()
        self.merge_analysis_files_into_one()
    
    def compare_with(self,Stock1):
        self.save_close_between(Stock1)
        self.save_regression_between(Stock1)
        self.save_rets_between(Stock1)
        self.save_rolling_corr_between(Stock1)
        
        self.merge_comparison_files_into_one(Stock1)
        self.generate_comparison_result_file(Stock1)
        
        
    """
                                PLOTTERS
    """
    def boxplot_close(self):
        fig, ax= plt.subplots(figsize=self.figsize)
        quotes = zip(date2num(self.df.index.to_pydatetime()),self.df["Open"],self.df["Close"],self.df["High"],self.df["Low"])
        mpl_finance.candlestick_ochl(ax,quotes,width=0.6,colorup="b",colordown="r")
        ax.xaxis_date()
        plt.grid(True)
        plt.xlabel("Date",fontsize=self.figsize[0])
        plt.ylabel("Price",fontsize=self.figsize[0])
        plt.title(self.symbol + " Close Price",fontsize=self.figsize[0])
        plt.setp(plt.gca().get_xticklabels(), rotation=30)
        return fig
    
    def plot_close(self):
        fig = plt.figure(figsize=self.figsize)
        plt.plot(self.df["Close"],label="Close",color='r')
        plt.legend(loc=0)
        plt.grid(True)
        plt.xlabel("Date",fontsize=self.figsize[0])
        plt.ylabel("Price",fontsize=self.figsize[0])
        plt.title(self.symbol + " Close Price",fontsize=self.figsize[0])
        return fig

    def plot_volatility(self):
        try:
            fig = plt.figure(figsize=self.figsize)
            plt.plot(self.df["Volatility"],color='b',label="Volatility")
            plt.legend(loc=0)
            plt.grid(True)
            plt.xlabel("Date",fontsize=self.figsize[0])
            plt.ylabel("% Rate",fontsize=self.figsize[0])
            plt.title(self.symbol + " Volatility",fontsize=self.figsize[0])
            return fig
        except:
            plt.close()
            print("Volatility has not been set in the Data Frame.")
            print("\nPlease use *object*.__set_volatility_and_log_return()")

    def plot_log_return(self):
        try:
            fig = plt.figure(figsize=self.figsize)
            plt.plot(self.df["Log_Ret"],color="b",label="Log Return")
            plt.legend(loc=0)
            plt.grid(True)
            plt.xlabel("Date",fontsize=self.figsize[0])
            plt.ylabel("% Rate",fontsize=self.figsize[0])
            plt.title(self.symbol + " Log Return",fontsize=self.figsize[0])
            return fig
        except:
            plt.close()
            print("Log Return has not been set in the Data Frame.")
            print("\nPlease use *object*.__set_volatility_and_log_return()")

    def plot_monte_carlo_simulation(self, I=10000):
        pdr = self.df["Log_Ret"][1:]
        z = np.random.standard_normal(I)
        ndp = self.df['Close'][-1] * np.exp((np.average(pdr) - ((np.var(pdr) / 2)) + (np.std(pdr) * z)))
        up = float(len(ndp[np.where(ndp >= self.df["Close"][-1])]))*100/I
        down = 100.0-up
        self.probability_up = up
        self.probability_down = down
        self.expected_value = np.average(ndp)
        fig = plt.figure(figsize=self.figsize)
        plt.hist(ndp, bins=50)
        plt.grid(True)
        plt.xlabel("Stock Price",fontsize=self.figsize[0])
        plt.ylabel("Frequency",fontsize=self.figsize[0])
        plt.title(self.symbol+ " Monte Carlo Simulation",fontsize=self.figsize[0])
        return fig
    
    def plot_n_mcs_chart_to_pdf(self,I=10000,T=252):
        self.check_if_analysis_dir_exists()
        S = self.df["Close"][-1]
        fig = plt.figure(figsize=self.figsize)
        for _ in range(I):
            daily_returns=np.random.normal(self.mu/T,self.vol/sqrt(T),T)+1
            price_list=[S]
            for x in daily_returns:
                price_list.append(price_list[-1]*x)
            plt.plot(price_list)
        plt.grid(True)
        plt.xlabel("Days",fontsize=self.figsize[0])
        plt.ylabel("Stock Price",fontsize=self.figsize[0])
        plt.title(self.symbol+" "+str(I)+" Monte Carlo Simulations",fontsize=self.figsize[0])
        return fig
        
    def plot_n_mcs_hist_daily_returns(self,I=10000,T=252):
        S = self.df["Close"][-1]
        result = []
        for _ in range(I):
            daily_returns=np.random.normal(self.mu/T,self.vol/sqrt(T),T)+1
            price_list=[S]
            for x in daily_returns:
                price_list.append(price_list[-1]*x)
            result.append(price_list[-1])
        self.expected_value2 = round(np.mean(result),2)
        self.fifthquantile = np.percentile(result,5)
        self.ninetyfifthquantile = np.percentile(result,95)
        fig = plt.figure(figsize=self.figsize)
        plt.hist(result, bins=100)
        plt.grid(True)
        plt.axvline(np.percentile(result,5), color='r', linestyle='dashed', linewidth=2)
        plt.axvline(np.percentile(result,95), color='r', linestyle='dashed', linewidth=2)
        plt.xlabel("Stock Price",fontsize=self.figsize[0])
        plt.ylabel("Days",fontsize=self.figsize[0])
        plt.title(self.symbol+" " +str(I)+" Monte Carlo Simulations",fontsize=self.figsize[0])
        return fig

    def plot_single_ma(self, window):
        try:
            fig = plt.figure(figsize=self.figsize)
            plt.plot(self.df[str(window)],color='b',label=str(window) + " MA")
            plt.legend(loc=0)
            plt.grid(True)
            plt.title(self.symbol + str(window) + " MA",fontsize=self.figsize[0])
            plt.xlabel("Price",fontsize=self.figsize[0])
            plt.ylabel("Date",fontsize=self.figsize[0])
            return fig
        except:
            plt.close()
            print(str(window) + " has not been set in the Data Frame.")
            print("\nPlease use *object*.__set_single_moving_average(*window_value*)")

    def plot_multiple_ma_regime_strategy_mr(self, window1, window2):
        """
        Buy signal:
            When the 42d trend is for the first time SD points above the 252d trend.
        Wait signal:
            When the 42d trend is within a range of +/- SD points around the 252d trend.
        Sell signal:
            When the 42d trend is for the first time SD points below the 252d trend
        """
        try:
            fig=plt.figure(figsize=self.figsize)
            plt.subplot(221)
            plt.plot(self.df["Close"],label="Close",color="r")
            plt.plot(self.df[str(window1)],label=str(window1) + " MA",color="b")
            plt.grid(True)
            plt.legend(loc=0)
            plt.ylabel("Price")
            plt.title(str(window1) + " days MA")
            plt.subplot(222)
            plt.plot(self.df["Close"],label="Close",color="r")
            plt.plot(self.df[str(window2)],label=str(window2) + " MA",color="b")
            plt.grid(True)
            plt.legend(loc=0)
            plt.ylabel("Price")
            plt.title(str(window2) + " days MA")
            plt.subplot(223)
            plt.plot(self.df["Regime"],color="b")
            plt.grid(True)
            plt.legend(loc=0)
            plt.xlabel("Date")
            plt.ylabel("Rate")
            plt.title("Regime")
            plt.subplot(224)
            plt.plot(self.df["Strategy"].cumsum().apply(np.exp),label="Strategy",color="b")
            plt.plot(self.df["Log_Ret"].cumsum().apply(np.exp),label="Market",color="r")
            plt.grid(True)
            plt.legend(loc=0)
            plt.xlabel("Date")
            plt.ylabel("% Return")
            plt.title("Strategy and Market Return")
            return fig
        except:
            plt.close()
            print(str(window1) + " and/or " + str(window2) + " has not been set.")
            print("\nPlease use *variable*.set_moving_average_regime_between(*window1*,*window2*,*SD*)")

    def plot_market_return(self):
        try:
            fig = plt.figure(figsize=self.figsize)
            plt.plot(self.df["Log_Ret"].cumsum().apply(np.exp),color="r",label="Market Return")
            plt.legend(loc=0)
            plt.grid(True)
            plt.xlabel("Date",fontsize=self.figsize[0])
            plt.ylabel("Rate",fontsize=self.figsize[0])
            plt.title(self.symbol + " Market Return",fontsize=self.figsize[0])
            return fig
        except:
            plt.close()
            print("Market Return has not been set in the Data Frame.")
            print("\nPlease use *object*.__set_log_return()")

    def plot_strategy(self):
        try:
            fig = plt.figure(figsize=self.figsize)
            plt.plot(self.df["Strategy"].cumsum().apply(np.exp),color="r",label="Strategy")
            plt.legend(loc=0)
            plt.grid(True)
            plt.xlabel("Date",fontsize=self.figsize[0])
            plt.ylabel("Rate",fontsize=self.figsize[0])
            plt.title(self.symbol + " Strategy",fontsize=self.figsize[0])
            return fig
        except:
            plt.close()
            print("Strategy has not been set in the Data Frame.")
            print("\nPlease use *object*.set_strategy()")

    def plot_market_return_and_strategy(self):
        try:
            fig = plt.figure(figsize=self.figsize)
            plt.plot(self.df["Log_Ret"].cumsum().apply(np.exp),color="r",label="Market Return")
            plt.plot(self.df["Strategy"].cumsum().apply(np.exp),color="b",label="Strategy")
            plt.legend(loc=0)
            plt.grid(True)
            plt.xlabel("Date",fontsize=self.figsize[0])
            plt.ylabel("Rate",fontsize=self.figsize[0])
            plt.title(self.symbol + " Market Return and Strategy",fontsize=self.figsize[0])
            return fig
        except:
            plt.close()
            print("Strategy and/or Market Return has not been set in the Data Frame.")
            print("\nPlease use *object*.__set_strategy()")
            print("\nPlease use *object*.__set_market_return()")
            
    def boxplot_multiple_mas(self,window1,window2):
        fig, ax= plt.subplots(figsize=self.figsize)
        quotes = zip(date2num(self.df.index.to_pydatetime()),self.df["Open"],self.df["Close"],self.df["High"],self.df["Low"])
        mpl_finance.candlestick_ochl(ax,quotes,width=0.6,colorup="b",colordown="r")
        ax.xaxis_date()
        plt.grid(True)
        plt.setp(plt.gca().get_xticklabels(), rotation=30)
        try:
            plt.plot(self.df[str(window1)],color="b",label=str(window1))
            plt.plot(self.df[str(window2)],color="g",label=str(window2))
            plt.legend(loc=0)
            plt.grid(True)
            plt.xlabel("Date",fontsize=self.figsize[0])
            plt.ylabel("Price",fontsize=self.figsize[0])
            plt.title(self.symbol + " " + str(window1) + " and " + str(window2) + " MA", fontsize=self.figsize[0])
            return fig
        except:
            plt.close()
            print(str(window1) + " and/or " + str(window2) + " MA has not been set.")
            print("\nPlease use *object*.set_single_moving_average(*window*)")
            print("\nPlease use *object*set_moving_average_regime_between(window1,window2,SD=None)")
        
    def plot_multiple_mas(self, window1, window2):
        try:
            fig = plt.figure(figsize=self.figsize)
            plt.plot(self.df["Close"],color="r",label="Close")
            plt.plot(self.df[str(window1)],color="b",label=str(window1))
            plt.plot(self.df[str(window2)],color="g",label=str(window2))
            plt.legend(loc=0)
            plt.grid(True)
            plt.xlabel("Date",fontsize=self.figsize[0])
            plt.ylabel("Price",fontsize=self.figsize[0])
            plt.title(self.symbol + " " + str(window1) + " and " + str(window2) + " MA", fontsize=self.figsize[0])
            return fig
        except:
            plt.close()
            print(str(window1) + " and/or " + str(window2) + " MA has not been set.")
            print("\nPlease use *object*.set_single_moving_average(*window*)")
            print("\nPlease use *object*set_moving_average_regime_between(window1,window2,SD=None)")
    

    
    def plot_rets_between(self, Stock1):
        cor = pd.DataFrame({self.get_symbol(): self.df["Close"]})
        cor = cor.join(pd.DataFrame({Stock1.get_symbol(): Stock1.get_df()["Close"]}))
        rets = np.log(cor / cor.shift(1))
        cor = cor.fillna(method="bfill")
        fig = plt.figure(figsize=self.figsize)
        plt.subplot(211)
        plt.plot(rets[self.symbol],color="b",label=self.symbol + " Log Return")
        plt.legend(loc=0)
        plt.grid(True)
        plt.ylabel("Rate",fontsize=self.figsize[0])
        plt.title(self.symbol +" Log Return", fontsize=self.figsize[0])
        plt.subplot(212)
        plt.plot(rets[Stock1.get_symbol()],color="r",label=Stock1.get_symbol()+ " Log Return")
        plt.legend(loc=0)
        plt.grid(True)
        plt.xlabel("Date",fontsize=self.figsize[0])
        plt.ylabel("Rate",fontsize=self.figsize[0])
        plt.title(Stock1.get_symbol() +" Log Return", fontsize=self.figsize[0])
        return fig
        
    def plot_regression_between(self, Stock1):
        cor = pd.DataFrame({self.symbol: self.df["Close"]})
        cor = cor.join(pd.DataFrame({Stock1.get_symbol(): Stock1.get_df()["Close"]}))
        rets = np.log(cor / cor.shift(1))
        cor = cor.fillna(method="bfill")
        xdat = rets[self.symbol]
        ydat = rets[Stock1.get_symbol()]
        model = pd.ols(y=ydat, x=xdat)
        fig = plt.figure(figsize=self.figsize)
        plt.plot(xdat, ydat, 'r.')
        ax=plt.axis()
        x=np.linspace(ax[0],ax[1]+0.01)
        plt.plot(x,model.beta[1]+model.beta[0]*x,'b',lw=2)
        plt.grid(True)
        plt.axis("tight")
        plt.ylabel(self.symbol + " returns",fontsize=self.figsize[0])
        plt.xlabel(Stock1.get_symbol() + " returns",fontsize=self.figsize[0])
        plt.title(self.symbol + " and " + Stock1.get_symbol() + " Regression.", fontsize=self.figsize[0])
        return fig
        
    def plot_rolling_corr_between(self,Stock1):
        try:
            cor = pd.DataFrame({self.symbol: self.df["Close"]})
            cor = cor.join(pd.DataFrame({Stock1.get_symbol(): Stock1.get_df()["Close"]}))
            rets = np.log(cor / cor.shift(1))
            cor = cor.fillna(method="bfill")
            fig = plt.figure(figsize=self.figsize)
            plt.plot(pd.rolling_corr(rets[self.symbol],rets[Stock1.get_symbol()],window=252),label=self.symbol \
                     + " and " + Stock1.get_symbol() + " Correlation" )
            plt.grid(True)
            plt.ylabel("Rate",fontsize=self.figsize[0])
            plt.xlabel("Date",fontsize=self.figsize[0])
            plt.legend(loc=0)
            plt.title(self.symbol + " and " + Stock1.get_symbol() + " Correlation" ,\
                      fontsize=self.figsize[0])
            return fig
        except:
            print("Dates are not valid for correlation analysis, skipping...")
        
    def plot_close_between(self,Stock1):
        fig = plt.figure(figsize=self.figsize)
        plt.subplot(211)
        plt.plot(self.df["Close"],color="b",label=self.symbol + " Close")
        plt.legend(loc=0)
        plt.grid(True)
        plt.ylabel("Price",fontsize=self.figsize[0])
        plt.title(self.symbol +" Close", fontsize=self.figsize[0])
        plt.subplot(212)
        plt.plot(Stock1.get_df()["Close"],color="b",label=Stock1.get_symbol() + " Close")
        plt.legend(loc=0)
        plt.grid(True)
        plt.xlabel("Date",fontsize=self.figsize[0])
        plt.ylabel("Price",fontsize=self.figsize[0])
        plt.title(Stock1.get_symbol() +" Close" , fontsize=self.figsize[0])
        return fig
    """
                                SAVERS
    """
    
    def save_close_boxplot_to_pdf(self):
        self.check_if_analysis_dir_exists()
        fig, ax= plt.subplots(figsize=self.figsize)
        quotes = zip(date2num(self.df.index.to_pydatetime()),self.df["Open"],self.df["Close"],self.df["High"],self.df["Low"])
        mpl_finance.candlestick_ochl(ax,quotes,width=0.6,colorup="b",colordown="r")
        ax.xaxis_date()
        plt.grid(True)
        plt.setp(plt.gca().get_xticklabels(), rotation=30)
        plt.legend(loc=0)
        plt.grid(True)
        plt.xlabel("Date",fontsize=self.figsize[0])
        plt.ylabel("Price",fontsize=self.figsize[0])
        plt.title(self.symbol + " Close Price",fontsize=self.figsize[0])
        plt.savefig(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol + "_Close_BP.pdf")
        self.filePaths.append(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol \
                              + "_Close_BP.pdf")
        plt.close()
        
    def save_close_chart_to_pdf(self):
        self.check_if_analysis_dir_exists()
        plt.figure(figsize=self.figsize)
        plt.plot(self.df["Close"],label="Close",color='r')
        plt.legend(loc=0)
        plt.grid(True)
        plt.xlabel("Date",fontsize=self.figsize[0])
        plt.ylabel("Price",fontsize=self.figsize[0])
        plt.title(self.symbol + " Close Price",fontsize=self.figsize[0])
        plt.savefig(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol + "_Close.pdf")
        self.filePaths.append(self.path + "\\" +self.symbol + "\Analysis\\" + self.symbol \
                              + "_Close.pdf")
        plt.close()

    def save_volatility_chart_to_pdf(self):
        try:
            self.check_if_analysis_dir_exists()
            plt.figure(figsize=self.figsize)
            plt.plot(self.df["Volatility"],color='b',label="Volatility")
            plt.legend(loc=0)
            plt.grid(True)
            plt.xlabel("Date",fontsize=self.figsize[0])
            plt.ylabel("% Rate",fontsize=self.figsize[0])
            plt.title(self.symbol + " Volatility",fontsize=self.figsize[0])
            plt.savefig(
                    self.path + "\\" + self.symbol + "\Analysis\\"+ self.symbol + "_Volatility.pdf")
            self.filePaths.append(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol \
                                  + "_Volatility.pdf")
            plt.close()
        except:
            plt.close()
            os.remove(self.path + "\\" + self.symbol + "\Analysis\\"+ self.symbol + "_Volatility.pdf")
            print("Dates are not valid for volatility skipping...")
        

    def save_log_return_chart_to_pdf(self):
        self.check_if_analysis_dir_exists()
        plt.figure(figsize=self.figsize)
        plt.plot(self.df["Log_Ret"],color="b",label="Log Return")
        plt.legend(loc=0)
        plt.grid(True)
        plt.xlabel("Date",fontsize=self.figsize[0])
        plt.ylabel("% Rate",fontsize=self.figsize[0])
        plt.title(self.symbol + " Log Return",fontsize=self.figsize[0])
        plt.savefig(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol + "_LogRet.pdf")
        self.filePaths.append(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol + "_LogRet.pdf")
        plt.close()

    def save_mcs_hist_to_pdf(self, I=10000):
        self.check_if_analysis_dir_exists()
        pdr = self.df["Log_Ret"][1:]
        z = np.random.standard_normal(I)
        ndp = self.df['Close'][-1] * np.exp((np.average(pdr) - ((np.var(pdr) / 2)) + (np.std(pdr) * z)))
        up = float(len(ndp[np.where(ndp >= self.df["Close"][-1])]))*100/I
        down = 100.0-up
        self.probability_up = up
        self.probability_down = down
        self.expected_value = np.average(ndp)
        plt.figure(figsize=self.figsize)
        plt.hist(ndp, bins=50)
        plt.grid(True)
        plt.xlabel("Stock Price",fontsize=self.figsize[0])
        plt.ylabel("Frequency",fontsize=self.figsize[0])
        plt.title(self.symbol+ " Monte Carlo Simulation",fontsize=self.figsize[0])
        plt.savefig(self.path + "\\" + self.symbol + "\Analysis\\"+ self.symbol + "_MonteCarlo.pdf")
        self.filePaths.append(self.path + "\\" +self.symbol + "\Analysis\\"+ self.symbol \
                              + "_MonteCarlo.pdf")
        plt.close()
        
    def save_n_mcs_chart_to_pdf(self,I=10000,T=252):
        self.check_if_analysis_dir_exists()
        S = self.df["Close"][-1]
        plt.figure(figsize=self.figsize)
        for _ in range(I):
            daily_returns=np.random.normal(self.mu/T,self.vol/sqrt(T),T)+1
            price_list=[S]
            for x in daily_returns:
                price_list.append(price_list[-1]*x)
            plt.plot(price_list)
        plt.grid(True)
        plt.xlabel("Frequency",fontsize=self.figsize[0])
        plt.ylabel("Stock Price",fontsize=self.figsize[0])
        plt.title(self.symbol+" "+ str(I)+" Monte Carlo Simulations",fontsize=self.figsize[0])
        plt.savefig(self.path + "\\" +self.symbol + "\Analysis\\"+ self.symbol \
                          + "_" + str(I) + "_Simulations_MonteCarlo.pdf")
        self.filePaths.append(self.path + "\\" +self.symbol + "\Analysis\\"+ self.symbol \
                          + "_" + str(I) + "_Simulations_MonteCarlo.pdf")
            
    def save_n_mcs_hist_daily_returns(self,I=10000,T=252):
        self.check_if_analysis_dir_exists()
        S = self.df["Close"][-1]
        result = []
        for _ in range(I):
            daily_returns=np.random.normal(self.mu/T,self.vol/sqrt(T),T)+1
            price_list=[S]
            for x in daily_returns:
                price_list.append(price_list[-1]*x)
            result.append(price_list[-1])
        self.expected_value2 = round(np.mean(result),2)
        self.fifthquantile = np.percentile(result,5)
        self.ninetyfifthquantile = np.percentile(result,95)
        fig = plt.figure(figsize=self.figsize)
        plt.hist(result, bins=100)
        plt.grid(True)
        plt.axvline(np.percentile(result,5), color='r', linestyle='dashed', linewidth=2)
        plt.axvline(np.percentile(result,95), color='r', linestyle='dashed', linewidth=2)
        plt.xlabel("Stock Price",fontsize=self.figsize[0])
        plt.ylabel("Frequency",fontsize=self.figsize[0])
        plt.title(self.symbol+" " +str(I)+" Monte Carlo Simulations",fontsize=self.figsize[0])
        plt.savefig(self.path + "\\" +self.symbol + "\Analysis\\"+ self.symbol \
                              +"_"+ str(I) + "_DailyReturns_MonteCarlo.pdf")
        self.filePaths.append(self.path + "\\" +self.symbol + "\Analysis\\"+ self.symbol \
                              +"_"+ str(I) + "_DailyReturns_MonteCarlo.pdf")
        
        
        
    def save_single_ma_chart_to_pdf(self, window):
        try:
            self.check_if_analysis_dir_exists()
            plt.figure(figsize=self.figsize)
            plt.plot(self.df[str(window)],color='b',label=str(window) + " MA")
            plt.legend(loc=0)
            plt.grid(True)
            plt.title(self.symbol + str(window) + " MA",fontsize=self.figsize[0])
            plt.xlabel("Price",fontsize=self.figsize[0])
            plt.ylabel("Date",fontsize=self.figsize[0])
            plt.savefig(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol + "_" + str(window) \
                + "_SMA.pdf")
            self.filePaths.append(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol + "_" \
                + str(window) + "_SMA.pdf")
            plt.close()
        except:
            plt.close()
            print(str(window) + " MA has not been set.")
            print("\nPlease use *variable*.set_single_moving_average(*window*)")
    
    
    def save_multiple_mas_boxplots_to_pdf(self, window1, window2):
        self.check_if_analysis_dir_exists()
        fig, ax= plt.subplots(figsize=self.figsize)
        quotes = zip(date2num(self.df.index.to_pydatetime()),self.df["Open"],self.df["Close"],self.df["High"],self.df["Low"])
        mpl_finance.candlestick_ochl(ax,quotes,width=0.6,colorup="b",colordown="r")
        ax.xaxis_date()
        plt.grid(True)
        plt.setp(plt.gca().get_xticklabels(), rotation=30)
        try:
            plt.plot(self.df[str(window1)],color="b",label=str(window1))
            plt.plot(self.df[str(window2)],color="g",label=str(window2))
            plt.legend(loc=0)
            plt.grid(True)
            plt.xlabel("Date",fontsize=self.figsize[0])
            plt.ylabel("Price",fontsize=self.figsize[0])
            plt.title(self.symbol + " " + str(window1) + " and " + str(window2) + " MA", fontsize=self.figsize[0])
            plt.savefig(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol + "_" + str(window1) \
                + "_" + str(window2) + "_MMA_BP.pdf")
            self.filePaths.append(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol + "_" \
                + str(window1) + "_" + str(window2) + "_MMA_BP.pdf")
            plt.close()
        
        except:
            plt.close()
            print(str(window1) + " and/or " + str(window2) + " MA has not been set.")
            print("\nPlease use *object*.set_single_moving_average(*window*)")
            print("\nPlease use *object*set_moving_average_regime_between(window1,window2,SD=None)")
            
    def save_multiple_mas_charts_to_pdf(self, window1, window2):
        try:
            self.check_if_analysis_dir_exists()
            plt.figure(figsize=self.figsize)
            plt.plot(self.df["Close"],color="r",label="Close")
            plt.plot(self.df[str(window1)],color="b",label=str(window1))
            plt.plot(self.df[str(window2)],color="g",label=str(window2))
            plt.legend(loc=0)
            plt.grid(True)
            plt.xlabel("Date",fontsize=self.figsize[0])
            plt.ylabel("Price",fontsize=self.figsize[0])
            plt.title(self.symbol + " " + str(window1) + " and " + str(window2) + " MA", fontsize=self.figsize[0])
            plt.savefig(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol + "_" + str(window1) \
                + "_" + str(window2) + "_MMA.pdf")
            self.filePaths.append(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol + "_" \
                + str(window1) + "_" + str(window2) + "_MMA.pdf")
            plt.close()
        except:
            plt.close()
            print(str(window1) + " and/or " + str(window2) + " MA has not been set.")
            print("\nPlease use *object*.set_single_moving_average(*window*)")
            print("\nPlease use *object*set_moving_average_regime_between(window1,window2,SD=None)")

    def save_ma_regime_strategy_marketr_charts_to_pdf(self, window1, window2):
        try:
            self.check_if_analysis_dir_exists()
            plt.figure(figsize=self.figsize)
            plt.subplot(221)
            plt.plot(self.df["Close"],label="Close")
            plt.plot(self.df[str(window1)],label=str(window1) + " MA")
            plt.grid(True)
            plt.legend(loc=0)
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.title(str(window1) + " days MA")
            plt.subplot(222)
            plt.plot(self.df["Close"],label="Close")
            plt.plot(self.df[str(window2)],label=str(window2) + " MA")
            plt.grid(True)
            plt.legend(loc=0)
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.title(str(window2) + " days MA")
            plt.subplot(223)
            plt.plot(self.df["Regime"],color="b")
            plt.grid(True)
            plt.legend(loc=0)
            plt.xlabel("Date")
            plt.ylabel("Rate")
            plt.title("Regime")
            plt.subplot(224)
            plt.plot(self.df["Strategy"].cumsum().apply(np.exp),label="Strategy")
            plt.plot(self.df["Log_Ret"].cumsum().apply(np.exp),label="Market")
            plt.grid(True)
            plt.legend(loc=0)
            plt.xlabel("Date")
            plt.ylabel("% Return")
            plt.title("Strategy and Market Return")
            plt.savefig(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol + "_" + str(window1) \
                + "_" + str(window2) + "_MA_Regime_Strategy_MR.pdf")
            self.filePaths.append(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol + "_" + \
                str(window1) + "_" + str(window2) + "_MA_Regime_Strategy_MR.pdf")
            plt.close()

        except:
            plt.close()
            print(str(window1) + " and/or " + str(window2) + " has not been set.")
            print("\nPlease use *object*.__set_moving_average_regime_between(*window1*,*window2*,*SD*")
            print("\nStrategy and/or Market Return has not been set.")
            print("\nPlease use *object*.__set_strategy() and/or *object*.__set_market_return()")
    
    
    def save_market_return_chart_to_pdf(self):
        try:
            self.check_if_analysis_dir_exists()
            plt.figure(figsize=self.figsize)
            plt.plot(self.df["Log_Ret"].cumsum().apply(np.exp),color="r",label="Market Return")
            plt.legend(loc=0)
            plt.grid(True)
            plt.xlabel("Date",fontsize=self.figsize[0])
            plt.ylabel("Rate",fontsize=self.figsize[0])
            plt.title(self.symbol + " Market Return",fontsize=self.figsize[0])
            plt.savefig(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol + "_MarketReturn.pdf")
            self.filePaths.append(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol + "_MarketReturn.pdf")
            plt.close()
        except:
            plt.close()
            print("Market Return has not been set in the Data Frame.")
            print("\nPlease use *object*.__set_market_return()")

    def save_strategy_chart_to_pdf(self):
        try:
            plt.figure(figsize=self.figsize)
            plt.plot(self.df["Strategy"].cumsum().apply(np.exp),color="r",label="Strategy")
            plt.legend(loc=0)
            plt.grid(True)
            plt.xlabel("Date",fontsize=self.figsize[0])
            plt.ylabel("Rate",fontsize=self.figsize[0])
            plt.title(self.symbol + " Strategy",fontsize=self.figsize[0])
            plt.savefig(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol + "_Strategy.pdf")
            self.filePaths.append(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol + "_Strategy.pdf")
            plt.close()
        except:
            plt.close()
            print("Strategy has not been set in the Data Frame.")
            print("\nPlease use *object*.set_strategy()")

    def save_market_return_and_strategy_chart_to_pdf(self):
        try:
            self.check_if_analysis_dir_exists()
            plt.figure(figsize=self.figsize)
            plt.plot(self.df["Log_Ret"].cumsum().apply(np.exp),color="r",label="Market Return")
            plt.plot(self.df["Strategy"].cumsum().apply(np.exp),color="b",label="Strategy")
            plt.legend(loc=0)
            plt.grid(True)
            plt.xlabel("Date",fontsize=self.figsize[0])
            plt.ylabel("Rate",fontsize=self.figsize[0])
            plt.title(self.symbol + " Market Return and Strategy",fontsize=self.figsize[0])
            plt.savefig(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol + \
                        "_Market&Strategy.pdf")
            self.filePaths.append(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol + \
                                  "_Market&Strategy.pdf")
            plt.close()
        except:
            plt.close()
            print("Strategy and/or Market Return has not been set in the Data Frame.")
            print("\nPlease use *object*.__set_strategy()")
            print("\nPlease use *object*.__set_market_return()")
    
    def save_rets_between(self,Stock1):
        self.check_if_comparison_dir_exists(Stock1)
        cor = pd.DataFrame({self.get_symbol(): self.df["Close"]})
        cor = cor.join(pd.DataFrame({Stock1.get_symbol(): Stock1.get_df()["Close"]}))
        rets = np.log(cor / cor.shift(1))
        cor = cor.fillna(method="bfill")
        plt.figure(figsize=self.figsize)
        plt.subplot(211)
        plt.plot(rets[self.symbol],color="b",label=self.symbol + " Log Return")
        plt.legend(loc=0)
        plt.grid(True)
        plt.ylabel("Rate",fontsize=self.figsize[0])
        plt.xlabel("Date",fontsize=self.figsize[0])
        plt.title(self.symbol +" Log Return", fontsize=self.figsize[0])
        plt.subplot(212)
        plt.plot(rets[Stock1.get_symbol()],color="r",label=Stock1.get_symbol()+ " Log Return")
        plt.legend(loc=0)
        plt.grid(True)
        plt.xlabel("Date",fontsize=self.figsize[0])
        plt.ylabel("Rate",fontsize=self.figsize[0])
        plt.title(Stock1.get_symbol() +" Log Return", fontsize=self.figsize[0])
        plt.savefig(self.path + "\\" + self.symbol + "\Comparisons\\" \
                    + Stock1.get_symbol() + "\\" +self.symbol + "_and_" + Stock1.get_symbol() + "_Returns.pdf")
        self.comparedFilePaths.append(self.path + "\\" + self.symbol + "\Comparisons\\"\
                    + Stock1.get_symbol() + "\\" +self.symbol + "_and_" + Stock1.get_symbol() \
                    + "_Returns.pdf")
        plt.close()
    
    def save_regression_between(self, Stock1):
        self.check_if_comparison_dir_exists(Stock1)
        cor = pd.DataFrame({self.symbol: self.df["Close"]})
        cor = cor.join(pd.DataFrame({Stock1.get_symbol(): Stock1.get_df()["Close"]}))
        rets = np.log(cor / cor.shift(1))
        cor = cor.fillna(method="bfill")
        xdat = rets[self.symbol]
        ydat = rets[Stock1.get_symbol()]
        model = pd.ols(y=ydat, x=xdat)
        plt.figure(figsize=self.figsize)
        plt.plot(xdat, ydat, 'r.')
        ax=plt.axis()
        x=np.linspace(ax[0],ax[1]+0.01)
        plt.plot(x,model.beta[1]+model.beta[0]*x,'b',lw=2)
        plt.grid(True)
        plt.axis("tight")
        plt.ylabel(self.symbol + " returns",fontsize=self.figsize[0])
        plt.xlabel(Stock1.get_symbol() + " returns",fontsize=self.figsize[0])
        plt.title(self.symbol + " and " + Stock1.get_symbol() + " Regression.", fontsize=self.figsize[0])
        plt.savefig(self.path + "\\" + self.symbol + "\Comparisons\\" \
                    + Stock1.get_symbol() + "\\" +self.symbol + "_and_" + Stock1.get_symbol() + "_Regression.pdf")
        self.comparedFilePaths.append(self.path + "\\" + self.symbol + "\Comparisons\\" \
                    + Stock1.get_symbol() + "\\" +self.symbol + "_and_" + Stock1.get_symbol() + "_Regression.pdf")
        plt.close()
        
    def save_rolling_corr_between(self,Stock1):
        self.check_if_comparison_dir_exists(Stock1)
        cor = pd.DataFrame({self.symbol: self.df["Close"]})
        cor = cor.join(pd.DataFrame({Stock1.get_symbol(): Stock1.get_df()["Close"]}))
        cor = cor.fillna(method="bfill")
        rets = np.log(cor / cor.shift(1))
        plt.figure(figsize=self.figsize)
        plt.plot(pd.rolling_corr(rets[self.symbol],rets[Stock1.get_symbol()],window=252))
        plt.grid(True)
        plt.ylabel("Rate",fontsize=self.figsize[0])
        plt.xlabel("Date",fontsize=self.figsize[0])
        plt.legend(loc=0)
        plt.title(self.symbol + " and " + Stock1.get_symbol() + " Correlation" ,\
                  fontsize=self.figsize[0])
        plt.savefig(self.path + "\\" + self.symbol + "\Comparisons\\" \
                    + Stock1.get_symbol() + "\\" +self.symbol + "_and_" + Stock1.get_symbol() + "_Correlation.pdf")
        self.comparedFilePaths.append(self.path + "\\" + self.symbol + "\Comparisons\\" \
                    + Stock1.get_symbol() + "\\" +self.symbol + "_and_" + Stock1.get_symbol() + "_Correlation.pdf")
        plt.close()
        
    def save_close_between(self,Stock1):
        self.check_if_comparison_dir_exists(Stock1)
        plt.figure(figsize=self.figsize)
        plt.subplot(211)
        plt.plot(self.df["Close"],color="b",label=self.symbol + " Close")
        plt.legend(loc=0)
        plt.grid(True)
        plt.ylabel("Price",fontsize=self.figsize[0])
        plt.xlabel("Date",fontsize=self.figsize[0])
        plt.title(self.symbol +" Close", fontsize=self.figsize[0])
        plt.subplot(212)
        plt.plot(Stock1.get_df()["Close"],color="b",label=Stock1.get_symbol() + " Close")
        plt.legend(loc=0)
        plt.grid(True)
        plt.xlabel("Date",fontsize=self.figsize[0])
        plt.ylabel("Price",fontsize=self.figsize[0])
        plt.title(Stock1.get_symbol() +" Close" , fontsize=self.figsize[0])
        plt.savefig(self.path + "\\" + self.symbol + "\Comparisons\\" \
                    + Stock1.get_symbol() + "\\" +self.symbol + "_and_" + Stock1.get_symbol() + "_Close.pdf")
        self.comparedFilePaths.append(self.path + "\\" + self.symbol + "\Comparisons\\" \
                    + Stock1.get_symbol() + "\\" +self.symbol + "_and_" + Stock1.get_symbol() + "_Close.pdf")
        plt.close()
    
    """
                                OPENERS
    """
    def open_analysis_results_file(self):
        if os.path.isfile(self.get_analysis_file_location() + "_Results.txt"):
            os.startfile(self.get_analysis_file_location() + "_Results.txt")
        else: 
            print("File doesn't exists.")
        
    def open_csv_file(self):
        if os.path.isfile(self.get_analysis_file_location() + ".csv"):
            os.startfile(self.get_analysis_file_location() + ".csv")
        else: 
            print("File doesn't exists.")
        
    def open_FullAnalysis_file(self):
        if os.path.isfile(self.get_analysis_file_location() + "_FullAnalysis.pdf"):
            os.startfile(self.get_analysis_file_location() + "_FullAnalysis.pdf")
        else: 
            print("File doesn't exists.")
    
    def open_comparison_results_file(self):
        if os.path.isfile(self.get_comparisons_file_location()+"_ComparisonResults.txt"):
            os.startfile(self.get_comparisons_file_location()+"_ComparisonResults.txt")
        else:
            print("File doesn't exists.")
    
    def open_FullComparison_file(self):
        if os.path.isfile(self.get_comparisons_file_location()+"_FullComparison.pdf"):
            os.startfile(self.get_comparisons_file_location()+"_FullComparison.pdf")
        else:
            print("File doesn't exists.")
    
    def open_all_files(self):
        self.open_analysis_results_file()
        self.open_FullAnalysis_file()
        self.open_comparison_results_file()
        self.open_FullComparison_file()
        self.open_csv_file()
    
    """
                                SETTERS
    """

    def __set_single_moving_average(self, window):
        self.df[str(window)] = self.df['Close'].rolling(window=window, min_periods=0).mean()
        
    def __set_moving_average_regime_between(self, window1, window2, SD=None):
        if not SD:
            SD = self.SD
        self.df[str(window1)] = self.df["Close"].rolling(window=window1, min_periods=0).mean()
        self.df[str(window2)] = self.df["Close"].rolling(window=window2, min_periods=0).mean()
        self.df[str(window1) + " - " + str(window2)] = self.df[str(window1)] - self.df[str(window2)]
        self.df["Regime"] = np.where(self.df[str(window1) + " - " + str(window2)] > SD, 1, 0)
        self.df["Regime"] = np.where(self.df[str(window1) + " - " + str(window2)] < -SD, -1, self.df["Regime"])


    def __set_strategy(self):
        try:
            self.df["Strategy"] = self.df["Regime"].shift(1) * self.df["Log_Ret"]
        except:
            print("Regime and/or Market has not been set")
            print("\nPlease use *object*.set_market_return() and *object*.set_moving_average_regime_between(*window1*,\
            *window2*,*SD*)")

    def __set_volatility(self):
        self.df['Volatility'] = pd.rolling_std(self.df['Log_Ret'], window=252) * np.sqrt(252)

    def __set_log_return(self):
        self.df['Log_Ret'] = np.log(self.df['Close'] / self.df['Close'].shift(1))

    def __set_volatility_and_log_return(self):
        self.__set_log_return()
        self.__set_volatility()
        return self.df
    
    def __set_Adj_Close(self):
        self.df["Aux"] = self.df["Close"]
        self.df["Adj Close"] = self.df["Aux"]
        self.df["Close"] =  data.get_data_yahoo(self.symbol, data_source="yahoo", start=self.start, end=self.end)["Close"]
        del self.df["Aux"]
    
    def set_privates(self,MA1=42,MA2=252):
        self.__set_moving_average_regime_between(MA1, MA2)
        self.__set_volatility_and_log_return()
        self.__set_strategy()
        self.__set_CAGR_ANV()
        self.__set_probabilities()
    
    def set_figsize(self,figsize):
        self.figsize=figsize
        
    def __set_CAGR_ANV(self):
        days = (self.df.index[-1] - self.df.index[0]).days
        cagr = ((((self.df["Close"][-1])/self.df["Close"][1]))**(365.0/days))-1
        self.mu =cagr
        self.df['Returns'] = self.df['Close'].pct_change()
        self.vol = self.df['Returns'].std()*sqrt(252)
        
    def __set_probabilities(self,I=10000):
        pdr = self.df["Log_Ret"][1:]
        z = np.random.standard_normal(I)
        ndp = self.df['Close'][-1] * np.exp((np.average(pdr) - ((np.var(pdr) / 2)) + (np.std(pdr) * z)))
        up = float(len(ndp[np.where(ndp >= self.df["Close"][-1])]))*100/I
        down = 100.0-up
        self.probability_up = up
        self.probability_down = down
        self.expected_value = np.average(ndp)
        
    def set_path(self,path):
        self.path = path
        
        
    def clean_comparedFilePaths(self):
        self.comparedFilePaths=[]
    
    def delete_all(self):
        gc.enable()
        del self.df
        del self.comparedFilePaths
        del self.data_source
        del self.SD
        del self.probability_down
        del self.probability_up
        del self.end
        del self.start
        del self.symbol
        del self.expected_value
        del self.fromDoc
        del self.filePaths
        del self.figsize
        del self.mu
        del self.vol
        del self.expected_value2
        gc.collect()
        

    """
                                GETTERS
    """

    def get_df(self):
        return self.df

    def get_symbol(self):
        return self.symbol
    
    def get_start(self):
        return self.start
    
    def get_end(self):
        return self.end
    
    def get_figsize(self):
        return self.figsize

    def get_current_close_price(self):
        return self.df['Close'][-1]

    def get_expected_value(self):
        return self.expected_value

    def get_probability_up(self):
        return self.probability_up

    def get_probability_down(self):
        return self.probability_down
    
    def get_analysis_file_location(self):
        return os.path.abspath(self.path + "\\" + self.symbol + "\Analysis\\" + self.symbol)
    
    def get_comparisons_file_location(self):
        return os.path.abspath(self.path + "\\" + self.symbol + "\Comparisons\\" + self.symbol)

    def get_path(self):
        return self.path
    
    

    """
                                STATICS
    """
    @staticmethod
    def check_if_log_exists(path):
        if not os.path.exists(path + "\Logs\\"):
            os.makedirs(path + "\Logs\\")
    
    @staticmethod
    def check_if_progress_exists(path):
        if not os.path.exists(path + "\Progress\\"):
            os.makedirs(path + "\Progress\\")
            
    @staticmethod
    def look_for_afordable_stocks_sp500():
        try:
            with open(self.path + "\sp500\sp500tickers.pickle","rb") as f:
                tickers = pickle.load(f)
        except:
            print("S&P500 data has not been loaded)
        
    @staticmethod
    def save_sp500_tickers(path):
        resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})
        tickers = []
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[0].text
            tickers.append(ticker)
        if not os.path.exists(path + "\sp500\\"):
            os.makedirs(path + "\sp500\\")
        with open(path + "\sp500\sp500tickers.pickle", "wb") as f:
            pickle.dump(tickers, f)       
    
    @staticmethod
    def analyze_sp500_data(path,start=dt.datetime(2000, 1, 1),end=dt.datetime.now()):
        Stock.save_sp500_tickers(path)
        try:
            with open(path + "\sp500\sp500tickers.pickle", "rb") as f:
                tickers = pickle.load(f)
        except:
            print("S&P500 data has not been loaded.")
        progress = 0
        Stock.check_if_log_exists(path)
        startg = time.time()
        with open(path + "\Logs\\" + strftime("%b-%d-%Y_%H%M%S", localtime()) + "__S&P500_log.txt","a") as f:
            for ticker in tickers:
                try:
                    f.write(strftime("%b %d %Y %H:%M:%S", localtime())+ "- Starting analysis of: " + ticker +"\n")
                    print("Starting analysis of: " + ticker)
                    s = Stock(ticker,path, start, end, figsize=(15, 15))
                    s.full_analysis()
                    del s
                    progress += 1
                    f.write(strftime("%b %d %Y %H:%M:%S", localtime())+ "- " + str(progress) + ". " + ticker + " analyzed." + "\n")
                    print(str(progress) + ". " + ticker + " analyzed.")
                    strprogress = str(round(float(progress) * 100 / len(tickers), 2))
                    f.write(strftime("%b-%d-%Y %H:%M:%S", localtime())+ "- " + "Progress: " + strprogress + "%.\n\n")
                    print("Progress: " + strprogress + "%.\n\n")
                    if progress == len(tickers):
                        f.write(strftime("%b %d %Y %H:%M:%S", localtime())+  "- " + "Analysis completed successfully.")
                        print("Analysis completed successfully.")
                except:
                    f.write(strftime("%b %d %Y %H:%M:%S", localtime())+  "- " + ticker + " not found." + "\n\n")
                    print(ticker + " not found.")
                progress+=1
            endg = time.time()
            f.write("\n\n" + strftime("%b-%d-%Y %H:%M:%S", localtime())+ "- Overall time:" + str(endg-startg))
            print(str(endg - startg))

