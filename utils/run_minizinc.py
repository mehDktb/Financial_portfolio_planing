import subprocess
import re


def compute_regression(solver_name, mzn_file, dzn_file):
    try:
        result = subprocess.run(
            ["minizinc", "--solver", solver_name, mzn_file, dzn_file],
            text=True,
            capture_output=True,
            check=True
        )

        # Output result
        print("MiniZinc Output:")
        print(result.stdout)
        print("-" * 50)

        # Extract prediction value - updated regex pattern
        prediction_match = re.search(r"Future prediction: ([\d\.\-e]+)", result.stdout)

        if prediction_match:
            prediction_value = float(prediction_match.group(1))
            print(f"Extracted prediction: {prediction_value}")
            return prediction_match
        else:
            print("Could not find prediction in MiniZinc output.")
            return None

    except subprocess.CalledProcessError as e:
        print("An error occurred while running MiniZinc:")
        print(e.stderr)
        return None


def run_portfolio_optimization(solver_name, mzn_file, dzn_file):
    """
    Executes a MiniZinc portfolio optimization model using subprocess and extracts solution values.

    Parameters:
        solver_name (str): Name of the MiniZinc solver (e.g., "gecode", "coin-bc").
        mzn_file (str): Path to the .mzn model file.
        dzn_file (str): Path to the .dzn data file.

    Returns:
        dict: A dictionary containing the values of decision variables (e.g., x_gold, x_btc, etc.) if successful.
              Returns None if an error occurs or parsing fails.
    """

    try:
        # Run the MiniZinc model with solver and data file
        result = subprocess.run(
            ["minizinc", "--solver", solver_name, mzn_file, dzn_file],
            text=True,
            capture_output=True,
            check=True
        )

        # Print raw MiniZinc output
        print("MiniZinc Output:\n", result.stdout)
        print("-" * 60)

        # Extract variable results using regex
        pattern = r"(x_gold|x_btc|x_eth|x_bond|x_nothing|lev_btc|lev_eth)\s*=\s*([\d\.]+)"
        matches = re.findall(pattern, result.stdout)

        if not matches:
            print("⚠️ No solution values found in output.")
            return None

        # Parse results into a dictionary
        solution = {var: float(val) if 'lev' not in var else int(float(val)) for var, val in matches}

        print("✅ Extracted Solution:")
        for var, val in solution.items():
            print(f"{var}: {val}")

        return solution

    except subprocess.CalledProcessError as e:
        print("❌ An error occurred while running MiniZinc:")
        print(e.stderr)
        return None