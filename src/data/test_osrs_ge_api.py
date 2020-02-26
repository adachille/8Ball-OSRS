import pytest
from osrs_ge_api import OldSchoolGEAPIInterface, get_all_item_ids

class TestOldSchoolGEAPIInterface: 
    def test_get_item_details(self):
        api_interface = OldSchoolGEAPIInterface()
        cannonball_id = 2
        cannonball_details = api_interface.get_item_details(cannonball_id)
        assert type(cannonball_details) == dict
        assert cannonball_details['name'] == "Cannonball"

def test_get_all_item_ids():
    item_ids = get_all_item_ids()
    assert type(item_ids) == list
    assert len(item_ids) > 0