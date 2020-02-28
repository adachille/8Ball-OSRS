import pandas as pd
from data.runescape_services_api import OldSchoolGEAPIInterface

if __name__ == "__main__":
    # Instantiate our Grand Exchange API Interface
    ge_api = OldSchoolGEAPIInterface()

    # refreshes the item ids csv
    ge_api.get_and_save_item_ids_to_csv('item_ids.csv') 
    item_ids = pd.read_csv('item_ids.csv')
    print(item_ids.shape)

    # Test the get_item_details method
    for item_id in item_ids.id[:10]:
        item_details = ge_api.get_item_details(item_id)
        print(item_details['name'], item_details['current'])