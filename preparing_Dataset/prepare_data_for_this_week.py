import pandas as pd
import os
from datetime import datetime, timedelta


def prepare_data_for_this_week(today):
    markets = ["Gold", "Bitcoin", "Ethereum"]
    for market in markets:
        save_path = f"./raw_data/{market}.csv"
        start_date = today - timedelta(days=29)
        raw_data = pd.read_csv(f"./raw_data/{market}_raw.csv")
        raw_data['Price'] = pd.to_datetime(raw_data['Price'])
        mask = (raw_data['Price'] >= start_date) & (raw_data['Price'] <= today)
        filtered_data = raw_data.loc[mask]
        filtered_data.to_csv(save_path, index=False)

        print(f"✅ Saved {market} ---> {len(filtered_data)} rows from {start_date.date()} to {today.date()} to: {save_path}")



