import pytest
import numpy as np
import pandas as pd
from manual_portfolio_allocator import ManualPortfolioAllocator

class TestManualPortfolioAllocator: 
    def test_get_portfolio_value(self):
        test_portfolio = {-1: (1, 1000), 2: (500, 3)}
        mpa = ManualPortfolioAllocator(test_portfolio)
        expected_portfolio_value = 1*1000 + 500*3
        actual_portfolio_value = mpa.portfolio_value
        assert actual_portfolio_value == expected_portfolio_value

    def test_pick_new_allocations(self):
        test_portfolio = {-1: (1, 1000), 2: (500, 3)}
        test_pred_prices = {2: 550}
        mpa = ManualPortfolioAllocator(test_portfolio)

        new_allocations = mpa.pick_new_allocations(test_pred_prices)
        assert type(new_allocations) == dict
        assert new_allocations[-1] == 0
        assert new_allocations[2] == 5
