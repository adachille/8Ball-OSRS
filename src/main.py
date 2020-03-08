import pandas as pd
from datetime import datetime
from data.runescape_services_api import OldSchoolGEAPIInterface

if __name__ == "__main__":
    # Instantiate our Grand Exchange API Interface
    ge_api = OldSchoolGEAPIInterface()

    # # refreshes the item ids csv
    # ge_api.get_and_save_item_ids_to_csv('item_ids.csv') 

    # Get item ids
    item_ids = pd.read_csv('item_ids.csv')
    print(item_ids.shape)
    cannonball_id = item_ids[item_ids['name'] == 'Cannonball'].id.values[0]

    # # Test the get_item_details method
    item_details = ge_api.get_item_details(cannonball_id)
    print(item_details)

    # Get the last 6 months of data for Cannonballs
    cannonball_price_history = ge_api.get_item_price_history(cannonball_id)
    timestamps = list(cannonball_price_history.keys())
    prices = list(cannonball_price_history.values())
    prices_df = pd.DataFrame(data={"timestamps": timestamps, "prices": prices})
    # Convert string timestamps to proper pandas timestamps
    prices_df["timestamps"] = pd.to_numeric(prices_df["timestamps"]) / 1000 # convert to seconds

    # Convert to dates
    prices_df["dates"] = pd.to_datetime(prices_df["timestamps"], unit='s')
    print(prices_df)
