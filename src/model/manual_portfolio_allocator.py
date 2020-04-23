from portfolio_allocator import PortfolioAllocator
import pandas as pd

class ManualPortfolioAllocator(PortfolioAllocator):   
    """
    A Price Predictor that has a manually crafted method for predicting new prices. 

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
        Set a new portfolio

    """
    def __init__(self, starting_portfolio):
        super().__init__(starting_portfolio) # sets self.portfolio to starting_portfolio

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
        # TODO: consider moving the gold addition to the Simulator class
        # Get a DataFrame with the portfolio data and new prices
        pred_prices_df = pd.DataFrame(data=pred_prices.values(), index=pred_prices.keys(), 
            columns=["pred_price"])
        df = pd.concat([self.portfolio, pred_prices_df], axis=1)

        # Get the pred return for each item
        df["delta"] = df["pred_price"] - df["price"]
        df["pred_return"] = df["delta"] / df["price"]
        
        # Sort by highest to lowest return
        df.sort_values(by="pred_return", ascending=False, inplace=True)
        
        # Iterate through the items from highest to lowest predicted return, and fully allocate
        # until we run out of money, hold the rest as cash
        money_to_allocate = self.portfolio_value
        i = 0
        new_amounts = {}
        while money_to_allocate > 0:
            row = df.iloc[i]
            item_id = row.name
            new_amounts[item_id] = money_to_allocate // row["price"]

            money_to_allocate -= new_amounts[item_id] * row["price"]
            i += 1

        # Add in 0's for the item id's of items where money is not being allocated
        items_allocated_to = list(new_amounts.keys())
        for item_id in df.index:
            if item_id not in items_allocated_to:
                new_amounts[item_id] = 0

        return new_amounts
