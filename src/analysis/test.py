import pandas as pd
import yfinance as fin
from src.resources import iex_api_requests as iex


ticker = fin.Ticker('AAPL')
all_dates = ticker.quarterly_income_stmt.columns
stock_price = ticker.history(start='2018-05-01', end='2018-05-01')
market_cap = stock_price * total_shares
print(market_cap)