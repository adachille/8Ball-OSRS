import pytest
import numpy as np
import pandas as pd
from manual_strategy import ManualStrategy

class TestManualStrategy: 
    def test_predict_returns(self):
        # Simulate a situation where we own 10 items with id = 1 and cur_price = 65
        test_id = 1
        test_portfolio = [{test_id: 10*65}]
        ms = ManualStrategy(test_portfolio)

        # Given the cur_price being higher than the upper bollinger band, our manual strategy 
        # Create the item features csv
        test_cur_price = 65
        test_item_csv = pd.DataFrame(data={"prices": [test_cur_price], "lbb": [20], "ubb": [60]})
        # expects a decrease of 5% of price.
        expected_pred_returns = {test_id: -0.05}
        actual_pred_returns = ms.predict_returns([(test_id, test_item_csv)])

        assert type(actual_pred_returns) == dict
        assert expected_pred_returns[test_id] == actual_pred_returns[test_id]

        # Trying the same experiment but with the cur_price being lower than the lower bollinger 
        # band, our manual strategy expects an increase of 5% of price
        test_cur_price = 15
        test_item_csv["prices"][test_id] = test_cur_price
        # expects an increase of 5% of price.
        expected_pred_returns = {test_id: 0.05}
        actual_pred_returns = ms.predict_returns([(test_id, test_item_csv)])
        assert expected_pred_returns[test_id] == actual_pred_returns[test_id]

        # Trying the same experiment but with the cur_price being b/w the bollinger bands,
        # our manual strategy expects a steady price
        test_cur_price = 40
        test_item_csv["prices"][test_id] = test_cur_price
        expected_pred_returns = {test_id: 0.00}
        actual_pred_returns = ms.predict_returns([(test_id, test_item_csv)])
        assert expected_pred_returns[test_id] == actual_pred_returns[test_id]