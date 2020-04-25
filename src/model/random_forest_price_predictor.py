from model.price_predictor import PricePredictor

class RandomForestPricePredictor(PricePredictor):   
    """
    A Price Predictor that uses a random forest machine learner for predicting new prices. 

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
    def __init__(self):
        required_features = ["price", "sma", "ema", "rsi", "moving_std_dev", "bb"] # Requires prices data and bollinger bands
        self.model = None
        super().__init__(required_features) # sets self.required_features to required_features
    
    def train_model(self, item_features_tuples, validation_size=0.2):
        """Train the model using the item_features_tuples

        Parameters
        ----------
        item_features_tuples : list(tuple(int, pd.DataFrame))
            list of tuples, where each tuple has an item id and its price and feature data over
            time in the form of a pandas DataFrames, train/validate on these
        validation_size : float
            the portion of rows to use as validation. Between 0 and 1

        """
        pass

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
        pred_prices = {}
        
        return pred_prices