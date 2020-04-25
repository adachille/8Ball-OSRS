import pytest
import numpy as np
import pandas as pd
from simulator import Simulator, PortfolioAllocatorType, PricePredictorType
from model.manual_price_predictor import ManualPricePredictor
from model.manual_portfolio_allocator import ManualPortfolioAllocator

class TestSimulator: 
    def test_simulator_init(self):
        test_starting_portfolio = pd.DataFrame(data=[[1, 1000], [500, 3]], 
            columns=["price", "amount"],
            index=[-1, 2])
        sim = Simulator(test_starting_portfolio)
        assert type(sim.pp) == ManualPricePredictor
        assert type(sim.pa) == ManualPortfolioAllocator
        assert sim.pa.portfolio.equals(test_starting_portfolio)

    def test_extract_features_from_price_history(self):
        test_starting_portfolio = pd.DataFrame(data=[[1, 1000], [50, 3]], 
            columns=["price", "amount"],
            index=[-1, 2])
        sim = Simulator(test_starting_portfolio)

        test_prices_df = pd.DataFrame([10, 20, 30, 40, 50], columns=["price"])
        test_price_history_tuples = [(2, test_prices_df)]
        item_feature_tuples = sim.extract_features_from_price_history(test_price_history_tuples)

        # item_feature_tuples should include, prices, smas, and lower and upper bollinger bands,
        # however, because price history is short, they should all be nans
        expected_features = pd.Series([np.nan, np.nan, np.nan, np.nan, np.nan])

        pd.testing.assert_series_equal(item_feature_tuples[0][1]["price"], test_prices_df["price"])
        pd.testing.assert_series_equal(item_feature_tuples[0][1]["lbb"], 
            expected_features.rename("lbb"))
        pd.testing.assert_series_equal(item_feature_tuples[0][1]["sma"], 
            expected_features.rename("sma"))
        pd.testing.assert_series_equal(item_feature_tuples[0][1]["ubb"],
            expected_features.rename("ubb"))
    
    def test_backtest(self):
        test_starting_portfolio = pd.DataFrame(data=[[1, 1000], [1, 0]], 
            columns=["price", "amount"],
            index=[-1, 2])        
        sim = Simulator(test_starting_portfolio)

        # Backtest for an item where the price increases by one each timestep
        test_prices_df = pd.DataFrame(np.ones(100), columns=["price"])
        test_prices_df["price"] = test_prices_df["price"] * (test_prices_df.index + 1)
        test_price_history_tuples = [(2, test_prices_df)]
        port_vals = sim.backtest(test_price_history_tuples)
        assert type(port_vals) == pd.Series
        assert len(port_vals) == 81 # 81 because bollinger bands have default n = 20

        # Backtest for an item where the price crosses the lower bollinger band
        test_prices_df = pd.DataFrame(np.ones(100), columns=["price"])
        test_prices_df["price"] = test_prices_df["price"] * (test_prices_df.index + 1)
        test_prices_df.at[50, "price"] = 10
        test_price_history_tuples = [(2, test_prices_df)]
        port_vals = sim.backtest(test_price_history_tuples)
        assert port_vals.iloc[-1] > port_vals.iloc[0] # Should be a gain in portfolio value