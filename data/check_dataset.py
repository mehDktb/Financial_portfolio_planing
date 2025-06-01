import os

def check_dzn_data(filepath):
    # Read the file
    with open(filepath, 'r') as f:
        content = f.read()

    # Parse key variables
    data = {}
    exec(content, {}, data)  # Caution: Only use with trusted files!
    # (For safety, you could parse manually instead of using exec)

    # Check required variables exist
    required = ['n_samples', 'n_features', 'X', 'y']
    missing = [var for var in required if var not in data]
    if missing:
        print(f"ERROR: Missing variables in .dzn file: {missing}")
        return False

    # Check dimensions
    X = data['X']
    y = data['y']
    if len(X) != data['n_samples'] or len(X[0]) != data['n_features']:
        print(f"ERROR: X dimensions do not match n_samples or n_features")
        return False
    if len(y) != data['n_samples']:
        print(f"ERROR: y length does not match n_samples")
        return False

    # Check intercept column (last column of X)
    intercept_col = [row[-1] for row in X]
    if not all(abs(x - 1.0) < 1e-6 for x in intercept_col):
        print("WARNING: Intercept column (last column of X) is not all 1.0")

    # Check for missing values
    if any(None in row for row in X):
        print("ERROR: X contains missing values")
        return False
    if None in y:
        print("ERROR: y contains missing values")
        return False

    print("Data appears correct.")
    return True

# Main
if __name__ == '__main__':
    filepath = "/home/mehdi_ktb/Documents/Uni/OR/project/Financial_portfolio_planing/data/data.dzn"
    if not filepath:
        filepath = 'data.dzn'
    if not os.path.exists(filepath):
        print(f"ERROR: File not found: {filepath}")
    else:
        check_dzn_data(filepath)
