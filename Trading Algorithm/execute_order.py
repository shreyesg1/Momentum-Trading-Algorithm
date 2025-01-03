import alpaca_trade_api as tradeapi
import config
from alpaca.trading.client import TradingClient


# Initialize Alpaca API client
api = tradeapi.REST(config.API_KEY, config.API_SECRET, base_url=config.BASE_URL)

trading_client = TradingClient('config.API_KEY', 'config.API_KEY')



def createMarketOrder(ticker, qty, side, ordertype):
    try:

        # Create market order
        order = api.submit_order(
            symbol=ticker,
            qty=qty,
            side=side,
            type=ordertype,
            time_in_force='day'
        )

        return order
    except tradeapi.rest.APIError as e:
        return f"APIError: {e}"
    except Exception as e:
        return f"Error: {e}"

