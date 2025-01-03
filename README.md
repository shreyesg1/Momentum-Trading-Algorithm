# Momentum-Based Stock Trading Algorithm

## Short Description
This script implements a momentum-based stock trading strategy, using historical stock data to rank and select top-performing stocks for a simulated portfolio. It calculates momentum scores based on six-month returns and annualized volatility, conducts monthly rebalancing, and backtests portfolio performance over a specified period.

## Overview
This Python script implements a momentum-based stock trading algorithm. The strategy ranks stocks by their momentum score, calculated using the stock's return and volatility, and selects the top performers for a simulated portfolio. The algorithm conducts monthly rebalancing and evaluates portfolio performance over time.

## Features
- **Data Retrieval**: Downloads historical stock price data using Yahoo Finance API.
- **Momentum Scoring**: Computes momentum scores for stocks based on six-month returns and annualized volatility.
- **Top Stock Selection**: Selects the top N stocks by momentum score for portfolio inclusion.
- **Backtesting**: Simulates portfolio performance with monthly rebalancing and equal-weighted allocation.
- **Error Handling**: Incorporates error checking for missing data and unexpected issues during calculations.

## Requirements
- Python 3.8+
- Libraries:
  - `pandas`
  - `numpy`
  - `yfinance`
  - `tqdm`
- Internet access for downloading stock data.

## Installation
1. Clone the repository or copy the script file.
2. Install the required libraries:
   ```bash
   pip install pandas numpy yfinance tqdm
   ```
3. Run the script in your preferred Python environment.

## How to Use
### 1. Define Parameters
Set the following parameters in the script:
- `start_date`: The start date for downloading historical stock data.
- `end_date`: The end date for downloading historical stock data.

### 2. Fetch Tickers
The script fetches tickers of NASDAQ-100 companies from Wikipedia:
```python
ticker_df = pd.read_html("https://en.wikipedia.org/wiki/Nasdaq-100")[4]
```
Modify this section if you wish to use a custom list of tickers.

### 3. Download Stock Data
Historical stock price data is downloaded for the specified tickers and date range:
```python
df = download_data(tickers, start_date, end_date)
```

### 4. Run Backtest
Start the backtest with specified parameters:
```python
portfolio = backtest('2010-01-01', '2024-12-31', df.columns.tolist(), df)
```
Adjust the start and end dates for the backtest as needed.

### 5. View Results
The script prints portfolio performance metrics, including:
- Monthly portfolio value.
- Total return at the end of the period.

Final results are displayed:
```plaintext
Final Results:
Starting Value: $100,000
Final Value: $X,XXX,XXX.XX
Total Return: XX.XX%
Number of months: XXX
```

## Algorithm Details
### Momentum Score Calculation
The momentum score for a stock is computed as:
```plaintext
Momentum Score = (6-month return) / (Annualized Volatility)
```
- **6-month return**: Percentage change over the last 126 trading days.
- **Annualized Volatility**: Standard deviation of daily returns scaled by the square root of 252.

Stocks with insufficient historical data or zero volatility are excluded from the top stock selection.

### Portfolio Rebalancing
- Equal weight allocation is applied to all selected stocks.
- Portfolio is rebalanced monthly, with performance tracked based on next-month returns.

## Notes
- Ensure all tickers are valid and available on Yahoo Finance.
- The script uses six months of historical data for momentum calculation; ensure the start date accommodates this.
- Backtesting results depend on data quality and may not represent actual trading performance.

## Disclaimer
This script is for educational purposes only. It does not constitute financial advice or guarantee profits. Use at your own risk.

