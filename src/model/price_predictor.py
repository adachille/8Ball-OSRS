from abc import ABC, abstractmethod

class PricePredictor:   
    """
    An abstract class that all Price Predictors must follow. A Price Predictor takes defines a set
    of features it needs and then uses those features for each item to predict their future price

    ...

    Attributes
    ----------
    required_features
        Constant set of feature_names that will need to be in the item_csv's 

    Methods
    -------
    predict_new_prices(item_features_tuples)
        Get the estimated prices for the next timestamp for each item

    """
    def __init__(self, required_features):
        self.required_features = required_features # passed in by classes implementing this class
        super().__init__()
    
    @abstractmethod
    def predict_new_prices(self, item_features_tuples):
        """Get the estimated prices for the next timestamp for each item using the features in its 
        item_csv.

        Parameters
        ----------
        item_features_tuples : list(tuple(int, pd.DataFrame))
            list of tuples, where each tuple has an item id and its price and feature data over
            time in the form of a pandas DataFrames

        Returns
        -------
        dict<int, int>
            dict of the item id keys and their estimated new price
        """
        pass