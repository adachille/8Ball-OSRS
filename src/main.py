import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime
from tqdm import tqdm
from api.runescape_services_api import OldSchoolGEAPIInterface
from data.indices import indices
from model.simulator import Simulator, PricePredictorType, PortfolioAllocatorType

def update_prices(ge_api, item_ids):
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
                api_called = ge_api.update_price_history_csv(item_id, "./data/prices/")
                if api_called:
                    sleep_counter += 1
                price_history_updated = True
            except Exception:
                # This except is triggered when the issue discussed above occurs,
                # just let it rest for a minute
                print('______________')
                print("Failed on item_id: ", item_id)
                print('______________')
                attempts += 1
                time.sleep(60)

def backtest_index(index_name, pp=PricePredictorType.MANUAL, 
        pa=PortfolioAllocatorType.MANUAL, starting_cash=100000):
    # Get the starting prices and and price_history_tuples for the index
    index_ids = indices[index_name]["id"].values
    price_histories = []
    starting_prices = []
    lastest_start_date = None
    for id in index_ids:
        index_price_history_df = pd.read_csv(f"./data/prices/{id}_price_history.csv", 
            index_col="date", parse_dates=["date"])
        price_histories.append(index_price_history_df)
        starting_prices.append(index_price_history_df["price"].iloc[0])

        # Get the lastest start date for the price history
        if lastest_start_date is None or index_price_history_df.index[0] > lastest_start_date:
            lastest_start_date = index_price_history_df.index[0]
    
    # Make sure that all the dataframes start at the lastest_start_date
    for i in range(len(price_histories)):
        price_histories[i] = price_histories[i][price_histories[i].index >= lastest_start_date]

    price_history_tuples = [(id, tup) for id, tup in zip(index_ids, price_histories)]

    # Create the starting portfolio
    index_portfolio = pd.DataFrame(data={
        "price": starting_prices,
        "amount": 0
    }, index=index_ids)
    cash_df = pd.DataFrame(data=[[1, starting_cash]], columns=["price", "amount"], index=[-1])
    starting_portfolio = pd.concat([index_portfolio, cash_df])

    sim = Simulator(starting_portfolio, pp, pa)
    return sim.backtest(price_history_tuples)

if __name__ == "__main__":
    # Instantiate our Grand Exchange API Interface
    ge_api = OldSchoolGEAPIInterface()

    # Update item id's
    # ge_api.get_and_save_item_ids_to_csv('./data/item_ids_04_X_2020.csv') 

    # Get item ids
    item_ids = pd.read_csv('./data/item_ids_04_12_2020.csv')["id"]

    # Update prices
    # update_prices(ge_api, item_ids)
    
    # Backtest using manual price predictor and portfolio allocator (defaults)
    index = "food"
    port_stats = {}
    port_stats["start_val"] = 100000
    port_stats["port_vals"] = backtest_index(index, starting_cash=port_stats["start_val"])
    port_stats["end_val"] = port_stats["port_vals"].iloc[-1]
    port_stats["total_ret"] = (port_stats["end_val"] - port_stats["start_val"]) / port_stats["start_val"]
    print(f'Start Value: {port_stats["start_val"]}')
    print(f'End Value: {port_stats["end_val"]}')
    print(f'Total Return: {port_stats["total_ret"]}')
    port_stats["delta"] = port_stats["port_vals"] - port_stats["port_vals"].shift(1)
    port_stats["rets"] = port_stats["delta"] / port_stats["port_vals"]
    port_stats["std_dev_rets"] = port_stats["rets"].std()
    print(f'Standard Deviation of Returns: {port_stats["std_dev_rets"]}')

    # Make Visualizations
    ax = port_stats["port_vals"].plot()
    fig = ax.get_figure()
    fig.savefig(f'./visualizations/model_performance/mpp_mpa_{index}_portvals.png')
    fig.clf()
    ax = port_stats["rets"].plot()
    fig = ax.get_figure()
    fig.savefig(f'./visualizations/model_performance/mpp_mpa_{index}_rets.png')