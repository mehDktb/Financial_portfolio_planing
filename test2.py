import pandas as pd
from sklearn.linear_model import LinearRegression

# Hard-coded path to the CSV dataset and forecast horizon
DATASET_PATH = "/home/mehdi_ktb/Desktop/sandbox/cososher/Bitcoin2.csv"
HORIZON = 7  # days ahead to predict (next week)


def load_data(path):
    """
    Load the CSV file, parse dates, and set the 'Date' index.
    """
    df = pd.read_csv(path, parse_dates=[0])
    df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
    df.set_index('Date', inplace=True)
    return df


def engineer_features(df):
    """
    Create lag-1 features for OHLCV.
    """
    df_feat = df.copy()
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df_feat[f'{col}_lag1'] = df_feat[col].shift(1)
    return df_feat.dropna()


def engineer_target(df_feat, horizon):
    """
    Prepare training set: align features with future High value.
    """
    target_col = f'High_target_{horizon}d'
    df_train = df_feat.copy()
    df_train[target_col] = df_train['High'].shift(-horizon)
    return df_train.dropna()


def train_and_forecast(df_feat, df_train, horizon):
    """
    Train a linear regression on historical data, then forecast for last raw date.
    """
    feature_cols = ['Open', 'High', 'Low', 'Close', 'Volume'] + [f'{col}_lag1' for col in ['Open', 'High', 'Low', 'Close', 'Volume'] ]
    target_col = f'High_target_{horizon}d'

    # Training data
    X_train = df_train[feature_cols]
    y_train = df_train[target_col]

    # Feature vector for forecasting: last available date
    last_date = df_feat.index.max()
    X_forecast = df_feat.loc[[last_date], feature_cols]

    # Fit and predict
    model = LinearRegression()
    model.fit(X_train, y_train)
    pred = model.predict(X_forecast)[0]

    # Output
    predict_date = last_date + pd.Timedelta(days=horizon)
    print(f"Predicted High for {predict_date.date()}: {pred:.2f}")


def main():
    # Load raw data
    df = load_data(DATASET_PATH)

    # Engineer features and prepare training set
    df_feat = engineer_features(df)
    df_train = engineer_target(df_feat, HORIZON)
    df_train.to_csv("train.csv")
    # Train model and forecast next week
    train_and_forecast(df_feat, df_train, HORIZON)


if __name__ == '__main__':
    main()
