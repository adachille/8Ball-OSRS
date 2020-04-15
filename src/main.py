import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime
from tqdm import tqdm
from api.runescape_services_api import OldSchoolGEAPIInterface
from features.extractors_technical_indicators import ExtractorTechnicalIndicators

if __name__ == "__main__":
    # Instantiate our Grand Exchange API Interface
    ge_api = OldSchoolGEAPIInterface()

    # # refreshes the item ids csv
    # ge_api.get_and_save_item_ids_to_csv('item_ids_04_X_2020.csv') 

    # Get item ids
    item_ids = pd.read_csv('item_ids_04_12_2020.csv')
    print(item_ids.shape)

    # # Test the get_item_details method
    cannonball_id = item_ids[item_ids['name'] == 'Cannonball'].id.values[0]
    item_details = ge_api.get_item_details(cannonball_id)
    print(item_details)

    update_all_prices = True
    if update_all_prices:
        print("Updating items")
        # Update all the price histories
        # JANK ALERT: We force the process to sleep every sleep_interval seconds for 
        # sleep_time seconds because the services api starts returning misformed JSONs 
        # if too many requests happen too quickly.
        sleep_counter = 1  # Tracks when to sleep
        sleep_interval = 5 # Every 5 iterations, sleep. Prevents api from returning misformed api
        sleep_time = 10    # Time to sleep every n iterations

        # Iterate through each starting character and collect id's for each page under that character
        for item_id in tqdm(item_ids["id"].values):
            # Sleep after sleep_interval iterations
            if sleep_counter % sleep_interval == 0:
                time.sleep(sleep_time)

            price_history_updated = False
            attempts = 0
            while not price_history_updated and attempts < 5:
                try:
                    # Update price history
                    ge_api.update_price_history_csv(item_id, "./data/")
                    price_history_updated = True
                except Exception as e:
                    # This except is triggered when the issue discussed above occurs,
                    # just let it rest for a minute
                    print('______________')
                    print("Failed on item_id: ", item_id)
                    print('______________')
                    attempts += 1
                    time.sleep(60)
                
            sleep_counter += 1

    cannonball_price_history = pd.read_csv(f'./data/{cannonball_id}_price_history.csv')
    cannonball_prices = cannonball_price_history['prices'].to_numpy()

    # Plot trend indicators
    extractor_ti = ExtractorTechnicalIndicators()
    smas = extractor_ti.simple_moving_average(cannonball_prices, 12)
    emas = extractor_ti.exponential_moving_average(cannonball_prices, 12)
    plt.plot(cannonball_prices, label="Prices")
    plt.plot(smas, label="SMAs")
    plt.plot(emas, label="EMAs")
    plt.legend()
    plt.savefig("./visualizations/trend_indicators.png")

    # Test the volatility indicators
