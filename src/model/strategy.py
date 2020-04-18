from abc import ABC, abstractmethod
# TODO: maybe add a "required_features" attribute that dictates what information the strategy 
# needs, and this higher level Strategy class can collect the proper data OR the engine could
# collect the data and pass it into the strategy
class Strategy:   
    """
    An abstract class that all Strategies must follow. A Strategy takes in item_csv's and has the 
    ability to estimate upcoming returns and determine how best to allocate a portfolio given 
    these estimated upcoming returns (this data can also be accompanied with risk estimateions, or
    other information)

    ...

    Attributes
    ----------
    portfolio : map
        This is a map of item_id's to 

    Methods
    -------
    predict_returns(item_csvs)
        Get the estimated percent returns for the next timestamp for each item using its item_csv

    """
    def __init__(self, portfolio):
        self.portfolio = portfolio
        super().__init__()
    
    @abstractmethod
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
        map<int, float>
            map of the item id keys and their estimated price changes for the next timestamp.
        """
        pass