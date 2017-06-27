# -*- coding: utf-8 -*-
"""
Created on Sat May 27 22:49:41 2017

@author: Jorge Alberto Niño Cabal
version: 0.1

THIS MODULE IS CURRENTLY UNDER DEVELOPMENT
"""

from Lib import * 
class Option():
    
    def __init__(self,symbol):
        self.symbol = symbol
        self.df = Options(self.symbol).get_all_data()
    
    
    def check_if_analysis_dir_exists(self,path=""):
        if not os.path.exists("Generated\Options\\" + path + "\\" + self.symbol + "\Analysis\\"):
            os.makedirs("Generated\Options\\" + path + "\\" + self.symbol + "\Analysis\\")
    
    def transfer_to_csv(self,path=""):
        self.check_if_analysis_dir_exists(path)
        self.df.to_csv(self.get_analysis_file_location(path) + ".csv")
    
    def monteCarloOptions(self,So=100, K=105, T=1.0, r=0.05, sigma=0.2,I=10000):
        """
        Monte Carlo Valuation of European call option
        Analytical Formula
        
        Parameters
        ===========
        So: int
            initial index level
        K: int
            strike price
        T: float
            time-to-maturity
        r: float
            riskless short rate
        sigma: float
            volatility 
        I: int
            number of simulations
        Returns
        =========
        value: float
            present value of the European call option
        """
        z = np.random.standard_normal(I)
        ST = So*np.exp((r-0.5*sigma**2)*T+sigma*np.sqrt(T)*z)
        hT = np.maximum(ST-K,0)
        Co=np.exp(-r*T)*np.sum(hT)/I
        print "Value of the European Call option %5.3f" %Co
    
    
    def monteCarloSimulation(self,So=100, K=105, T=1.0, r=0.05, sigma=0.2,M=50,I=250000):
        seed(20000)
        to = time()
        dt = T/M
        S=[]
        for i in range(I):
            path = []
            for t in range(M+1):
                if t == 0:
                    path.append(So)
                else:
                    z=gauss(0.0,1.0)
                    St=path[t-1]*exp((r-0.5*sigma**2)*dt + sigma*sqrt(dt) * z)
                    path.append(St)
            S.append(path)
        # Calculating the Monte Carlo estimator
        Co = exp(-r*T)*sum([max(path[-1]-K,0) for path in S])/I
        #Results output
        tpy = time() - to
        print "European option value %7.3f" %Co
        print "Duration in Seconds %7.3f" %tpy
    
    def monteCarloSimulationNp(self,So=100, K=105, T=1.0, r=0.05, sigma=0.2,M=50,I=250000):
        np.random.seed(20000)
        to = time()
        dt = T/M
        S = np.zeros((M+1,I))
        S[0]=So
        for t in range(1,M+1):
            z=np.random.standard_normal(I)
            S[t]=S[t-1]*np.exp((r-0.5*sigma**2)*dt+sigma*sqrt(dt)*z)
        Co = exp(-r*T)*np.sum(np.maximum(S[-1]-K,0))/I
        tpy = time() - to
        print "European option value %7.3f" %Co
        print "Duration in Seconds %7.3f" %tpy
        plt.plot(S[:, :10])
        plt.grid(True)
        plt.xlabel("Time Step")
        plt.ylabel("Index Level")
        plt.show()
        plt.hist(S[-1],bins=50)
        plt.grid(True)
        plt.xlabel("Index Level")
        plt.ylabel("Frequency")
        plt.show()
        plt.hist(np.maximum(S[-1]-K,0),bins=50)
        plt.grid(True)
        plt.xlabel("Option Inner Value")
        plt.ylabel("Frequency")
        plt.ylim(0,50000)
        plt.show()
        
    def bsm_call_value(So,K,T,r,sigma):
        """
        Valuation of European call option in BSM model.
        Analytical Formula
        
        Parameters
        ===========
        So: float
            initial stock/index level
        K: float
            strike price
        T: float
            maturity date (in year fractions)
        r: float
            constant risk-free short rate
        sigma: float
            volatility factor in diffusion term
        Returns
        =========
        value: float
            present value of the European call option
        """
        So = float(So)
        d1 = (log(So/K)+(r+0.5*sigma**2)*T)/(sigma*sqrt(T))
        d2 = (log(So/K)+(r-0.5*sigma**2)*T)/(sigma*sqrt(T))
        value=(So*stats.norm.cdf(d1 ,0.0,1.0)-K * exp(-r*T)*stats.norm.cdf(d2,0.0,1.0))
        # stats.norm.cdf --> cumulative distribution function for normal distribution
        return value
    def bsm_vega(So,K,T,R,sigma):
        """
        Vega of European option in BSM model.
        
        Parameters
        ===========
        So: float
            initial stock/index level
        K: float
            strike price
        T: float
            maturity date (in year fractions)
        r: float
            constant risk-free short rate
        sigma: float
            volatility factor in diffusion term
        Returns
        =========
        vega: float
            partial derivative of BSM formula with respect to sigma, i.e, Vega
        """
        So = float(So)
        d1 = (log(So/K)+(r+0.5*sigma**2)*T)/(sigma*sqrt(T))
        vega = So * stats.norm.cdf(d1, 0.0, 1.0) * sqrt(T)
        return vega
    
    def bsm_call_imp_vol(So, K, T, R, Co, sigma_est, it=100):
        """
        Implied volatility of European call option in BSM model.
        
        Parameters
        ===========
        So: float
            initial stock/index level
        K: float
            strike price
        T: float
            maturity date (in year fractions)
        r: float
            constant risk-free short rate
        sigma_est: float
            estimate of impl. volatility
        it: integer
            number of iterations
        Returns
        =========
        sigma_est: float
            numerically estimated implied volatility
        """
        for i in range(it):
            sigma_est -= ((bsm_call_value(So,K,T,R,sigma_est)-Co)/bsm_vega(So,K,T,R,sigma_est))
            return sigma_est
    
    def binomial_np(strike,So = 100, T=1, r = 0.05, vola = 0.20, M=1000):
        """ Binomial option pricing with NumPy
        
        Parameters
        ==============
        strike: float
            strike price of the European call option
        So: float
            initial index level 
        T: int 
            call option maturity
        r: float
            constant short rate
        vola: float
            constant volatility factor of diffusion
        M: int
            time steps
        """
        #Index levels with NumPy
        
        dt = T/M # length of time interval
        df = exp(-r*dt) # discount factor per time interval
        u = exp(vola*sqrt(dt)) #up-movement
        d = 1/u # down-movement
        q = (exp(r*dt) - d) / (u-d) # martingale probability
        mu = np.arange(M+1)
        mu = np.resize(mu,(M+1,M+1))
        md = np.transpose(mu)
        mu = u ** (mu-md)
        md = d**md
        S = So * mu * md
        pv = np.maximum(S-strike,0)
        z=0
        for t in range(M-1,-1,-1):
            pv[0:M-z,t]=(q*pv[0:M-z,t+1]+(1-q)*pv[1:M-z+1,t+1]) * df
            z+=1
        return pv[0,0]
        
        """
        
                                    GETTERS
        """
    
    def get_analysis_file_location(self,path):
        return os.path.abspath("Generated\Options\\" + path + "\\" + self.symbol + "\Analysis\\" + self.symbol)
    
    def get_df(self):
        return self.df