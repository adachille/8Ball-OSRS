"""
NOTE: Many of the techniques here are build using the guidance of Investopedia, including some of the 
description documentation for the methods.
"""
import pandas as pd
import numpy as np

# TODO: make this file return information as pandas series and take in information as pandas
class ExtractorTechnicalIndicators:   
    """
    A class used to extract technical indicator using a price signal (price over time)

    ...

    Attributes
    ----------

    Methods
    -------
    simple_moving_average(prices, n)
        Get the simple moving average of the prices using n as the period
    exponential_moving_average(prices, n)
        Get the exponential moving average of the prices using n as the period
    rsi(self, prices, n)
        Get the Relative Strength Index (RSI) of the prices using n as the period
    moving_std_dev(self, prices, n)
        Get the moving standard deviation of the prices using n as the period
    bollinger_bands(self, prices, n)
        Get the Bollinger Bands of the prices using n as the period

    """
    def __init__(self):
        print("init")

    ### TREND INDICATORS ###
    def simple_moving_average(self, prices, n=12):
        """Get the simple moving average (SMA) of the prices using n as the period.

        SMA is a trend indicator that uses the n most recent prices to calculate a moving average.
        Short-term averages respond quickly to changes in the price of the underlying, while 
        long-term averages are slow to react. 

        Parameters
        ----------
        prices : ndarray
            numpy array of prices to get the SMA from
        n : int
            the period to use for the moving average

        Returns
        -------
        pd.Series
            an array of simple moving average values for prices, will have length = len(prices)
            but will only have len(prices) - n + 1 smas, the rest will be nan's
        """
        prices_series = pd.Series(prices)
        smas = prices_series.rolling(window=n).mean()    
        return smas.to_numpy()
    
    def exponential_moving_average(self, prices, n=12, weighting_factor=None):
        """Get the exponential moving average (EMA) of the prices using n as the period.

        EMA is a trend indicator that uses the n most recent prices to calculate a moving average.
        EMA uses exponential weighting to put more emphasis on recent prices over old prices.
        Short-term averages respond quickly to changes in the price of the underlying, while 
        long-term averages are slow to react. 

        Parameters
        ----------
        prices : ndarray
            numpy array of prices to get the EMA from
        n : int
            the period to use for the moving average
        weighting_factor : float
            the weighting multiplier for the moving average, defaults to 2 / (n + 1)


        Returns
        -------
        ndarray
            an array of exponential moving average values for prices, will have length = 
            len(prices) but will only have len(prices) - n + 1 smas, the rest will be nan's
        """
        if weighting_factor is None:
            wf = 2 / (n + 1)
        else:
            wf = weighting_factor
            
        smas = self.simple_moving_average(prices, n)

        emas = np.empty(prices.shape)
        emas[:n-1] = np.nan # Default the first n values to be nan
        emas[n-1] = smas[n-1]
        # Calculate emas using prices and smas
        for i in range(n, len(smas)):
            emas[i] = (prices[i] - emas[i-1]) * wf + emas[i-1]

        return emas
    
    # TODO: finish implementing
    def moving_average_convergence_divergence(self, prices, n_lt=26, n_st=12):
        """Get the Moving Average Convergence Divergence (MACD) of the prices using n as the period.

        MACD is a trend indicator that measures the relationship between the short term and long term
        exponential moving averages of prices.

        """
        pass

    ### MOMENTUM INDICATORS ###
    def rsi(self, prices, n=14):
        """Get the Relative Strength Index, a momentum indicator that measures the magnitude of 
        recent price changes to evaluate overbought or oversold conditions. The RSI is an 
        oscillator, moving between two extremes and can have a reading from 0 to 100.

        Traditional interpretation and usage of the RSI are that values of 70 or above indicate
        that a security is becoming overbought or overvalued and may be primed for a trend reversal
        or corrective pullback in price. An RSI reading of 30 or below indicates an oversold or 
        undervalued condition.
        
        Parameters:
        ----------
        prices : pandas.Series
            series of prices to get the RSI from
        n : int
            the period to use for the RSI

        Returns
        -------
        pandas.Series
            the RSI of the prices, will have length = len(prices) but will only have 
            len(prices) - n values, the rest will be nan's
        """
        # Get price deltas
        prices_df = pd.DataFrame(data={"prices": prices})
        prices_df["delta"] = prices_df["prices"] - prices_df["prices"].shift(1)

        
        # Get up deltas and down deltas
        up_delta, down_delta = prices_df["delta"].copy(), prices_df["delta"].copy()
        up_delta[up_delta < 0] = 0
        down_delta[down_delta > 0] = 0
        
        # Get rolling means
        smas = prices_df.rolling(window=n).mean()    
        up_rolling = up_delta.rolling(window=n).mean()
        down_rolling = down_delta.rolling(window=n).mean().abs()
        rs = up_rolling / down_rolling
        rsi = 100.0 - (100.0 / (1.0 + rs))
        return rsi

    ### VOLATILITY INDICATORS ###

    def moving_std_dev(self, prices, n=12):
        """Get the standard deviation of the prices

        Standard deviation is a classic volatility technical indicator.

        Parameters
        ----------
        prices : ndarray
            numpy array of prices to get the standard deviation from

        Returns
        -------
        ndarray
            the moving standard of prices, will have length = len(prices) but will only have 
            len(prices) - n + 1 values, the rest will be nan's
        """
        prices_series = pd.Series(prices)
        moving_std_dev = prices_series.rolling(window=n).std()
        return moving_std_dev.to_numpy()
    
    def bollinger_bands(self, prices, n=20):
        """Get the standard deviation of the prices

        Standard deviation is a classic volatility technical indicator.

        Parameters
        ----------
        prices : ndarray
            numpy array of prices to get the Bollinger bands from

        Returns
        -------
        (ndarray, ndarray, ndarray)
            three ndarray's, one with the lower bollinger band, the sma, and one with the upper 
            bollinger band, each array will have length = len(prices) but will only have 
            len(prices) - n + 1 values, the rest will be nan's
        """
        sma = self.simple_moving_average(prices, n)
        moving_std_dev = self.moving_std_dev(prices, n)
        return (sma - 2*moving_std_dev, sma, sma + 2*moving_std_dev)