import robin_stocks.robinhood as r
import pandas as pd
import numpy as np
import ta as ta
from pandas.plotting import register_matplotlib_converters
from ta import *
from misc import *
from tradingstats import *
from config import *

# Log in to Robinhood
# Put your username and password in a config.py file in the same directory (see sample file)
login = r.login(rh_username,rh_password)

# Safe divide by zero division function
def safe_division(n, d):
    return n / d if d else 0

def get_historicals(ticker, intervalArg, spanArg, boundsArg):
    # If it's a ticker in this program, then it must be a crypto ticker
    history = r.get_crypto_historicals(ticker,interval=intervalArg,span=spanArg,bounds=boundsArg)
    return history

def get_watchlist_symbols():
    """
    Returns: the symbol for each stock in your watchlist as a list of strings
    """
    my_list_names = set()
    symbols = set()

    watchlistInfo = r.get_all_watchlists()
    for watchlist in watchlistInfo['results']:
        listName = watchlist['display_name']
        my_list_names.add(listName)

    for listName in my_list_names:
        watchlist = r.get_watchlist_by_name(name=listName)
        for item in watchlist['results']:
            symbol = item['symbol']
            symbols.add(symbol)

    return symbols

def get_portfolio_symbols():
    """
    Returns: the symbol for each stock in your portfolio as a list of strings
    """
    symbols = []
    holdings_data = r.get_open_stock_positions()
    for item in holdings_data:
        if not item:
            continue
        instrument_data = r.get_instrument_by_url(item.get('instrument'))
        symbol = instrument_data['symbol']
        symbols.append(symbol)
    return symbols

def get_position_creation_date(symbol, holdings_data):
    """Returns the time at which we bought a certain stock in our portfolio

    Args:
        symbol(str): Symbol of the stock that we are trying to figure out when it was bought
        holdings_data(dict): dict returned by r.get_open_stock_positions()

    Returns:
        A string containing the date and time the stock was bought, or "Not found" otherwise
    """
    instrument = r.get_instruments_by_symbols(symbol)
    url = instrument[0].get('url')
    for dict in holdings_data:
        if(dict.get('instrument') == url):
            return dict.get('created_at')
    return "Not found"

def get_modified_holdings():
    """ Retrieves the same dictionary as r.build_holdings, but includes data about
        when the stock was purchased, which is useful for the read_trade_history() method
        in tradingstats.py

    Returns:
        the same dict from r.build_holdings, but with an extra key-value pair for each
        position you have, which is 'bought_at': (the time the stock was purchased)
    """
    holdings = r.build_holdings()
    holdings_data = r.get_open_stock_positions()
    for symbol, dict in holdings.items():
        bought_at = get_position_creation_date(symbol, holdings_data)
        bought_at = str(pd.to_datetime(bought_at))
        holdings[symbol].update({'bought_at': bought_at})
    return holdings

def sell_holdings(symbol, holdings_data):
    """ Place an order to sell all holdings of a stock.

    Args:
        symbol(str): Symbol of the stock we want to sell
        holdings_data(dict): dict obtained from get_modified_holdings() method
    """
    shares_owned = int(float(holdings_data[symbol].get("quantity")))
    if not debug:
        r.order_sell_market(symbol, shares_owned)
    print("####### Selling " + str(shares_owned) + " shares of " + symbol + " #######")

def buy_holdings(potential_buys, profile_data, holdings_data):
    """ Places orders to buy holdings of stocks. This method will try to order
        an appropriate amount of shares such that your holdings of the stock will
        roughly match the average for the rest of your portfoilio. If the share
        price is too high considering the rest of your holdings and the amount of
        buying power in your account, it will not order any shares.

    Args:
        potential_buys(list): List of strings, the strings are the symbols of stocks we want to buy
        symbol(str): Symbol of the stock we want to sell
        holdings_data(dict): dict obtained from r.build_holdings() or get_modified_holdings() method
    """
    cash = float(profile_data.get('cash'))
    portfolio_value = float(profile_data.get('equity')) - cash
    ideal_position_size = (safe_division(portfolio_value, len(holdings_data))+cash/len(potential_buys))/(2 * len(potential_buys))
    prices = r.get_latest_price(potential_buys)
    for i in range(0, len(potential_buys)):
        stock_price = float(prices[i])
        if(ideal_position_size < stock_price < ideal_position_size*1.5):
            num_shares = int(ideal_position_size*1.5/stock_price)
        elif (stock_price < ideal_position_size):
            num_shares = int(ideal_position_size/stock_price)
        else:
            print("####### Tried buying shares of " + potential_buys[i] + ", but not enough buying power to do so#######")
            break
        print("####### Buying " + str(num_shares) + " shares of " + potential_buys[i] + " #######")
        if not debug:
            r.order_buy_market(potential_buys[i], num_shares)



