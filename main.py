import subprocess
import joblib
from preparing_Dataset.preprocessing import preprocess
import numpy as np 

# Your filenames
csv_data = "./raw_data"
mzn_file = "/home/mehdi_ktb/Documents/Uni/OR/project/Financial_portfolio_planing/MiniZinc/linear_regression.mzn"
dzn_file = "./processed_data/processed_data.dzn"


datasets = ["Gold.csv", "Bitcoin.csv", "Ethereum.csv"]
# Specify your solver, e.g., "gecode", "cbc", "coin-bc", "chuffed"
solver_name = "coin-bc"

preprocess(data_path=csv_data+'/'+datasets[1], horizon=7, pred="High")


scaler = joblib.load("/home/mehdi_ktb/Documents/Uni/OR/project/Financial_portfolio_planing/scalers/target_scaler.pkl")


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
else:
    print("Could not find prediction in MiniZinc output.")

