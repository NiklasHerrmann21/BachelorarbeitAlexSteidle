import yfinance as yf

stocks = ["MMM", "AXP", "BA", "CAT", "CVX", "CSCO", "KO","XOM", "HD","INTC","IBM","JNJ","JPM","MCD", "MRK","MSFT","PFE","PG", "TRV","RTX","VZ","WMT","DIS"]
# UTC/UTX has been removed as not possible to retrieve historical data and RTX might not be the right data

sum_of_all=0

for stock in stocks:
    market_data_monthly = yf.download(stock, start="2010-01-01", end="2020-01-01", interval='1mo')
    market_data_monthly = market_data_monthly["Adj Close"].pct_change().dropna()
    for months in range(0, len(market_data_monthly)-1):
        sum_of_all += market_data_monthly.iloc[months]

sum_of_all = sum_of_all / len(stocks) / 12 / 10
print(sum_of_all)
