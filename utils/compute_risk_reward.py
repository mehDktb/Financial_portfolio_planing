from utils.todays_price import todays_price

def compute_risk_reward(predictions):
    """
    Compute buy/sell decision and risk-reward ratios for gold, bitcoin, and ethereum
    based on today's prices and predicted min/max values.

    Parameters:
    - predictions: dict with keys: max_gold, min_gold, max_btc, min_btc, max_eth, min_eth

    Returns:
    - buy_sell: List[int] where 0 = buy, 1 = sell
    - risk_rewards: List[float] corresponding to risk/reward ratios
    """
    buy_sell = [None, None, None]  # 0 = buy, 1 = sell
    risk_rewards = [0.0, 0.0, 0.0]

    gold_today, btc_today, eth_today = todays_price()

    # Calculate profit potential
    gold_buy_profit = (predictions["max_gold"] - gold_today) / gold_today
    gold_sell_profit = (gold_today - predictions["min_gold"]) / gold_today

    btc_buy_profit = (predictions["max_btc"] - btc_today) / btc_today
    btc_sell_profit = (btc_today - predictions["min_btc"]) / btc_today

    eth_buy_profit = (predictions["max_eth"] - eth_today) / eth_today
    eth_sell_profit = (eth_today - predictions["min_eth"]) / eth_today

    # Helper function to safely calculate ratio
    def safe_ratio(numerator, denominator):
        if denominator == 0:
            return float('inf')  # Represent very high risk/reward
        return numerator / denominator

    # GOLD
    if gold_buy_profit >= gold_sell_profit:
        buy_sell[0] = 0  # buy
        risk_rewards[0] = min(abs(safe_ratio(gold_buy_profit, gold_sell_profit)), 10)
    else:
        buy_sell[0] = 1  # sell
        risk_rewards[0] = min(abs(safe_ratio(gold_sell_profit, gold_buy_profit)), 10)

    # BTC
    if btc_buy_profit >= btc_sell_profit:
        buy_sell[1] = 0
        risk_rewards[1] = min(abs(safe_ratio(btc_buy_profit, btc_sell_profit)), 10)
    else:
        buy_sell[1] = 1
        risk_rewards[1] = min(abs(safe_ratio(btc_sell_profit, btc_buy_profit)), 10)

    # ETH
    if eth_buy_profit >= eth_sell_profit:
        buy_sell[2] = 0
        risk_rewards[2] = min(abs(safe_ratio(eth_buy_profit, eth_sell_profit)), 10)
    else:
        buy_sell[2] = 1
        risk_rewards[2] = min(abs(safe_ratio(eth_sell_profit, eth_buy_profit)), 10)

    return buy_sell, risk_rewards
