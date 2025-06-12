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


def engineer_features(df: pd.DataFrame, lags=[1, 2, 5], include_ma=True, ma_windows=[5, 10]) -> pd.DataFrame:
    df_feat = df.copy()
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        for lag in lags:
            df_feat[f'{col}_lag{lag}'] = df_feat[col].shift(lag)
        if include_ma:
            for window in ma_windows:
                df_feat[f'{col}_ma{window}'] = df_feat[col].rolling(window=window).mean()
    return df_feat.dropna()


def prepare_training_data(df_feat: pd.DataFrame, horizon: int, pred: str) -> tuple:
    """
    Prepare training data by creating target values from historical data.
    For each row, the target is the value 'horizon' days in the future.

    Returns:
        - df_train: DataFrame with features and targets for training
        - df_predict: DataFrame with features for the final prediction (no target)
    """
    target_col = f'{pred}_target_{horizon}d'
    df_train = df_feat.copy()

    # Create target by shifting the prediction column backward by horizon days
    # This means: for day i, target = value at day (i + horizon)
    df_train[target_col] = df_train[pred].shift(-horizon)

    # Split into training data (has targets) and prediction data (no targets)
    # Training data: all rows except the last 'horizon' rows (they don't have future targets)
    df_train_with_targets = df_train[:-horizon].copy()

    # Prediction data: the last row(s) that we'll use to predict future values
    # We only need the last row since we're predicting one step ahead
    df_predict = df_train.iloc[[-1]].copy()  # Last row for prediction
    df_predict = df_predict.drop(columns=[target_col])  # Remove target column

    return df_train_with_targets.dropna(), df_predict


def to_minizinc_2d(data: list) -> str:
    """Convert Python list of lists to MiniZinc 2D array literal"""
    rows = []
    for row in data:
        formatted_row = ", ".join([f"{x:.4f}" for x in row])
        rows.append(f"| {formatted_row}")
    return f"[{' '.join(rows)} |]"


def prepare_minizinc_data(df_train: pd.DataFrame, df_predict: pd.DataFrame,
                          target_col: str, scale_features=True, scale_target=True) -> str:
    """
    Prepare data for MiniZinc regression with intercept and optional scaling.

    Args:
        df_train: DataFrame with features and target for training.
        df_predict: DataFrame with features for prediction (no target).
        target_col: Name of the target column.
        scale_features: Whether to scale features.
        scale_target: Whether to scale the target.

    Returns:
        Path to the generated .dzn file.
    """
    # Ensure scalers directory exists
    os.makedirs('scalers', exist_ok=True)
    os.makedirs('processed_data', exist_ok=True)

    # Separate features and target from training data
    train_features_df = df_train.drop(columns=[target_col])
    target = df_train[target_col]

    # Get prediction features
    predict_features_df = df_predict.copy()

    # Scale features if requested
    if scale_features:
        scaler = StandardScaler()
        # Fit on training features
        train_features_scaled = scaler.fit_transform(train_features_df)
        train_features_df = pd.DataFrame(train_features_scaled,
                                         columns=train_features_df.columns,
                                         index=train_features_df.index)

        # Transform prediction features using the same scaler
        predict_features_scaled = scaler.transform(predict_features_df)
        predict_features_df = pd.DataFrame(predict_features_scaled,
                                           columns=predict_features_df.columns,
                                           index=predict_features_df.index)

        joblib.dump(scaler, 'scalers/feature_scaler.pkl')

    # Scale target if requested
    if scale_target:
        target_scaler = StandardScaler()
        target_scaled = target_scaler.fit_transform(target.values.reshape(-1, 1)).flatten()
        target = pd.Series(target_scaled, index=target.index)
        joblib.dump(target_scaler, 'scalers/target_scaler.pkl')

    # Add intercept column (after scaling)
    train_features_df['intercept'] = 1.0
    predict_features_df['intercept'] = 1.0

    # Convert to MiniZinc format
    train_features = train_features_df.values.tolist()
    predict_features = predict_features_df.values.tolist()
    target_list = target.values.tolist()

    dzn_content = f"""
n_samples = {len(train_features)};
n_features = {len(train_features[0])};
X = {to_minizinc_2d(train_features)};
y = {target_list};
X_predict = {to_minizinc_2d(predict_features)};
"""

    with open("processed_data/processed_data.dzn", "w") as f:
        f.write(dzn_content)

    return "processed_data/processed_data.dzn"


def preprocess(data_path, horizon, pred):
    """
    Main preprocessing function for forecasting.

    This function prepares data to predict the value 'horizon' days into the future.
    For example, if you have data for days 1-100 and horizon=1,
    it will prepare data to predict the value for day 101.
    """
    # Load and process the entire dataset
    df = load_data(data_path)
    print(f"Loaded data: {len(df)} samples")
    print(f"Date range: {df.index[0]} to {df.index[-1]}")

    # Engineer features (adds lag-1 features)
    df_feat = engineer_features(df)
    print(f"Features engineered: {len(df_feat)} samples after adding lags")

    # Prepare training and prediction data
    df_train, df_predict = prepare_training_data(df_feat, horizon, pred)

    print(f"Training samples: {len(df_train)}")
    print(f"Prediction features prepared for forecasting {horizon} days ahead")
    print(f"Last training date: {df_train.index[-1]}")
    print(f"Predicting for approximately: {df_train.index[-1] + pd.Timedelta(days=horizon)}")

    # Get target column name dynamically
    target_col = f'{pred}_target_{horizon}d'

    # Prepare MiniZinc data
    prepare_minizinc_data(df_train, df_predict, target_col)

    print("Data prepared successfully!")
    print(f"Training data shape: {df_train.shape}")
    print(f"Prediction data shape: {df_predict.shape}")

    return df_train, df_predict


def main():
    parser = argparse.ArgumentParser(description="Prepare data for forecasting")
    parser.add_argument("--data", type=str, required=True, help="Path to CSV file")
    parser.add_argument("--horizon", type=int, default=1, help="Days ahead to predict")
    parser.add_argument("--pred", type=str, required=True,
                        help="Column to predict (e.g., 'High', 'Low', 'Close')")

    args = parser.parse_args()

    # Preprocess data
    df_train, df_predict = preprocess(args.data, args.horizon, args.pred)

    print("\nSample of training data:")
    print(df_train.tail(3))
    print("\nFeatures for prediction:")
    print(df_predict)


if __name__ == '__main__':
    main()