import requests
import pandas as pd
from pathlib import Path
import time

# TODO: make this file return information in a more specific way, needs a stricter interface
class OldSchoolGEAPIInterface:   
    """
    A class used to interaact with the OSRS Services Grand Exchange API.

    ...

    Attributes
    ----------
    BASE_URL : str
        The base services url that all api calls will need as a prefix

    Methods
    -------
    get_item_details(item_id)
        Gets the details of an item with the id item_id.
    get_number_of_items()
        Gets the total number of items in the runescape services GE Database
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
            A dictionary containing the details of the item
        """
        r = requests.get(self.BASE_URL + "/api/catalogue/detail.json", params={"item": item_id})
        r.raise_for_status()
        return r.json()['item'] 

    def get_number_of_items(self):
        """Gets the total number of items in the runescape services GE Database
        
        Raises
        ----------
        requests.exceptions.HTTPError:
            If the request got an error status

        Returns
        -------
        int
            the total number of items in the runescape services GE Database
        """
        # API requires letter and page
        r = requests.get(self.BASE_URL + "/api/catalogue/items.json", params={"category": 1, "alpha": "a", "page": 1})
        r.raise_for_status()
        return r.json()["total"]

    def get_paginated_items_details(self, starting_char="a", page=1):
        """Retrieves 12 items given pagination parameters

        Parameters
        ----------
        starting_char : str
            The letter that all items must start with in the results. Note, use "%23" 
            to get items that start with a number
        page : int
            The page number for the search, each page brings 12 results

        Raises
        ----------
        requests.exceptions.HTTPError:
            If the request got an error status

        Returns
        -------
        dict
            a list containing dictionaries of the details of 12 items
        """
        # API requires letter and page
        r = requests.get(self.BASE_URL + f"/api/catalogue/items.json?category=1&alpha={starting_char}&page={page}")
        r.raise_for_status()
        return r.json()["items"]

    # TODO: Figure out a way to test this function       
    def get_and_save_item_ids_to_csv(self, filename):
        """Saves the id's and associated names of every item in the runescape services GE Database to a
        CSV with filename passed in.

        Parameters
        ----------
        filename : str
            The file name of the CSV to save the id's and names to
        """
        item_ids = []
        STARTING_CHARS = ["%23", # get items that start with a number
                        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 
                        "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                        "u", "v", "w", "x", "y", "z"
                        ]
        n_items = self.get_number_of_items()

        # JANK ALERT: We force the process to sleep every sleep_interval seconds for 
        # sleep_time seconds because the services api starts returning misformed JSONs 
        # if too many requests happen too quickly.
        sleep_counter = 1  # Tracks when to sleep
        sleep_interval = 5 # Every 5 iterations, sleep. Prevents api from returning misformed api
        sleep_time = 10    # Time to sleep every n iterations

        # Iterate through each starting character and collect id's for each page under that character
        for char in STARTING_CHARS:
            print(f"Getting items that begin with char: {char}") # Debug
            no_items_left = False
            page = 1
            while not no_items_left:
                try:
                    # Get new items and add them into the array
                    new_items = self.get_paginated_items_details(char, page)
                    if len(new_items) == 0:
                        no_items_left = True
                    else:
                        page += 1
                        for item in new_items:
                            item_ids.append({"id": item["id"], "name": item["name"]})
                    
                    # Sleep after sleep_interval iterations
                    if sleep_counter % sleep_interval == 0:
                        time.sleep(sleep_time)
                except Exception as e:
                    # This except is triggered when the issue discussed above occurs,
                    # just let it rest for a minute
                    print('______________')
                    print(char, page)
                    print(e)
                    print('______________')
                    time.sleep(60)
                
                sleep_counter += 1


        if n_items != len(item_ids):
            print(f"WARNING: {n_items} in DB, only {len(item_ids)} written.")

        # Create a csv for the item ids
        item_ids = pd.DataFrame(item_ids)
        item_ids.to_csv(filename, index=False)
    
    def get_item_price_history(self, item_id):
        """Gets the item's price history for the last 6 months

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
            A dictionary with timestamp keys for the last 6 months and prices as values
        """
        r = requests.get(self.BASE_URL + f"/api/graph/{item_id}.json")
        r.raise_for_status()
        return r.json()['daily']
    
    # TODO: test
    def update_price_history_csv(self, item_id, datapath):
        """ Takes in an item_id and gets the item's price history for the last 6 months. It then performs a union between
        the new price history data and the price history data in the csv associated with the item.

        Parameters
        ----------
        item_id : int
            Id of an item

        Raises
        ----------
        requests.exceptions.HTTPError:
            If the request got an error status - likely due to an invalid id
        """
        # Get api data
        price_history = self.get_item_price_history(item_id)

        # Get a DataFrame from api data
        timestamps = list(price_history.keys())
        prices = list(price_history.values())
        prices_df = pd.DataFrame(data={"timestamps": timestamps, "prices": prices})
        # Convert string timestamps to proper pandas timestamps
        prices_df["timestamps"] = pd.to_numeric(prices_df["timestamps"]) / 1000 # convert to seconds
        # Convert to dates
        prices_df["dates"] = pd.to_datetime(prices_df["timestamps"], unit='s')
        prices_df = prices_df.set_index("dates")

        # Get old csv for item and add these dates to it
        # item_csv_path = Path("./runescape_services")
        # print(path.parent)
        try:
            old_prices_df = pd.read_csv(f"{datapath}{item_id}_price_history.csv", index_col="dates", parse_dates=["dates"])
            # only get the rows that have a date after the last date of old_prices_df
            prices_df = prices_df[prices_df.index > old_prices_df.index[-1]]
            new_prices_df = pd.concat([old_prices_df, prices_df])
            new_prices_df.to_csv(f"{datapath}{item_id}_price_history.csv")
        except FileNotFoundError as e:
            print("Preexisting price_history file not found, creating one")
            prices_df.to_csv(f"{datapath}{item_id}_price_history.csv")