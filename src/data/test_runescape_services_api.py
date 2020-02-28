import pytest
import requests
from runescape_services_api import OldSchoolGEAPIInterface, get_all_item_ids

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

def test_get_all_item_ids():
    item_ids = get_all_item_ids()
    assert type(item_ids) == list
    assert len(item_ids) > 0