from abc import ABC, abstractmethod
import numpy as np

class PortfolioAllocator:   
    """
    An abstract class that all Portfolio Allocator classes must follow. A Portfolio Allocator 
    determines how best to allocate a given portfolio, using estimated future prices along with
    other information such as risk tolerance, buy limits, etc.

    ...

    Attributes
    ----------
    portfolio : pd.DataFrame
        A dataframe with item_id's as indices and price and amount as columns

    Methods
    -------
    pick_new_allocations(pred_prices)
        Pick the new portfolio allocations for the next timestamp
    set_portfolio(portfolio)
        Set a portfolio attribute

    """
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.portfolio_value = self.get_portfolio_value()
        super().__init__()

    @abstractmethod
    def pick_new_allocations(self, pred_prices):
        """Pick the new portfolio allocations for the next timestamp using the predicted future
        (next timestamp) prices.

        Parameters
        ----------
        pred_prices : dict<int, int>
            dict of the item id keys and their estimated new price
        
        Returns
        -------
        dict
            A dict of item_id's to item amounts, represents new allocations
        """
        pass

    def set_portfolio(self, portfolio):
        """Set the portfolio attribute.

        Parameters
        ----------
        portfolio : pd.DataFrame
            A dataframe with item_id's as indices and price and amount as columns

        """
        self.portfolio = portfolio
        self.portfolio_value = self.get_portfolio_value()

    def get_portfolio_value(self):
        """Get the value of the inputted portfolio.
        
        Returns
        -------
        int
            value of the portfolio

        """
        return (self.portfolio["price"] * self.portfolio["amount"]).sum()
