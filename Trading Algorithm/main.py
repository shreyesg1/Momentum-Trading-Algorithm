from dateutil.utils import today
import algorithm as alg
from execute_order import createMarketOrder, trading_client

account = trading_client.get_account()
balance = float(account.cash)  # Available cash
print(f"Account balance: ${balance:.2f}")

# Find current holdings
def fetch_current_holdings():
    positions = trading_client.get_all_positions()
    return {pos.symbol: int(pos.qty) for pos in positions}


current_holdings = fetch_current_holdings()
print(f"Current holdings: {current_holdings}")

# Find top stocks
top_stocks = alg.get_top_stocks(today(), alg.tickers, alg.df)
print(f"Top stocks: {top_stocks}")

# Calculate target quantities
def quantity(stocks, total_money):
    """Calculate target quantities based on the available cash."""
    amount_per_stock = total_money / len(stocks)  # Equal allocation per stock
    quantities = {}

    for stock in stocks:
        current_price = alg.df[stock].iloc[-1]  # Get the latest closing price
        if current_price > 0:
            quantities[stock] = int(amount_per_stock // current_price)
        else:
            print(f"Invalid price for {stock}. Skipping.")
            quantities[stock] = 0

    return quantities

required_quantities = quantity(top_stocks, float(account.equity))
print(f"Target quantities: {required_quantities}")

# Execute buy and sell orders
def execute_orders(required_quantities, current_holdings, available_cash):
    for stock, target_qty in required_quantities.items():
        held_qty = current_holdings.get(stock, 0)  # Get the currently held quantity
        current_price = alg.df[stock].iloc[-1]  # Get the latest closing price

        if held_qty < target_qty:  # Need to buy more shares
            qty_to_buy = target_qty - held_qty
            cost = qty_to_buy * current_price
            if qty_to_buy > 0 and cost <= available_cash:  # Ensure enough cash is available
                print(f"Buying {qty_to_buy} shares of {stock} for ${cost:.2f}")
                order = createMarketOrder(stock, qty_to_buy, 'buy', 'market')
                print(order)
                current_holdings[stock] = held_qty + qty_to_buy
                available_cash -= cost
            else:
                print(f"Insufficient funds to buy {qty_to_buy} shares of {stock}.")

        elif held_qty > target_qty:  # Need to sell excess shares
            qty_to_sell = held_qty - target_qty
            revenue = qty_to_sell * current_price
            if qty_to_sell > 0:
                print(f"Selling {qty_to_sell} shares of {stock} for ${revenue:.2f}")
                order = createMarketOrder(stock, qty_to_sell, 'sell', 'market')
                print(order)
                current_holdings[stock] = held_qty - qty_to_sell
                available_cash += revenue

        else:
            print(f"No action needed for {stock}. Held quantity matches target quantity.")

    print(f"Updated holdings: {current_holdings}")
    print(f"Remaining cash: ${available_cash:.2f}")
    return available_cash, current_holdings

# Execute the orders
balance, current_holdings = execute_orders(required_quantities, current_holdings, balance)

