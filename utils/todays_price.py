import pandas as pd
def todays_price():

    df_gold = pd.read_csv("./raw_data/Gold.csv")
    gold_today = df_gold.tail(1)["Open"].iloc[0]
    print(gold_today)
    del df_gold

    df_btc = pd.read_csv("./raw_data/Bitcoin.csv")
    btc_today = df_btc.tail(1)["Open"].iloc[0]
    print(btc_today)
    del df_btc

    df_eth = pd.read_csv("./raw_data/Ethereum.csv")
    eth_today = df_eth.tail(1)["Open"].iloc[0]
    print(eth_today)
    del df_eth

    return gold_today, btc_today, eth_today