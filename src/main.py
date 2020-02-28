import pandas as pd
from data.runescape_services_api import OldSchoolGEAPIInterface, get_all_item_ids

if __name__ == "__main__":
    # refreshes the item ids csv
    items = get_all_item_ids() 
    item_ids = pd.DataFrame(items).to_csv('item_ids.csv', index=False)
    item_ids = pd.read_csv('item_ids.csv')
    print(item_ids.shape)

    # Test the get_item_details method
    ge_api = OldSchoolGEAPIInterface()
    for item_id in item_ids.id[:10]:
        item_details = ge_api.get_item_details(item_id)
        print(item_details['name'], item_details['current'])