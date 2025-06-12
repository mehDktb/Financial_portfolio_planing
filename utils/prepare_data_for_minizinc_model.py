def prepare_and_save_minizinc_data(
        gold_profit,
        btc_profit,
        eth_profit,
        rw_gold,
        rw_btc,
        rw_eth,
        rw_bond,
        rw_none,
        acc_gold,
        acc_btc,
        acc_eth,
        acc_bond,
        acc_none,
        ml_btc,
        ml_eth,
        capital=10000.0,
):
    """
    Prepare data for MiniZinc optimization model and save it to a .dzn file.

    Args:
        All the model parameters...
        filename: Name of the .dzn file to create (default: "portfolio_optimization.dzn")

    Returns:
        Dictionary with all parameters needed for the MiniZinc model.
    """
    # Calculate SOP_RW_ACC (sum of products of risk-rewards and accuracies)
    sop_rw_acc = (rw_gold * acc_gold) + (rw_btc * acc_btc) + (rw_eth * acc_eth) + (rw_bond * acc_bond) + (
                rw_none * acc_none)
    filename = "./processed_data/portfolio_optimization.dzn"
    # Prepare data dictionary for MiniZinc
    minizinc_data = {
        'GOLD_PROFIT': gold_profit,
        'BTC_PROFIT': btc_profit,
        'ETH_PROFIT': eth_profit,
        'RW_GOLD': rw_gold,
        'RW_BTC': rw_btc,
        'RW_ETH': rw_eth,
        'RW_BOND': rw_bond,
        'RW_NONE': rw_none,
        'ACC_GOLD': acc_gold,
        'ACC_BTC': acc_btc,
        'ACC_ETH': acc_eth,
        'ACC_BOND': acc_bond,
        'ACC_NONE': acc_none,
        'ML_GOLD': ml_gold,
        'ML_BTC': ml_btc,
        'ML_ETH': ml_eth,
        'SOP_RW_ACC': sop_rw_acc,
        'CAPITAL': capital
    }

    # Save to .dzn file
    with open(filename, 'w') as f:
        f.write("% MiniZinc Data File - Portfolio Optimization\n")
        f.write("% Generated automatically\n\n")

        for key, value in minizinc_data.items():
            f.write(f"{key} = {value};\n")

    print(f"Data saved to {filename}")
    return minizinc_data

