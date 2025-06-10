import joblib
import argparse
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import StandardScaler

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

def engineer_target(df_feat: pd.DataFrame, horizon: int, pred) -> pd.DataFrame:
    """
    Align features with future 'High' values.
    """
    target_col = f'{pred}_target_{horizon}d'
    df_train = df_feat.copy()
    df_train[target_col] = df_train[pred].shift(-horizon)
    print(df_train.head(15))
    return df_train.dropna()



def to_minizinc_2d(data: list) -> str:
    """Convert Python list of lists to MiniZinc 2D array literal"""
    rows = []
    for row in data:
        formatted_row = ", ".join([f"{x:.4f}" for x in row])
        rows.append(f"| {formatted_row}")
    return f"[{' '.join(rows)} |]"




def prepare_minizinc_data(df_train: pd.DataFrame, target_col: str, scale_features=True, scale_target=True) -> str:
    """
    Prepare processed_data for MiniZinc regression with intercept and optional scaling.

    Args:
        df_train: DataFrame with features and target.
        target_col: Name of the target column.
        scale_features: Whether to scale features (recommended for large values).
        scale_target: Whether to scale the target (recommended for large values).

    Returns:
        Path to the generated .dzn file.
    """
    # Separate features and target
    features_df = df_train.drop(columns=[target_col])
    target = df_train[target_col]

    # Scale features if requested
    if scale_features:
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features_df)
        features_df = pd.DataFrame(features_scaled, columns=features_df.columns, index=features_df.index)
        joblib.dump(scaler, 'scalers/feature_scaler.pkl')

    # Scale target if requested
    if scale_target:
        target_scaler = StandardScaler()
        target_scaled = target_scaler.fit_transform(target.values.reshape(-1, 1)).flatten()
        target = pd.Series(target_scaled, index=target.index)
        joblib.dump(target_scaler, 'scalers/target_scaler.pkl')

    # Add intercept column (after scaling)
    features_df['intercept'] = 1.0

    # Convert to MiniZinc format
    features = features_df.values.tolist()
    target_list = target.values.tolist()

    dzn_content = f"""
    n_samples = {len(features)};
    n_features = {len(features[0])};
    X = {to_minizinc_2d(features)};
    y = {target_list};
    """
    with open("processed_data/processed_data.dzn", "w") as f:
        f.write(dzn_content)

    return "processed_data.dzn"



def preprocess(data_path, horizon, pred):
    # Load and process the entire dataset
    df = load_data(data_path)
    df_feat = engineer_features(df)
    df_train = engineer_target(df_feat, horizon, pred)
    # print(df_train.head(15))
    target_col = f'{pred}_target_{horizon}d'
    prepare_minizinc_data(df_train, target_col)





# def main():
#     parser = argparse.ArgumentParser(description="Forecast Bitcoin high price in N days")
#     parser.add_argument("--data", type=str, required=True, help="Path to CSV file")
#     parser.add_argument("--horizon", type=int, default=7, help="Days ahead to predict")
#     parser.add_argument("--pred" , type =str, required=True, help="High for highest price during the next week and Low for lowest price for next week")
#     args = parser.parse_args()
#
#     # Load and process
#     df = load_data(args.data)
#     df_feat = engineer_features(df)
#     df_train = engineer_target(df_feat, args.horizon, args.pred)
#
#     # Get target column name dynamically
#     target_col = f'{args.pred}_target_{args.horizon}d'
#
#     # Prepare MiniZinc processed_data
#     prepare_minizinc_data(df_train, target_col)
#
# if __name__ == '__main__':
#     main()

