import joblib

from utils.compute_regression import compute_regression
from preparing_Dataset.preprocessing import preprocess
from utils.compute_risk_reward import compute_risk_reward

# Your filenames
csv_data = "./raw_data"
mzn_file = "./MiniZinc/linear_regression.mzn"
dzn_file = "./processed_data/processed_data.dzn"


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

for market in datasets:
        for horizon in range(1, 8):
            for pred in ["High", "Low"]:

                preprocess(data_path=csv_data+'/'+market, horizon=horizon, pred=pred)
                scaler = joblib.load("./scalers/target_scaler.pkl")

                match = compute_regression(solver_name, mzn_file, dzn_file)
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


predictions["max_btc"] = max(bitcoin_high)
predictions["max_gold"] = max(gold_high)
predictions["max_eth"] = max(ethereum_high)

predictions["min_gold"] = min(gold_low)
predictions["min_btc"] = min(bitcoin_low)
predictions["min_eth"] = min(ethereum_low)


buy_or_sell, risk_rewards = compute_risk_reward(predictions)

# todo implementing minizinc code

# todo risk/reward ____ accuracy ____ sum of product of them

# todo pass data to new minizinc code

# todo update the capital

# todo update the dataset

# todo run this fucking code till End







print(gold_high)
print(bitcoin_high)
print(ethereum_high)

print(gold_low)
print(bitcoin_low)
print(ethereum_low)



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




