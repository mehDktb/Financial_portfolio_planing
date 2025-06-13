import pandas as pd
from datetime import datetime, timedelta

def update_capital(today, capital, solution, predictions, buy_or_sell, profits, losses, accuracy, total_number_of_positions):
    # Convert the input string to a datetime object
    end_date = today + timedelta(days=7)

    results = {}

    tp_gold = predictions["min_gold"] if buy_or_sell[0] else predictions["max_gold"]
    sl_gold = predictions["max_gold"] if buy_or_sell[0] else predictions["min_gold"]

    tp_btc = predictions["min_btc"] if buy_or_sell[0] else predictions["max_btc"]
    sl_btc = predictions["max_btc"] if buy_or_sell[0] else predictions["min_btc"]

    tp_eth = predictions["min_eth"] if buy_or_sell[0] else predictions["max_eth"]
    sl_eth = predictions["max_eth"] if buy_or_sell[0] else predictions["min_eth"]

    for market in ["Gold", "Bitcoin", "Ethereum"]:
        # Load data
        data = pd.read_csv(f"./raw_data/{market}_raw.csv")

        # Convert the 'Price' column to datetime
        data['Price'] = pd.to_datetime(data['Price'])

        # Filter data between today and next 7 days
        mask = (data['Price'] >= today) & (data['Price'] <= end_date)
        filtered_data = data.loc[mask]

        if filtered_data.empty:
            max_high = None
            min_low = None
        else:
            max_high = filtered_data['High'].max()
            min_low = filtered_data['Low'].min()

        results[market] = {"max_high": max_high, "min_low": min_low}

    print("this is reultsssssssssssssssssssssssssssss" , results)
    if solution:
        if buy_or_sell[0]:
            if results["Gold"]["min_low"] <= predictions["min_gold"]:
                capital += solution['x_gold'] * (profits['gold'])
                accuracy[0] += 1
                print(f"\033[31m you earned {solution['x_gold'] * (profits['gold'])} in gold \033[0m")

            elif results["Gold"]["max_high"] >= predictions["max_gold"]:
                capital += solution['x_gold'] * (-losses['gold'])
                print(f"\033[31m you lost {solution['x_gold'] * (-losses['gold'])} in gold \033[0m")

            else:
                capital += solution['x_gold'] * (profits['gold']*0.3)
                accuracy[0] += 1
                print(f"\033[31m you earned {solution['x_gold'] * (profits['gold']*0.3)} in gold \033[0m")


        else:
            if results["Gold"]["max_high"] >= predictions["max_gold"]:
                capital += solution['x_gold'] * (profits['gold'])
                accuracy[0] += 1
                print(f"\033[31m you earned {solution['x_gold'] * (profits['gold'])} in gold \033[0m")

            elif results["Gold"]["min_low"] <= predictions["min_gold"]:
                capital += solution['x_gold'] * (-losses['gold'])
                print(f"\033[31m you lost {solution['x_gold'] * (-losses['gold'])} in gold \033[0m")
            else:
                capital += solution['x_gold'] * (profits['gold']*0.3)
                accuracy[0] += 1
                print(f"\033[31m you earned {solution['x_gold'] * (profits['gold'] * 0.3)} in gold \033[0m")

        if buy_or_sell[1]:
            if results["Bitcoin"]["min_low"] <= predictions["min_btc"]:
                capital += solution["lev_btc"] * solution['x_btc'] * (profits['btc'])
                accuracy[1] += 1
                print(f"\033[31m you earned {solution['x_btc'] * (profits['btc'])} in btc \033[0m")

            elif results["Bitcoin"]["max_high"] >= predictions["max_btc"]:
                capital += solution["lev_btc"] * solution['x_btc'] * (-losses['btc'])
                print(f"\033[31m you lost {solution['x_btc'] * (-losses['btc'])} in btc \033[0m")

            else:
                capital += solution['x_btc'] * (profits['btc']*0.3)
                accuracy[1] += 1
                print(f"\033[31m you earned {solution['x_btc'] * (profits['btc']*0.3)} in btc \033[0m")

        else:
            if results["Bitcoin"]["max_high"] >= predictions["max_btc"]:
                capital += solution["lev_btc"] * solution['x_btc'] * (profits['btc'])
                accuracy[1] += 1
                print(f"\033[31m you earned {solution['x_btc'] * (profits['btc'])} in btc \033[0m")

            elif results["Bitcoin"]["min_low"] <= predictions["min_btc"]:
                capital += solution["lev_btc"] * solution['x_btc'] * (-losses['btc'])
                print(f"\033[31m you lost {solution['x_btc'] * (-losses['btc'])} in btc \033[0m")

            else:
                capital += solution['x_btc'] * (profits['btc']*0.3)
                accuracy[1] += 1
                print(f"\033[31m you earned {solution['x_btc'] * (profits['btc']*0.3)} in btc \033[0m")


        if buy_or_sell[2]:
            if results["Ethereum"]["min_low"] <= predictions["min_eth"]:
                capital += solution["lev_eth"] * solution['x_eth'] * (+profits['eth'])
                accuracy[2] += 1
                print(f"\033[31m you earned {solution['x_eth'] * (+profits['eth'])} in eth \033[0m")

            elif results["Ethereum"]["max_high"] >= predictions["max_eth"]:
                capital += solution["lev_eth"] * solution['x_eth'] * (-losses['eth'])
                print(f"\033[31m you lost {solution['x_eth'] * (-losses['eth'])} in eth \033[0m")

            else:
                capital += solution['x_eth'] * (profits['eth']*0.3)
                accuracy[2] += 1
                print(f"\033[31m you earned {solution['x_eth'] * (profits['eth']*0.3)} in eth \033[0m")

        else:
            if results["Ethereum"]["max_high"] >= predictions["max_eth"]:
                capital += solution["lev_eth"] * solution['x_eth'] * (profits['eth'])
                accuracy[2] += 1
                print(f"\033[31m you earned {solution['x_eth'] * (+profits['eth'])} in eth \033[0m")

            elif results["Ethereum"]["min_low"] <= predictions["min_eth"]:
                capital += solution["lev_eth"] * solution['x_eth'] * (-losses['eth'])
                print(f"\033[31m you lost {solution['x_eth'] * (-losses['eth'])} in eth \033[0m")

            else:
                capital += solution['x_eth'] * (profits['eth']*0.3)
                accuracy[2] += 1
                print(f"\033[31m you earned {solution['x_eth'] * (profits['eth']*0.3)} in eth \033[0m")


        if solution["x_bond"]:
            capital += solution["x_bond"] * (0.0055/4)
    else:
        print("KIR TO IN ZENDEGI TRADE NEMIKONAM !")

    total_number_of_positions[0] += 1
    total_number_of_positions[1] += 1
    total_number_of_positions[2] += 1

    accuracy[0] = accuracy[0]/total_number_of_positions[0]
    accuracy[1] = accuracy[1]/total_number_of_positions[1]
    accuracy[2] = accuracy[2]/total_number_of_positions[2]

    return results, capital, accuracy, total_number_of_positions


# Example usage:
# today = "2024-01-01"
# capital = 10000
# result, updated_capital = update_capital(today, capital)
# print(result)
