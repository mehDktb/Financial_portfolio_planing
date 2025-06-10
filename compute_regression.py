import subprocess
import re

def comoute_regression(solver_name, mzn_file, dzn_file):

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

    return re.search(r"Prediction for last row: ([\d\.\-e]+)", result.stdout)