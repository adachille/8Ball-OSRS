import requests
import pandas as pd
import time

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

    # TODO: Testing
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

    # TODO: Testing
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
        r = requests.get(self.BASE_URL + "/api/catalogue/items.json", 
            params={"category": 1, "alpha": starting_char, "page": page})
        r.raise_for_status()
        return r.json()["items"]

    # TODO: testing       
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

        # Iterate through each starting character and collect id's for each page under that character
        for char in STARTING_CHARS:
            # print(f"Getting items that begin with char: {char}") # Debug
            no_items_left = False
            page = 1
            while not no_items_left:
                try:
                    # Get new items and add them into the array
                    new_items = self.get_paginated_items_details(char, page)
                    if len(new_items) == 0:
                        no_items_left = True
                    else:
                        for item in new_items:
                            item_ids.append({"id": item["id"], "name": item["name"]})
                        page += 1
                    
                    # This is essential, as the api returns a misformed JSON if requests come in to fast
                    time.sleep(5) # TODO: investigate this issue further
                except Exception as e:
                    # This except is triggered when the issue discussed above occurs
                    print('______________')
                    print(char, page)
                    print(e)
                    print('______________')
                    no_items_left = True

        if n_items != len(item_ids):
            print(f"WARNING: {n_items} in DB, only {len(item_ids)} written.")

        # Create a csv for the item ids
        item_ids = pd.DataFrame(item_ids)
        item_ids.to_csv(filename, index=False)