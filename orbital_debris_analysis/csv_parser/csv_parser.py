import pandas as pd
from pandas import DataFrame


def csv_to_pandas(file_path: str) -> DataFrame:
    return pd.read_csv(file_path)

