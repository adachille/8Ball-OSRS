import pytest
import os
import pandas as pd
import requests
from runescape_services_api import OldSchoolGEAPIInterface

class TestOldSchoolGEAPIInterface: 
    @pytest.mark.api
    def test_get_item_details_gets_cannonball(self):
        api_interface = OldSchoolGEAPIInterface()
        cannonball_id = 2
        cannonball_details = api_interface.get_item_details(cannonball_id)
        assert type(cannonball_details) == dict
        assert cannonball_details['name'] == "Cannonball"
    
    @pytest.mark.api
    def test_get_item_details_fails_on_bad_id(self):
        api_interface = OldSchoolGEAPIInterface()
        bad_id = -1
        with pytest.raises(Exception) as excep_info:
            api_interface.get_item_details(bad_id)
        print(excep_info.type)
        assert excep_info.type == requests.exceptions.HTTPError

    @pytest.mark.api
    def test_get_number_of_items(self):
        api_interface = OldSchoolGEAPIInterface()
        assert api_interface.get_number_of_items() > 0
    
    @pytest.mark.api
    def test_get_paginated_items_details_returns_items(self):
        api_interface = OldSchoolGEAPIInterface()
        item_details = api_interface.get_paginated_items_details(starting_char="a", page="1")
        assert type(item_details) == list
        assert len(item_details) > 0
    
    @pytest.mark.api
    def test_get_paginated_items_details_returns_empty_list_on_bad_input(self):
        api_interface = OldSchoolGEAPIInterface()
        item_details = api_interface.get_paginated_items_details(starting_char="2msdkn", page="1")
        assert type(item_details) == list
        assert len(item_details) == 0

        item_details = api_interface.get_paginated_items_details(starting_char="a", page=1000)
        assert type(item_details) == list
        assert len(item_details) == 0

    @pytest.mark.api
    def test_get_item_price_history(self):
        api_interface = OldSchoolGEAPIInterface()
        cannonball_id = 2
        item_price_history = api_interface.get_item_price_history(cannonball_id)
        assert type(item_price_history) == dict

        timestamps = list(item_price_history.keys())
        assert len(timestamps) == 180
        prices = list(item_price_history.values())
        assert len(prices) == 180

    @pytest.mark.api
    def test_get_item_price_history_fails_on_bad_id(self):
        api_interface = OldSchoolGEAPIInterface()
        bad_id = -1
        with pytest.raises(Exception) as excep_info:
            api_interface.get_item_details(bad_id)
        print(excep_info.type)
        assert excep_info.type == requests.exceptions.HTTPError
    
    @pytest.mark.api
    def test_update_price_history_csv(self):
        api_interface = OldSchoolGEAPIInterface()
        cannonball_id = 2
        api_interface.update_price_history_csv(cannonball_id, "./")
        cannonball_price_history = pd.read_csv(f"./{cannonball_id}_price_history.csv")
        assert len(cannonball_price_history.index) == 180
        os.remove(f"./{cannonball_id}_price_history.csv")
        
    @pytest.mark.api
    def test_update_price_history_csv_fails_on_bad_id(self):
        api_interface = OldSchoolGEAPIInterface()
        bad_id = -1
        with pytest.raises(Exception) as excep_info:
            api_interface.get_item_details(bad_id)
        print(excep_info.type)
        assert excep_info.type == requests.exceptions.HTTPError