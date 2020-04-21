import pytest
import numpy as np
import pandas as pd
from simulator import Simulator, PortfolioAllocatorType, PricePredictorType
from manual_price_predictor import ManualPricePredictor
from manual_portfolio_allocator import ManualPortfolioAllocator

class TestSimulator: 
    def test_simulator_init(self):
        test_starting_portfolio = {-1: (1, 1000), 2: (500, 3)}
        sim = Simulator(test_starting_portfolio)
        assert type(sim.ppt) == ManualPricePredictor
        assert type(sim.pat) == ManualPortfolioAllocator
        assert sim.pat.portfolio == test_starting_portfolio

    def test_extract_features_from_price_history(self):
        test_starting_portfolio = {-1: (1, 1000), 2: (50, 3)}
        sim = Simulator(test_starting_portfolio)

        test_prices_df = pd.DataFrame([10, 20, 30, 40, 50], columns=["prices"])
        test_price_history_tuples = [(2, test_prices_df)]
        item_feature_tuples = sim.extract_features_from_price_history(test_price_history_tuples)

        # item_feature_tuples should include, prices, smas, and lower and upper bollinger bands,
        # however, because price history is short, they should all be nans
        expected_features = pd.Series([np.nan, np.nan, np.nan, np.nan, np.nan])

        pd.testing.assert_series_equal(item_feature_tuples[0][1]["prices"], test_prices_df["prices"])
        pd.testing.assert_series_equal(item_feature_tuples[0][1]["lbb"], 
            expected_features.rename("lbb"))
        pd.testing.assert_series_equal(item_feature_tuples[0][1]["sma"], 
            expected_features.rename("sma"))
        pd.testing.assert_series_equal(item_feature_tuples[0][1]["ubb"],
            expected_features.rename("ubb"))