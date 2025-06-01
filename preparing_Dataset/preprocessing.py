import argparse
import pandas as pd
import os

def load_data(path: str) -> pd.DataFrame:
    """
    Load CSV, parse 'Price' column as datetime, and set as index.
    """
    df = pd.read_csv(path, parse_dates=['Price'])
    df.set_index('Price', inplace=True)
    return df

# def filter_interval(df: pd.DataFrame, start: str, end: str) -> pd.DataFrame: #! it can be used to create a time frame 
#     """
#     Filter DataFrame between start and end dates (inclusive).
#     """
#     return df.loc[start:end]

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add lag-1 features for OHLCV.
    """
    df_feat = df.copy()
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df_feat[f'{col}_lag1'] = df_feat[col].shift(1)
    return df_feat.dropna()

def engineer_target(df_feat: pd.DataFrame, horizon: int) -> pd.DataFrame:
    """
    Align features with future 'High' values.
    """
    target_col = f'High_target_{horizon}d'
    df_train = df_feat.copy()
    df_train[target_col] = df_train['High'].shift(-horizon)
    return df_train.dropna()



def prepare_minizinc_data(df_train: pd.DataFrame, target_col: str) -> str:
    """
    Prepare data for MiniZinc with intercept column and save it in the specified data folder.
    
    Parameters:
        df_train (pd.DataFrame): DataFrame containing features and target.
        target_col (str): The name of the target column.

    Returns:
        str: The full path to the generated .dzn file.
    """
    # Add intercept column
    features_df = df_train.drop(columns=[target_col]).copy()
    features_df['intercept'] = 1.0

    # Convert to MiniZinc format
    features = features_df.values.tolist()
    target = df_train[target_col].values.tolist()

    dzn_content = f"""
    n_samples = {len(features)};
    n_features = {len(features[0])};
    X = {features};
    y = {target};
    """

    # Define target path
    file_dir = "/home/mehdi_ktb/Documents/Uni/OR/project/Financial_portfolio_planing/data"
    file_path = os.path.join(file_dir, "data.dzn")

    # Ensure directory exists
    os.makedirs(file_dir, exist_ok=True)

    # Write to file
    with open(file_path, "w") as f:
        f.write(dzn_content.strip())  # strip() removes leading/trailing whitespace

    return file_path




# def preprocess(data_path, horizon):
#     # Load and process the entire dataset
#     df = load_data(data_path)
#     df_feat = engineer_features(df)
#     df_train = engineer_target(df_feat, horizon)
#     # print(df_train.head(15))
#     Y = df_train.iloc[:, -1]
#     prepare_minizinc_data(df_train, Y)




def main():
    parser = argparse.ArgumentParser(description="Forecast Bitcoin high price in N days")
    parser.add_argument("--data", type=str, required=True, help="Path to CSV file")
    parser.add_argument("--horizon", type=int, default=7, help="Days ahead to predict")
    args = parser.parse_args()

    # Load and process
    df = load_data(args.data)
    df_feat = engineer_features(df)
    df_train = engineer_target(df_feat, args.horizon)
    
    # Get target column name dynamically
    target_col = f'High_target_{args.horizon}d'
    
    # Prepare MiniZinc data
    prepare_minizinc_data(df_train, target_col)

if __name__ == '__main__':
    main()

