import pytest
import numpy as np
import pandas as pd
from manual_price_predictor import ManualPricePredictor

class TestManualPricePredictor: 
    def test_predict_returns(self):
        mpp = ManualPricePredictor()
        test_id = 1

        ## Check required features ##
        assert "price" in mpp.required_features
        assert "bb" in mpp.required_features

        ## Test Manual Price Predictor Behavior ##
        # Given cur_price > upper bollinger band, our manual price predictor expects increase in
        # price by 5%
        test_cur_price = 65
        test_item_csv = pd.DataFrame(data={"price": [test_cur_price], "lbb": [20], "ubb": [60]})
        expected_pred_prices = {test_id: test_cur_price * .95}
        actual_pred_prices = mpp.predict_new_prices([(test_id, test_item_csv)])
        assert type(actual_pred_prices) == dict
        assert expected_pred_prices[test_id] == actual_pred_prices[test_id]

        # Given cur_price < lower bollinger band, our manual price predictor expects decrease in
        # price by 5%
        test_cur_price = 15
        test_item_csv["price"][test_id] = test_cur_price
        expected_pred_prices = {test_id: test_cur_price * 1.05}
        actual_pred_prices = mpp.predict_new_prices([(test_id, test_item_csv)])
        assert expected_pred_prices[test_id] == actual_pred_prices[test_id]

        # If above cases aren't met, our manual price predictor assumes a stable price
        test_cur_price = 40
        test_item_csv["price"][test_id] = test_cur_price
        expected_pred_prices = {test_id: test_cur_price * 1.00}
        actual_pred_prices = mpp.predict_new_prices([(test_id, test_item_csv)])
        assert expected_pred_prices[test_id] == actual_pred_prices[test_id]