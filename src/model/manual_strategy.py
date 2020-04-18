from strategy import Strategy
from features.extractors_technical_indicators import ExtractorTechnicalIndicators

class ManualStrategy(Strategy):   
    """
    A Manual Strategy, currently just uses bollinger bands as indicators of oversold/overbought items

    ...

    Attributes
    ----------
    portfolio : map
        This is a map of item_id's to allocations (item price * n_items)

    Methods
    -------
    predict_returns(item_csvs)
        Get the estimated percent returns for the next timestamp for each item using its item_csv

    """
    def __init__(self, starting_portfolio):
        super().__init__(starting_portfolio) # sets self.portfolio to starting_portfolio
        self.eti = ExtractorTechnicalIndicators()
    
    def predict_returns(self, item_csv_tuples):
        """Get the estimated percent returns for the next timestamp for each item using its 
        item_csv.

        Parameters
        ----------
        item_csv_tuples : list(tuple(int, pd.DataFrame))
            list of tuples, where each tuple has an item id and its price and feature data over
            time in the form of a pandas DataFrames

        Returns
        -------
        dict<int, float>
            dict of the item id keys and their estimated price changes for the next timestamp.
        """
        pred_returns = {}
        # Go through each item and predict the returns
        for item_id, item_csv in item_csv_tuples:
            prices = item_csv["prices"]

            ## Our Manual Strategy will be a simple handmade decision tree ##
            lbb = item_csv["lbb"]
            ubb = item_csv["ubb"]
            # If the price dips below the lower bollinger band, assume a price increase is coming up
            if prices.iloc[-1] < lbb.iloc[-1]: 
                pred_returns[item_id] = 0.05
            # If the price goes above the upper bollinger band, assume a price decrease is coming up
            elif prices.iloc[-1] > ubb.iloc[-1]:
                pred_returns[item_id] = -0.05
            # If nothing else, assume a constant price
            else:
                pred_returns[item_id] = 0.0
        return pred_returns