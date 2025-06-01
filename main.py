import subprocess
import joblib
import numpy as np 

# Your filenames
mzn_file = "/home/mehdi_ktb/Documents/Uni/OR/project/Financial_portfolio_planing/MiniZinc/linear_regression.mzn"
dzn_file = "/home/mehdi_ktb/Documents/Uni/OR/project/Financial_portfolio_planing/data/data.dzn"

# Specify your solver, e.g., "gecode", "cbc", "coin-bc", "chuffed"
solver_name = "coin-bc"

scaler = joblib.load("/home/mehdi_ktb/Documents/Uni/OR/project/Financial_portfolio_planing/preparing_Dataset/target_scaler.pkl")


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
match = re.search(r"Prediction for last row: ([\d\.\-e]+)", result.stdout)
if match:
    scaled_pred = float(match.group(1))
    original_pred = scaler.inverse_transform([[scaled_pred]])[0][0]
    print(f"\nUnscaled Prediction for last row: {original_pred}")
else:
    print("Could not find prediction in MiniZinc output.")


