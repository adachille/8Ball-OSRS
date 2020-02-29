import pytest
import os
import pandas as pd
import requests
from runescape_services_api import OldSchoolGEAPIInterface

class TestOldSchoolGEAPIInterface: 
    def test_get_item_details_gets_cannonball(self):
        api_interface = OldSchoolGEAPIInterface()
        cannonball_id = 2
        cannonball_details = api_interface.get_item_details(cannonball_id)
        assert type(cannonball_details) == dict
        assert cannonball_details['name'] == "Cannonball"

    def test_get_item_details_fails_on_bad_id(self):
        api_interface = OldSchoolGEAPIInterface()
        bad_id = -1
        with pytest.raises(Exception) as excep_info:
            api_interface.get_item_details(bad_id)
        print(excep_info.type)
        assert excep_info.type == requests.exceptions.HTTPError

    def test_get_number_of_items(self):
        api_interface = OldSchoolGEAPIInterface()
        assert api_interface.get_number_of_items() > 0
    
    def test_get_paginated_items_details_returns_items(self):
        api_interface = OldSchoolGEAPIInterface()
        item_details = api_interface.get_paginated_items_details(starting_char="a", page="1")
        assert type(item_details) == list
        assert len(item_details) > 0
    
    def test_get_paginated_items_details_returns_empty_list_on_bad_input(self):
        api_interface = OldSchoolGEAPIInterface()
        item_details = api_interface.get_paginated_items_details(starting_char="2msdkn", page="1")
        assert type(item_details) == list
        assert len(item_details) == 0

        item_details = api_interface.get_paginated_items_details(starting_char="a", page=1000)
        assert type(item_details) == list
        assert len(item_details) == 0
    
    # This is commented out as it takes a ton of time to run and it's a sketchy test that
    # could fail because of the api, not the code itself
    def test_get_and_save_item_ids_to_csv(self):
        api_interface = OldSchoolGEAPIInterface()
        api_interface.get_and_save_item_ids_to_csv("test.csv")
        assert len(pd.read_csv("test.csv")) > 0
        os.remove("test.csv")