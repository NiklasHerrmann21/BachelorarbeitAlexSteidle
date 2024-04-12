import requests
import yfinance as yf

api_token = "pk_f28886bab3cc4f22ba8a1adf16ac912c"


def get_latest_balance_sheets_by_years(comp_symbol, years):
    url = f"https://cloud.iexapis.com/stable/stock/{comp_symbol}/balance-sheet?period=annual&last={years}&token={api_token}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error retrieving data from IEX Cloud API for {comp_symbol}")
        return None

def get_historical_data_by_years(comp_symbol, fromDate, toDate):
    url = f"https://cloud.iexapis.com/stable/stock/{comp_symbol}/chart/date/{fromDate}?chartByDay=true&token={api_token}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error retrieving data from IEX Cloud API for {comp_symbol}")
        return None



def get_market_cap(company,year):
    data = yf.download(company, start=f"{year}-01-01", end=f"{year}-12-31")

    # Calculate Market Cap
    data["Market Cap"] = data["Adj Close"] * data["Volume"]