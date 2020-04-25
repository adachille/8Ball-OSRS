import numpy as np
import pandas as pd
from enum import Enum
from model.manual_price_predictor import ManualPricePredictor
from model.manual_portfolio_allocator import ManualPortfolioAllocator
from model.features.extractors_technical_indicators import ExtractorTechnicalIndicators
from tqdm import tqdm

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
    pp : PricePredictorType
        specificies which PricePredictor class to use
    pa : PortfolioAllocatorType
        specificies which PortfolioAllocator class to use

    Methods
    -------
    extract_features_from_price_history()
        Extracts and returns feature data from the price_history_tuples
    backtest()
        Backtests the pp, pa pair using the price_history_tuples and given starting_portfolio
    portfolio : pd.DataFrame
        A dataframe with item_id's as indices and item_value and item_amount as columns

    """
    def __init__(self, starting_portfolio, pp=PricePredictorType.MANUAL, 
        pa=PortfolioAllocatorType.MANUAL):
        self.portfolio = starting_portfolio
        super()
        
        if pp == PricePredictorType.MANUAL:
            self.pp = ManualPricePredictor()
        else:
            raise Exception("Invalid PricePredictorType, check the PricePredictorType class to \
                see available values")
        
        if pa == PortfolioAllocatorType.MANUAL:
            self.pa = ManualPortfolioAllocator(self.portfolio)
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
        req_feats = self.pp.required_features
        eti = ExtractorTechnicalIndicators()
        # Go through each item and get its item_feature_tuple
        for item_id, price_history in price_history_tuples:
            prices = price_history["price"]
            
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
        
        Returns
        -------
        pd.Series
            series of portfolio values over time
        
        """
        port_vals = []

        # Get feature data
        item_features_tuples = self.extract_features_from_price_history(price_history_tuples)
        item_ids, item_features_dfs = map(list, zip(*item_features_tuples))

        # First drop the rows with na, as they can't be used
        for df in item_features_dfs:
            df.dropna(axis=0, inplace=True)
        
        # TODO: figure out a way of doing this that won't cause issues if different item_csvs 
        # have different ranges in price history.
        dates = item_features_tuples[0][1].index
        for date in tqdm(dates):
             # Get the item_feature_data up to the current date
            data_up_to_data = [(id, df.loc[:date]) for id, df in zip(item_ids, item_features_dfs)]

            # Update the portfolio prices to the current day
            for id, df in data_up_to_data:
                self.portfolio["price"].at[id] = df["price"].iloc[-1]
            self.pa.set_portfolio(self.portfolio)
            
            # Record portfolio value
            port_vals.append(self.pa.portfolio_value)

            # Predict prices and get new allocations
            pred_prices = self.pp.predict_new_prices(data_up_to_data)
            pred_prices[-1] = 1 # -1 is id for gold, always stays at value of 1
            new_allocations = self.pa.pick_new_allocations(pred_prices)
            
            for id, amount in new_allocations.items():
                self.portfolio["amount"].at[id] = amount

        return pd.Series(port_vals).rename("port_vals")