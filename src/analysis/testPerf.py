import pandas as pd
import yfinance as yf
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Define the list of stocks
stocks = ["AAPL", "AXP", "BA", "CAT", "CSCO", "CVX", "DIS", "DOW", "GS", "HD", "IBM", "INTC",
          "JNJ", "JPM", "KO", "MCD", "MMM", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV", "UNH",
          "V", "VZ", "WMT", "XOM"]

# Download historical data for S&P 500
market_data = yf.download("^GSPC", start="2010-01-01", end="2019-12-31")
market_data = market_data["Adj Close"].pct_change().dropna()

# Create empty DataFrames to store beta and returns
betas = pd.DataFrame(index=stocks, columns=["Beta"])
stock_returns = pd.DataFrame(index=market_data.index, columns=stocks)

# Calculate Beta for Each Stock
for stock in stocks:
    stock_data = yf.download(stock, start="2010-01-01", end="2019-12-31")
    stock_data = stock_data["Adj Close"].pct_change().dropna()

    # Merge stock data with market data
    combined_data = pd.concat([stock_data, market_data], axis=1).dropna()
    combined_data.columns = ["Stock Returns", "Market Returns"]

    X = sm.add_constant(combined_data["Market Returns"])
    model = sm.OLS(combined_data["Stock Returns"], X).fit()

    betas.loc[stock, "Beta"] = model.params.iloc[1]

# Calculate Market Returns
market_returns = yf.download("^GSPC", start="2010-01-01", end="2019-12-31")
market_returns = market_returns["Adj Close"].pct_change().dropna()

# Calculate Stock Returns
for stock in stocks:
    stock_data = yf.download(stock, start="2010-01-01", end="2019-12-31")
    stock_returns[stock] = stock_data["Adj Close"].pct_change().dropna()

# Create High Beta and Low Beta Portfolios
high_beta_stocks = betas[betas["Beta"] > 1].index
low_beta_stocks = betas[betas["Beta"] < 1].index

high_beta_portfolio = stock_returns[high_beta_stocks].mean(axis=1)
low_beta_portfolio = stock_returns[low_beta_stocks].mean(axis=1)

# Calculate BAB Strategy Return
bab_strategy_return = low_beta_portfolio - high_beta_portfolio


# Calculate Cumulative Returns
cumulative_market_return = (1 + market_returns).cumprod() - 1
cumulative_bab_strategy_return = (1 + bab_strategy_return).cumprod() - 1


# Plotting the Cumulative Returns
#plt.figure(figsize=(10, 6))
#plt.plot(cumulative_market_return, label="S&P 500 Market Returns", linewidth=2)
#plt.plot(cumulative_bab_strategy_return, label="Betting Against Beta (BAB) Strategy", linewidth=2)
#plt.title("Cumulative Returns - BAB Strategy vs. S&P 500")
#plt.xlabel("Date")
#plt.ylabel("Cumulative Return")
#plt.legend()
#plt.grid(True)
#plt.tight_layout()
#plt.show()

print(cumulative_market_return)
print(cumulative_bab_strategy_return)
