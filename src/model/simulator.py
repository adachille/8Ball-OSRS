import numpy as np
import pandas as pd
from enum import Enum
from manual_price_predictor import ManualPricePredictor
from manual_portfolio_allocator import ManualPortfolioAllocator
from features.extractors_technical_indicators import ExtractorTechnicalIndicators

class PricePredictorType(Enum):
    MANUAL = 1
class PortfolioAllocatorType(Enum):
    MANUAL = 1

# TODO: create an enum for data features
class Simulator:   
    """
    A class that is used to run simulations with historical price/feature data and pairs of 
    PricePredictor's and PortfolioAllocator's.
    ...

    Attributes
    ----------
    ppt : PricePredictorType
        specificies which PricePredictor class to use
    pat : PortfolioAllocatorType
        specificies which PortfolioAllocator class to use

    Methods
    -------
    extract_features_from_price_history()
        Extracts and returns feature data from the price_history_tuples
    backtest()
        Backtests the ppt, pat pair using the price_history_tuples and given starting_portfolio

    """
    def __init__(self, starting_portfolio, ppt=PricePredictorType.MANUAL, 
        pat=PortfolioAllocatorType.MANUAL):
        self.portfolio = starting_portfolio
        super()
        
        if ppt == PricePredictorType.MANUAL:
            self.ppt = ManualPricePredictor()
        else:
            raise Exception("Invalid PricePredictorType, check the PricePredictorType class to \
                see available values")
        
        if pat == PortfolioAllocatorType.MANUAL:
            self.pat = ManualPortfolioAllocator(self.portfolio)
        else:
            raise Exception("Invalid PortfolioAllocatorType, check the PortfolioAllocatorType \
                class to see available values")

    def extract_features_from_price_history(self, price_history_tuples):
        """ Extracts and returns feature data from the price_history_tuples
        
        Parameters
        ----------
        price_history_tuples : list(tuple(int, pd.DataFrame))
            list of tuples, where each tuple has an item id and its price data over time in the form
            of a pandas DataFrames

        Returns
        -------
        item_features_tuples : list(tuple(int, pd.DataFrame))
            list of tuples, where each tuple has an item id and its price and feature data over
            time in the form of a pandas DataFrames

        """
        item_features_tuples = []
        req_feats = self.ppt.required_features
        eti = ExtractorTechnicalIndicators()

        # Go through each item and get its item_feature_tuple
        for item_id, price_history in price_history_tuples:
            prices = price_history["prices"]
            
            # Get the features needed for the chosen PricePredictor
            feature_series = []
            if "sma" in req_feats:
                feature_series.append(eti.simple_moving_average(prices)) 
            if "ema" in req_feats:
                feature_series.append(eti.exponential_moving_average(prices))
            if "rsi" in req_feats:
                feature_series.append(eti.rsi(prices))
            if "moving_std_dev" in req_feats:
                feature_series.append(eti.moving_std_dev(prices))
            if "bb" in req_feats:
                lbb, sma, ubb = eti.bollinger_bands(prices)
                feature_series.append(lbb)
                feature_series.append(sma)
                feature_series.append(ubb)
            item_features_df = pd.concat([prices] + feature_series, axis=1) # add prices and feature data
            item_features_tuples.append((item_id, item_features_df))

        return item_features_tuples

    def backtest(self, price_history_tuples):
        """

        Parameters
        ----------
        price_history_tuples : list(tuple(int, pd.DataFrame))
            list of tuples, where each tuple has an item id and its price data over time in the form
            of a pandas DataFrames
        portfolio : map
            A dict of item_id's to allocation tuples (item_value, item_amount)
        
        Returns
        -------
        
        """
        item_features_tuples = self.extract_features_from_price_history(price_history_tuples)
        pass
