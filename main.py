import subprocess
import joblib
from preparing_Dataset.preprocessing import preprocess
import numpy as np 

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

# Specify your solver, e.g., "gecode", "cbc", "coin-bc", "chuffed"
solver_name = "coin-bc"

for market in datasets:
        for horizon in range(1, 8):
            for pred in ["High", "Low"]:

                preprocess(data_path=csv_data+'/'+market, horizon=horizon, pred=pred)


                scaler = joblib.load("./scalers/target_scaler.pkl")


                try:
                    result = subprocess.run(
                        ["minizinc", "--solver", solver_name, mzn_file, dzn_file],
                        text=True,
                        capture_output=True,
                        check=True
                    )

                    # Output result
                    print("MiniZinc Output:\n")
                    print(result.stdout)

                except subprocess.CalledProcessError as e:
                    print("An error occurred while running MiniZinc:")
                    print(e.stderr)



                # coefficients = result.stdout[1:-13].split(", ")
                # print(coefficients)

                import re
                # Extract prediction
                match = re.search(r"Prediction for last row: ([\d\.\-e]+)", result.stdout)
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



print(gold_high)
print(bitcoin_high)
print(ethereum_high)

print(gold_low)
print(bitcoin_low)
print(ethereum_low)



print("----------------------------- Max -----------------------------")
print(f"maximum of gold: {max(gold_high)}")
print(f"maximum of bitcoin: {max(bitcoin_high)}")
print(f"maximum of ethereum: {max(ethereum_high)}")
print("----------------------------- Min -----------------------------")
print(f"minimum of gold: {min(gold_low)}")
print(f"minimum of bitcoin: {min(bitcoin_low)}")
print(f"minimum of ethereum: {min(ethereum_low)}")






