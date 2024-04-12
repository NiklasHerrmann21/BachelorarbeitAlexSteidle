import pandas as pd
import yfinance as fin
from src.resources import iex_api_requests as iex


def calculate_bm_ratio(market_cap, book_value):
    try:
        pb_ratio = market_cap / book_value
        return pb_ratio
    except ZeroDivisionError:
        return None


def main():
    # Define the Dow 30 companies as of 2010
    dow_30_companies = ["MSFT"]

    # Define your API token for IEX Cloud
    iex_cloud_api_token = "pk_f28886bab3cc4f22ba8a1adf16ac912c"

    # Create a dictionary to store results
    results = {}


    # Loop through each company
    for company in dow_30_companies:
        # Get the data from IEX Cloud API
        data = iex.get_latest_balance_sheets_by_years(company, 20)
        ticker = fin.Ticker(company)


        if data is not None and 'balancesheet' in data:
            # Filter balance sheet data for the specific year (2010)
            for entry in data['balancesheet']:
                for year in range(2023, 2024):
                    if 'fiscalYear' in entry and entry['fiscalYear'] == year:
                        # Extract balancesheet data
                        total_assets = entry['totalAssets']
                        total_liabilities = entry['totalLiabilities']

                        # Get historical data for the specific date
                        numberOfShares = ticker.get_shares_full(start=f"{year}-01-01", end=None)[0]

                        # Calculate book value
                        book_value = total_assets - total_liabilities
                        result = fin.download(company, start=f"{year}-05-01", end=f"{year}-05-02")
                        market_cap_fin = result['Close'][0] * numberOfShares
                       # market_cap = entry['marketCap']

                        # Calculate B/M ratio
                        bm_ratio = calculate_bm_ratio(book_value,market_cap_fin)

                        if company not in results:
                            results[company] = {}
                        results[company][year] = {"Market Cap": market_cap_fin, "Book Value": book_value,
                                                  "P/B Ratio": bm_ratio}
        else:
            print(f"No balancesheet data found for {company}")

    # Create DataFrame from the results
    df = pd.DataFrame.from_dict({(i, j): results[i][j]
                                 for i in results.keys()
                                 for j in results[i].keys()},
                                orient='index')

    # Display the DataFrame
    pd.options.display.float_format = '${:,.2f}'.format
    print(df)


if __name__ == "__main__":
    main()
