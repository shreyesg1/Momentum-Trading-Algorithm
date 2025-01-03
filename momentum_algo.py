import pandas as pd
import numpy as np
import yfinance as yf
from tqdm import tqdm

def download_data(tickers, start_date, end_date):
    """Download stock data with a progress bar."""
    from tqdm import tqdm
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

def backtest(start_date, end_date, tickers, df):
    """Backtest with monthly rebalancing."""
    portfolio_value = 100000 # Start with $100,000
    portfolio = pd.DataFrame(index=df.index, columns=['Portfolio Value'])
    
    current_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    while current_date <= end_date:
        try:
            # Get top stocks
            top_stocks = get_top_stocks(current_date, tickers, df)
            
            if not top_stocks:
                print(f"No stocks selected for {current_date}")
                current_date += pd.DateOffset(months=1)
                continue
            
            # Get next month
            next_month = current_date + pd.DateOffset(months=1)
            if next_month not in df.index:
                next_month = df.index[df.index.searchsorted(next_month)]
            
            # Calculate returns (equal weight)
            returns = []
            position_size = 1.0 / len(top_stocks)
            for stock in top_stocks:
                try:
                    current_price = df[stock].loc[current_date]
                    next_price = df[stock].loc[next_month]
                    
                    if pd.isna(current_price) or pd.isna(next_price):
                        print(f"Skipping {stock} due to missing data.")
                        returns.append(0)
                    else:
                        stock_return = next_price / current_price - 1
                        returns.append(stock_return * position_size)
                except Exception as e:
                    print(f"Error calculating return for {stock}: {e}")
                    returns.append(0)
            
            # Update portfolio
            portfolio_return = sum(returns)
            portfolio_value *= (1 + portfolio_return)
            portfolio.loc[next_month] = portfolio_value
            
            print(f"Date: {next_month.strftime('%Y-%m-%d')}, Portfolio Value: ${portfolio_value:,.2f}, Return: {portfolio_return:.2%}")
            
            current_date = next_month
        
        except Exception as e:
            print(f"Error in backtest at {current_date}: {str(e)}")
            current_date += pd.DateOffset(months=1)
    
    return portfolio.dropna()

# Date range for data
start_date = '2016-01-01'
end_date = '2025-01-01'

print("Fetching NASDAQ-100 tickers...")
ticker_df = pd.read_html("https://en.wikipedia.org/wiki/Nasdaq-100")[4]
tickers = [ticker.replace('.', '-') for ticker in ticker_df['Symbol'].to_list()]

df = download_data(tickers, start_date, end_date)

# Run backtest
print("Running backtest...")
portfolio = backtest('2010-01-01', '2024-12-31', df.columns.tolist(), df)

# Calculate final return
final_return = portfolio['Portfolio Value'].iloc[-1] / 100000

print(f"\nFinal Results:")
print(f"Starting Value: $100,000")
print(f"Final Value: ${portfolio['Portfolio Value'].iloc[-1]:,.2f}")
print(f"Total Return: {(final_return - 1) * 100:.2f}%")
print(f"Number of months: {len(portfolio)}")