def scan_stocks():
    if debug:
        print("----- DEBUG MODE -----\n")
    print("----- Starting scan... -----\n")
    register_matplotlib_converters()
    watchlist_symbols = get_watchlist_symbols()
    portfolio_symbols = get_portfolio_symbols()
    holdings_data = get_modified_holdings()
    potential_buys = []
    sells = []
    print("Current Portfolio: " + str(portfolio_symbols) + "\n")
    print("Current Watchlist: " + str(watchlist_symbols) + "\n")
    print("----- Scanning portfolio for assets to sell -----\n")
    # Add your own selling logic here

    profile_data = r.build_user_profile()
    print("\n----- Scanning watchlist for assets to buy -----\n")
    # Add your own buying logic here

    if(len(potential_buys) > 0):
        buy_holdings(potential_buys, profile_data, holdings_data)
    if(len(sells) > 0):
        update_trade_history(sells, holdings_data, "tradehistory.txt")
    print("----- Scan over -----\n")
    if debug:
        print("----- DEBUG MODE -----\n")

# Execute the scan
# scan_stocks()
# get_historicals("DOGE", "15second", "month", "24_7")
# print(r.get_crypto_historicals(symbol="DOGE",interval="15second",span="month",bounds="24_7"))





# Organize cash and DOGE into tiers

# if-statements for buying
# if tier_buy_price >= actual_price:
# if cash in tier > 0:
# limit_buy_order() for amount of cash in tier
# if-statements for selling
# if tier_sell_price >= actual_price:
# if DOGE in tier:
# imit_sell_order() for amount of DOGE in tier

def jm_trading_strategy():  # Here is my own trading strategy code --Jonathan McCormick:
    actively_trading = True
    while actively_trading == True:

        # Gather price info on DOGE.
        doge_quote = r.get_crypto_quote("DOGE")
        doge_ask_price, doge_bid_price = doge_quote["ask_price"], doge_quote["bid_price"]
        print("DOGE ask price:", doge_ask_price, "\nDOGE bid price:", doge_bid_price)

        # Check my USD available for trading.
        my_theoretical_buying_power = r.load_account_profile()["buying_power"]
        savings_amount = 20  # This is off-limits for trading. Value is measured in USD.
        my_usd_to_trade = float(my_theoretical_buying_power) - savings_amount  # My real tradable buying power.
        print("My USD trading supply: $", my_usd_to_trade)

        # Check my DOGE available for trading.
        my_crypto_positions = r.get_crypto_positions()
        my_doge_to_trade = float(my_crypto_positions[2]["quantity_available"])
        print("My DOGE trading supply: Ð", my_doge_to_trade)

        # Create tiers.
        num_of_tiers = 100
        tiers = []
        tier_increment_size = 0.01  # Value in USD
        tier_buy_price = 0.01  # The lowest price I expect DOGE to go (for these purposes)
        tier_sell_price = tier_buy_price + tier_increment_size

        tier_counter = 0

        while num_of_tiers > tier_counter:
            tiers.append("Tier " + str(tier_counter))
            tier_counter += 1

        tier_dictionary = {}
        for tier in tiers:

            tier_doge_supply = my_doge_to_trade / num_of_tiers
            tier_usd_supply = my_usd_to_trade / num_of_tiers


            tier_dictionary[tier] = [tier_buy_price, tier_sell_price, tier_doge_supply, tier_usd_supply]
            tier_buy_price += tier_increment_size
            tier_sell_price += tier_increment_size




        print(tier_dictionary)
        print("DOGE supply per tier: " + str(tier_doge_supply) + "\nUSD supply per tier:" + str(tier_usd_supply))

        for tier in tier_dictionary:

            # Math.
            def doge_buy(amountInDollars, limitPrice):
                r.order_buy_crypto_limit_by_price('DOGE', amountInDollars, limitPrice, timeInForce='gfd', jsonify=True)

            def doge_sell(amountInDollars, limitPrice):
                r.order_sell_crypto_limit_by_price('DOGE', amountInDollars, limitPrice, timeInForce='gfd', jsonify=True)

            # if seller price is less than your buying price, then place a limit buy order for 1 DOGE
            if doge_ask_price <= tier[0]:
                amount_of_doge_to_buy = 1 / float(tier[0])
                print(amount_of_doge_to_buy)
                #doge_buy(tier_dictionary[tier_usd_supply], tier_buy_price)

            # if buyer price is more than your selling price, then place a limit sell order for 1 DOGE
            """if doge_bid_price > tier[1]:

                doge_sell(doge, ___)"""
            # Assign USD to tiers.
            #usd_per_tier = my_usd_to_trade / num_of_tiers

            # Assign DOGE to tiers.

            # Execute orders
            
            """
            Consider whether or not to have some sort of emergency stop switch which will trigger if the net account value falls x% within x amount of time.
            You can always resume the bot manually. 
            """

        # Record data
        if(len(sells) > 0):
            update_trade_history(sells, holdings_data, "tradehistory.txt")

    return "Exited trading for now."
jm_trading_strategy()
# This is a comment
