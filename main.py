import joblib

from utils.run_minizinc import compute_regression, run_portfolio_optimization
from preparing_Dataset.preprocessing import preprocess
from utils.compute_risk_reward import compute_risk_reward
from utils.prepare_data_for_minizinc_model import prepare_and_save_minizinc_data
from datetime import datetime, timedelta
from preparing_Dataset.prepare_data_for_this_week import prepare_data_for_this_week
# Your filenames
csv_data = "./raw_data"
mzn_file = "./MiniZinc/"
dzn_file = "./processed_data/"


today_str = "2024-01-01"
today = datetime.strptime(today_str, "%Y-%m-%d")
end_date = datetime.strptime("2025-02-24", "%Y-%m-%d")

capital=100000.0
datasets = ["Gold.csv", "Bitcoin.csv", "Ethereum.csv"]

gold_high =[]
bitcoin_high =[]
ethereum_high =[]

gold_low =[]
bitcoin_low =[]
ethereum_low =[]

predictions = {}
# always GOLD, BTC, ETH
total_number_of_positions = [1,1,1]
accuracy = [1,1,1]

# Specify your solver, e.g., "gecode", "cbc", "coin-bc", "chuffed"
solver_name = "coin-bc"

while today <= end_date:
    print(f"\033[31m 000000000000000000000000000000000000000 prediction for {today} 000000000000000000000000000000000000000 \033[0m")
    prepare_data_for_this_week(today)
    today += timedelta(days=7)
    for market in datasets:
            for horizon in range(1, 8):
                for pred in ["High", "Low"]:

                    preprocess(data_path=csv_data+'/'+market, horizon=horizon, pred=pred)
                    scaler = joblib.load("./scalers/target_scaler.pkl")

                    match = compute_regression(solver_name, mzn_file+"linear_regression.mzn", dzn_file+"processed_data.dzn")
                    if match:
                        scaled_pred = float(match.group(1))
                        print(f"Scaled prediction: {scaled_pred}")

                        # Load correct scaler
                        target_scaler = joblib.load('scalers/target_scaler.pkl')

                        # Inverse transform
                        original_pred = target_scaler.inverse_transform([[scaled_pred]])[0][0]
                        print(f"Unscaled Prediction for last row: {original_pred}")

                        if market == "Gold.csv" and pred == "High":
                            gold_high.append(original_pred)
                        elif market == "Gold.csv" and pred == "Low":
                            gold_low.append(original_pred)
                        elif market == "Bitcoin.csv" and pred == "High":
                            bitcoin_high.append(original_pred)
                        elif market == "Bitcoin.csv" and pred == "Low":
                            bitcoin_low.append(original_pred)
                        elif market == "Ethereum.csv" and pred == "High":
                            ethereum_high.append(original_pred)
                        elif market == "Ethereum.csv" and pred == "Low":
                            ethereum_low.append(original_pred)
                        else :
                            raise ValueError (f"unsuported input {market} {horizon} {pred}")
                    else:
                        print("Could not find prediction in MiniZinc output.")

                    print(f"000000000000000000000000000000000000000 processing {market} ///// {horizon} ///// {pred} 000000000000000000000000000000000000000")



    predictions["max_btc"] = max(bitcoin_high)
    predictions["max_gold"] = max(gold_high)
    predictions["max_eth"] = max(ethereum_high)

    predictions["min_gold"] = min(gold_low)
    predictions["min_btc"] = min(bitcoin_low)
    predictions["min_eth"] = min(ethereum_low)


    buy_or_sell, risk_rewards, profits, losses= compute_risk_reward(predictions)



    # todo update the capital

    # todo update the dataset

    # todo run this fucking code till End







    # print(gold_high)
    # print(bitcoin_high)
    # print(ethereum_high)
    #
    # print(gold_low)
    # print(bitcoin_low)
    # print(ethereum_low)



    print("----------------------------- Max -----------------------------")
    print(f"maximum of gold: {predictions['max_gold']}")
    print(f"maximum of bitcoin: {predictions['max_btc']}")
    print(f"maximum of ethereum: {predictions['max_eth']}")
    print("----------------------------- Min -----------------------------")
    print(f"minimum of gold: {predictions['min_gold']}")
    print(f"minimum of bitcoin: {predictions['min_btc']}")
    print(f"minimum of ethereum: {predictions['min_eth']}")

    print("----------------------------- risk/rewards -----------------------------")
    print(f"we should {"sell" if buy_or_sell[0] else "buy"} GOLD with rr equal to {risk_rewards[0]}")
    print(f"we should {"sell" if buy_or_sell[1] else "buy"} BTC  with rr equal to {risk_rewards[1]}")
    print(f"we should {"sell" if buy_or_sell[2] else "buy"} ETH with rr equal to {risk_rewards[2]}")



    print("----------------------------- Minizinc -----------------------------")

    prepare_and_save_minizinc_data(gold_profit=profits["gold"], btc_profit=profits["btc"], eth_profit=profits["eth"], rw_gold=risk_rewards[0], rw_btc=risk_rewards[1],
        rw_eth=risk_rewards[2], rw_bond=1, rw_none=1, acc_gold=accuracy[0], acc_btc=accuracy[1],
        acc_eth=accuracy[2], acc_bond=1, acc_none=1, ml_btc=losses["btc"], ml_eth=losses["eth"], capital=capital)

    solution = run_portfolio_optimization(solver_name="Gecode", dzn_file=dzn_file+"portfolio_optimization.dzn", mzn_file=mzn_file+"main_model.mzn")
    if solution:
        print("Optimized Allocation:", solution)
    else:
        print("Optimization failed.")

