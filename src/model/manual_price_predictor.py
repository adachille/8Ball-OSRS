from price_predictor import PricePredictor
from features.extractors_technical_indicators import ExtractorTechnicalIndicators

class ManualPricePredictor(PricePredictor):   
    """
    An abstract class that all Price Predictors must follow. A Price Predictor takes in item_csv's and has the 
    ability to estimate upcoming returns and determine how best to allocate a portfolio given 
    these estimated upcoming returns (this data can also be accompanied with risk estimateions, or
    other information)

    ...

    Attributes
    ----------
    required_features
        Constant set of feature_names that will need to be in the item_csv's 

    Methods
    -------
    predict_new_prices(item_csv_tuples)
        Get the estimated prices for the next timestamp for each item

    """
    def __init__(self):
        required_features = ["prices", "lbb", "ubb"]
        super().__init__(required_features) # sets self.portfolio to starting_portfolio
    
    def predict_new_prices(self, item_csv_tuples):
        """Get the estimated prices for the next timestamp for each item using the features in its 
        item_csv.

        Parameters
        ----------
        item_csv_tuples : list(tuple(int, pd.DataFrame))
            list of tuples, where each tuple has an item id and its price and feature data over
            time in the form of a pandas DataFrames

        Returns
        -------
        dict<int, float>
            dict of the item id keys and their estimated new price
        """
        pred_prices = {}
        # Go through each item and predict the returns
        for item_id, item_csv in item_csv_tuples:
            prices = item_csv["prices"]

            ## Our Manual Strategy will be a simple handmade decision tree ##
            lbb = item_csv["lbb"]
            ubb = item_csv["ubb"]
            # If the price dips below the lower bollinger band, assume a price increase is coming up
            if prices.iloc[-1] < lbb.iloc[-1]: 
                pred_prices[item_id] = prices.iloc[-1] * 1.05
            # If the price goes above the upper bollinger band, assume a price decrease is coming up
            elif prices.iloc[-1] > ubb.iloc[-1]:
                pred_prices[item_id] = prices.iloc[-1] * .95
            # If nothing else, assume a constant price
            else:
                pred_prices[item_id] = prices.iloc[-1]
        return pred_prices