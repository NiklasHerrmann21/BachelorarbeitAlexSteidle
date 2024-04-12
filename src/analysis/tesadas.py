import pandas as pd
import yfinance as yf
import statsmodels.api as sm
import matplotlib.pyplot as plt

stocks = ["AAPL", "AXP", "BA", "CAT", "CSCO", "CVX", "DIS",  "IBM", "INTC",
          "JNJ", "JPM", "KO", "MCD", "MMM", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV",
          "V", "VZ", "WMT", "XOM"]

sum_of_all=0
test=[]


for month in range(0,5):
    for stock in stocks:
        market_data_monthly = yf.download(stock, start="2010-01-01", end="2010-12-31", interval='1mo')
        market_data_monthly = market_data_monthly["Adj Close"].pct_change().dropna()

        test[month] += market_data_monthly[month]
        sum_of_all += market_data_monthly[0]

print(sum_of_all)
print(test)
