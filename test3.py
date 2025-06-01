
from sklearn.linear_model import LinearRegression
import pandas as pd



def train_and_forecast(df_feat: pd.DataFrame, df_train: pd.DataFrame, horizon: int) -> float:
    """
    Train on all data and forecast the high price horizon days ahead.
    """
    # Define features and target
    base_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    feature_cols = base_cols + [f"{col}_lag1" for col in base_cols]
    target_col = f'High_target_{horizon}d'

    # Training
    X_train = df_train[feature_cols]
    y_train = df_train[target_col]
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Prepare inputs for forecast: features from the last available date
    last_date = df_feat.index.max()
    X_forecast = df_feat.loc[[last_date], feature_cols]

    # Predict
    prediction = model.predict(X_forecast)[0]
    predict_date = last_date + pd.Timedelta(days=horizon)
    print(f"Predicted High for {predict_date.date()}: {prediction:.2f}")
    return prediction


def main():
    parser = argparse.ArgumentParser(description="Forecast Bitcoin high price in N days")
    parser.add_argument("--data", type=str, required=True, help="Path to CSV file")
    parser.add_argument("--horizon", type=int, default=7, help="Days ahead to predict")
    args = parser.parse_args()

    # Load and process
    df = load_data(args.data)
    df_feat = engineer_features(df)
    df_train = engineer_target(df_feat, args.horizon)

    # Train on all and forecast
    train_and_forecast(df_feat, df_train, args.horizon)


if __name__ == '__main__':
    main()
