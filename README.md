# Financial Portfolio Optimization Using Operations Research

## Overview

This repository contains the implementation of an advanced financial portfolio optimization system integrating time-series forecasting, risk-reward evaluation, and mathematical optimization techniques. The goal is to dynamically allocate investments across Gold, Bitcoin, Ethereum, and Bonds, considering risk constraints and leverage.

## Features

* **Time-Series Forecasting**: Employs linear regression models to predict future asset prices based on historical data.
* **Feature Engineering**: Utilizes lagged variables and moving averages to enhance prediction accuracy.
* **Risk-Reward Analysis**: Generates buy/sell signals based on predicted price movements and calculates potential profits and losses.
* **Constraint Optimization**: Implements constraint programming models in MiniZinc to determine optimal capital allocation while respecting leverage and risk tolerance limits.
* **Weekly Capital Updates**: Automatically adjusts the portfolio based on real market outcomes, tracking performance and accuracy over time.

## Workflow

The complete workflow includes:

1. **Data Preparation** (`prepare_data_for_this_week.py`)

   * Extracts recent market data (100-day window).

2. **Preprocessing and Feature Engineering** (`preprocessing.py`)

   * Prepares and scales data, generating lagged features and moving averages.

3. **Forecasting** (`linear_regression.mzn`)

   * Applies linear regression via MiniZinc to forecast future prices.

4. **Risk-Reward Analysis** (`compute_risk_reward.py`)

   * Calculates potential buy/sell profits and generates trading signals.

5. **Portfolio Optimization** (`main_model.mzn`)

   * Solves optimization problems to allocate investments optimally.

6. **Capital Update** (`update_capital.py`)

   * Updates portfolio values weekly based on actual market performance.

7. **Performance Tracking**

   * Records capital growth, prediction accuracy, and trade effectiveness.

## Performance Evaluation

* Typical weekly iteration time: **under 30 seconds**.
* Forecast and optimization models provide near-real-time decision-making capabilities.
* Tracks metrics including Return on Investment (ROI), accuracy rates, and capital growth.

## Visualization

Currently, the repository does not include built-in visualization tools or scripts. However, suggested visualizations for implementation include:

* Forecasted vs. actual asset prices
* Capital growth trajectories
* Weekly allocation breakdown
* Prediction accuracy trends
* Risk-reward profiles

## Limitations and Future Improvements

* Consideration of nonlinear market dynamics through advanced models (e.g., ARIMA, Random Forest, Neural Networks).
* Incorporation of adaptive risk management and dynamic leverage constraints.
* Inclusion of transaction costs and detailed margin rules.
* Real-time data streaming integration for intraday trading.

## Installation and Usage

Clone the repository:

```bash
git clone https://github.com/mehDktb/Financial_portfolio_planing.git
cd Financial_portfolio_planing
```

Ensure you have required dependencies installed (Python, MiniZinc, pandas, sklearn):

```bash
pip install -r requirements.txt
```

To run the system, execute:

```bash
python3 main.py
```

Follow the steps outlined in the workflow to further interact with the system.

## Contribution

Contributions and suggestions are welcome. Please submit pull requests or issues on GitHub. Contributions toward adding visualization and plotting capabilities are especially encouraged.

## License

This project is licensed under the MIT License.
