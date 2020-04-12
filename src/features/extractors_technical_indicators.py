"""
NOTE: Many of the techniques here are build using the guidance of Investopedia, including some of the 
description documentation for the methods.
"""
import pandas as pd
import numpy as np

# TODO: make this file return information in a more specific way, needs a stricter interface
class ExtractorTechnicalIndicators:   
    """
    A class used to extract technical indicator using a price signal (price over time)

    ...

    Attributes
    ----------

    Methods
    -------
    get_simple_moving_average(prices, n)
        Get the simple moving average of the prices using n as the period

    """
    def __init__(self):
        print("init")

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
        ndarray
            an array of simple moving average values for prices, will have length = len(prices)
            but will only have len(prices) - n smas, the rest will be nan's
        """
        smas = np.empty(prices.shape)
        smas[:n] = np.nan # Default the first n values to be nan
        cumsum = np.cumsum(prices)
        smas[n:] = (cumsum[n:] - cumsum[:-n]) / n # Get the smas
        return smas
    
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
            an array of simple moving average values for prices, will have length = len(prices)
            but will only have len(prices) - n smas, the rest will be nan's
        """
        if weighting_factor is None:
            wf = 2 / (n + 1)
        else:
            wf = weighting_factor
            
        smas = np.empty(prices.shape)
        smas[:n] = np.nan # Default the first n values to be nan
        cumsum = np.cumsum(prices)
        smas[n:] = (cumsum[n:] - cumsum[:-n]) / n # Get the smas

        emas = np.empty(prices.shape)
        emas[:n] = np.nan # Default the first n values to be nan
        emas[n] = smas[n]
        # Calculate emas using prices and smas
        for i in range(n + 1, len(smas)):
            emas[i] = (prices[i] - emas[i-1]) * wf + emas[i-1]

        return emas
    
    # TODO: finish implementing
    def moving_average_convergence_divergence(self, prices, n_lt=26, n_st=12):
        """Get the Moving Average Convergence Divergence (MACD) of the prices using n as the period.

        MACD is a trend indicator that measures the relationship between the short term and long term
        exponential moving averages of prices.

        """
        pass

    # TODO: test
    def std_dev(self, prices):
        """Get the standard deviation of the prices

        Standard deviation is a classic volatility technical indicator.

        Parameters
        ----------
        prices : ndarray
            numpy array of prices to get the standard deviation from

        Returns
        -------
        float
            the standard deviation of prices
        """
        return np.std(prices)
    
    # TODO: test
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
            three ndarray's, one with the lower bollinger band, the sma, and one with the upper bollinger band
        """
        sma = self.simple_moving_average(prices, n)
        std_dev = self.std_dev(prices)
        return (sma - 2*std_dev, sma, sma + 2*std_dev)