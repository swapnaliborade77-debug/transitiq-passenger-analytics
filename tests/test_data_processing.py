import pandas as pd
from src.data_cleaning import clean_data

def test_clean_removes_duplicates_and_trims_strings():
    df = pd.DataFrame({"route":[" R1 "," R1 "], "stop":[" A "," A "], "hour":[8,8], "passengers":[10,10]})
    result = clean_data(df)
    assert len(result) == 1
    assert result.iloc[0]["route"] == "R1"
    assert result.iloc[0]["passengers"] == 10
