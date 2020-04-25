import pytest
import pandas as pd
from data.indices import indices

class TestIndices: 
    def test_ids_match_names(self):
        item_ids = pd.read_csv("data/item_ids_04_12_2020.csv", index_col="id")
        for index_df in indices.values():
            expected_names = item_ids.loc[index_df["id"]]["name"].reset_index(drop=True)
            actual_names = pd.Series(index_df["name"])
            pd.testing.assert_series_equal(expected_names, actual_names)