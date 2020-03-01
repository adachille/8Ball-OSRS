import pandas as pd
from data.runescape_services_api import OldSchoolGEAPIInterface

if __name__ == "__main__":
    # Instantiate our Grand Exchange API Interface
    ge_api = OldSchoolGEAPIInterface()

    # # refreshes the item ids csv
    # ge_api.get_and_save_item_ids_to_csv('item_ids.csv') 

    # Get item ids
    item_ids = pd.read_csv('item_ids.csv')
    print(item_ids.shape)

    # Test the get_item_details method
    for item_id in item_ids.id[:10]:
        item_details = ge_api.get_item_details(item_id)
        print(item_details['name'], item_details['current'])

    # Get the last 6 months of data for Cannonballs
    cannonball_id = item_ids[item_ids['name'] == 'Cannonball'].id.values[0]
    print('______________')
    print(item_ids[item_ids['name'] == 'Cannonball'])
    print(cannonball_id)
    cannonball_price_history = ge_api.get_item_price_history(cannonball_id)
    print(cannonball_price_history)