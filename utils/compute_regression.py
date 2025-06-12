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