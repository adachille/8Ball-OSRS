import requests
import pandas as pd

class OldSchoolGEAPIInterface:
    """
    A class used to interaact with the Old School Runescape Grand Exchange API

    ...

    Attributes
    ----------

    Methods
    -------
    get_item_details(item_id)
        gets the details of an item with the id item_id.
    """
    def __init__(self):
        self.BASE_URL = "http://services.runescape.com/m=itemdb_oldschool" # Base url needed for all requests

    def get_item_details(self, item_id):
        """Gets the details of an item with the id item_id

        Parameters
        ----------
        item_id : int
            Id of an item

        Raises
        ----------
        requests.exceptions.HTTPError:
            If the request got an error status - likely due to an invalid id

        Returns
        -------
        dict
            a dictionary containing the details of the item
        """
        r = requests.get(self.BASE_URL + f"/api/catalogue/detail.json?item={item_id}")
        r.raise_for_status()
        return r.json()['item'] 

# TODO: scary to rely on a single pastebin url, consider how to fix this
def get_all_item_ids():
    item_ids = requests.get("https://pastebin.com/raw/LhxJ7GRG").json()
    return item_ids