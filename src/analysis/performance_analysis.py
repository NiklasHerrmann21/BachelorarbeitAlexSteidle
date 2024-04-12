import pandas as pd
import yfinance as yf
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Define a function to save DataFrame to CSV
def save_to_csv(file_name, dataframe):
    dataframe.to_csv(file_name, index=True)

# Define the list of stocks
stocks = ["AAPL", "AXP", "BA", "CAT", "CSCO", "CVX", "DIS",  "IBM", "INTC",
          "JNJ", "JPM", "KO", "MCD", "MMM", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV",
          "V", "VZ", "WMT", "XOM"]

# Download historical data for S&P 500
market_data = yf.download("SPY", start="2010-01-01", end="2019-12-31", progress=False)
market_data = market_data["Adj Close"].pct_change().dropna()

# Create empty DataFrames to store beta and returns
betas = pd.DataFrame(index=stocks, columns=["Beta"])
stock_returns = pd.DataFrame(index=market_data.index, columns=stocks)

# Calculate Beta for Each Stock
for stock in stocks:
    stock_data = yf.download(stock, start="2010-01-01", end="2019-12-31", progress=False)
    stock_data = stock_data.Close.pct_change().dropna()

    # Merge stock data with market data
    combined_data = pd.concat([stock_data, market_data], axis=1).dropna()
    combined_data.columns = ["Stock Returns", "Market Returns"]

    X = sm.add_constant(combined_data["Market Returns"])
    model = sm.OLS(combined_data["Stock Returns"], X).fit()

    betas.loc[stock, "Beta"] = model.params.iloc[1]

# Save Beta calculations to CSV
save_to_csv("betas.csv", betas)

# Calculate Market Returns
market_returns = yf.download("SPY", start="2010-01-01", end="2019-12-31", progress=False)
market_returns = market_returns.Close.pct_change().dropna()

# Calculate Stock Returns
for stock in stocks:
    stock_data = yf.download(stock, start="2010-01-01", end="2019-12-31", progress=False)
    stock_returns[stock] = stock_data.Close.pct_change().dropna()

# Calculate average market beta
avg_market_beta = betas["Beta"].mean()

# Refine High and Low Beta Criteria
high_beta_stocks = betas[betas["Beta"] > 1.3 * avg_market_beta].index
low_beta_stocks = betas[betas["Beta"] < 0.7 * avg_market_beta].index

# Calculate new portfolios
high_beta_portfolio = stock_returns[high_beta_stocks].mean(axis=1)
low_beta_portfolio = stock_returns[low_beta_stocks].mean(axis=1)

# Calculate BAB Strategy Return
bab_strategy_return = low_beta_portfolio - high_beta_portfolio

# Save BAB Strategy Return to CSV
bab_strategy_df = pd.DataFrame(bab_strategy_return, columns=["BAB Strategy Return"])
save_to_csv("bab_strategy_return.csv", bab_strategy_df)

# Calculate Cumulative Returns
cumulative_market_return = (1 + market_returns).cumprod() - 1
cumulative_bab_strategy_return = (1 + bab_strategy_return).cumprod() - 1

# Calculate Average Annualized Returns
average_annual_return_bab = (1 + bab_strategy_return.mean()) ** (1/10) - 1
average_annual_return_market = (1 + market_returns.mean()) ** (1/10) - 1

# Save Cumulative Returns to CSV
cumulative_returns = pd.DataFrame({
    "Cumulative Market Returns": cumulative_market_return,
    "Cumulative BAB Strategy Returns": cumulative_bab_strategy_return
})
save_to_csv("cumulative_returns.csv", cumulative_returns)

# Plotting the Cumulative Returns
plt.figure(figsize=(10, 6))
plt.plot(cumulative_market_return, label="S&P 500 Market Returns", linewidth=2)
plt.plot(cumulative_bab_strategy_return, label="Betting Against Beta (BAB) Strategy", linewidth=2)
plt.title("Cumulative Returns - BAB Strategy vs. S&P 500")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Print the results
print("Average Annualized Returns - BAB Strategy:", average_annual_return_bab)
print("Average Annualized Returns - S&P 500:", average_annual_return_market)

# Performance Comparison
strategy_outperformed = average_annual_return_bab > average_annual_return_market
print("Did the BAB Strategy outperform the S&P 500?", strategy_outperformed)
