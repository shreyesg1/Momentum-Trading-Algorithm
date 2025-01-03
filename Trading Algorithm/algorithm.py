import pandas as pd
import numpy as np
import yfinance as yf
from tqdm import tqdm


def download_data(tickers, start_date, end_date):
    all_data = {}  # Dictionary to store data for each ticker
    for ticker in tqdm(tickers, desc="Downloading data"):
        try:
            # Download the close prices
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)['Close']
            if not data.empty:  # Only add if data is valid
                all_data[ticker] = data
        except Exception as e:
            print(f"Error downloading data for {ticker}: {e}")

    # Combine all series into one df
    if all_data:
        df = pd.concat(all_data, axis=1)
        df.columns = all_data.keys()
    else:
        raise ValueError("No valid data downloaded for any ticker.")

    return df


def calculate_momentum_score(df, stock, date, min_history=126):
    """Calculate momentum score with detailed error logging."""
    try:
        # Get stock data up to the date
        stock_data = df[stock].loc[:date]

        # Check for minimum data
        if len(stock_data) < min_history:
            return float('-inf')

        # Calculate 6-month return
        returns_6m = stock_data.pct_change(periods=126, fill_method=None).iloc[-1]

        # Calculate volatility
        vol = stock_data.pct_change(fill_method=None).std() * np.sqrt(252)

        if vol == 0 or np.isnan(returns_6m) or np.isnan(vol):
            return float('-inf')

        # Calculate simple momentum score
        momentum_score = returns_6m / vol

        return momentum_score
    except Exception as e:
        print(f"Error calculating momentum for {stock}: {str(e)}")
        return float('-inf')


def get_top_stocks(date, tickers, df, min_stocks=10):
    """Get top stocks with error checking."""
    momentum_scores = {}

    for ticker in tickers:
        score = calculate_momentum_score(df, ticker, date)
        momentum_scores[ticker] = score

    # Sort stocks by momentum score
    sorted_stocks = sorted(momentum_scores.items(), key=lambda x: x[1], reverse=True)

    # Take top stocks
    top_stocks = [stock[0] for stock in sorted_stocks[:min_stocks]]
    return top_stocks

# Date range for data
start_date = '2023-12-31'
end_date = '2024-12-31'

print("Fetching NASDAQ-100 tickers...")
ticker_df = pd.read_html("https://en.wikipedia.org/wiki/Nasdaq-100")[4]
tickers = [ticker.replace('.', '-') for ticker in ticker_df['Symbol'].to_list()]

df = download_data(tickers, start_date, end_date)