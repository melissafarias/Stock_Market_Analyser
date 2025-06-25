import requests
import json
import configparser
import pandas as pd
import matplotlib.pyplot as plt # Keep this import here for now, as get_historical_data might still benefit from pandas/matplotlib type definitions
import time # For rate limiting
from plotter import plot_historical_prices # Import the plotting function from the new file

# --- API Key Configuration ---
config = configparser.ConfigParser()
try:
    config.read('config.ini')
    API_KEY = config['api_keys']['alpha_vantage_key']
except FileNotFoundError:
    print("Error: config.ini not found. Please create it with your API key.")
    API_KEY = None
except KeyError:
    print("Error: 'alpha_vantage_key' not found in config.ini under '[api_keys]' section.")
    API_KEY = None
# --- End API Key Configuration ---

BASE_URL = "https://www.alphavantage.co/query"

def get_stock_quote(symbol):
    """
    Fetches real-time stock quote data for a given stock symbol from Alpha Vantage.

    Args:
        symbol (str): The stock ticker symbol (e.g., "IBM", "AAPL").

    Returns:
        dict or None: A dictionary containing the stock's quote data if found,
                      otherwise None.
    """
    if API_KEY is None:
        print("API key not loaded. Please ensure config.ini is correctly set up.")
        return None

    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": API_KEY
    }
    print(f"Fetching real-time data for symbol: {symbol} from Alpha Vantage...")
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "Global Quote" in data and data["Global Quote"]:
            return data["Global Quote"]
        elif "Error Message" in data:
            print(f"API Error for '{symbol}': {data['Error Message']}")
        else:
            print(f"No real-time data found for symbol '{symbol}'. Please check the symbol.")
        return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}. Please check your internet connection.")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}. The request took too long.")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred during API request: {req_err}")
    return None

def get_historical_data(symbol, outputsize='compact'):
    """
    Fetches historical daily **unadjusted** closing price data for a given stock symbol.
    NOTE: TIME_SERIES_DAILY_ADJUSTED is a premium endpoint for Alpha Vantage.
    This function uses TIME_SERIES_DAILY (unadjusted) for free tier compatibility.

    Args:
        symbol (str): The stock ticker symbol (e.g., "IBM", "AAPL").
        outputsize (str): 'compact' returns last 100 data points, 'full' returns all.

    Returns:
        pd.DataFrame or None: A DataFrame containing historical data, or None if error.
    """
    if API_KEY is None:
        print("API key not loaded. Please ensure config.ini is correctly set up.")
        return None

    params = {
        # Changed from "TIME_SERIES_DAILY_ADJUSTED" to "TIME_SERIES_DAILY"
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": outputsize,
        "apikey": API_KEY
    }
    print(f"Fetching historical data for symbol: {symbol} from Alpha Vantage (outputsize={outputsize})...")
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # --- DEBUGGING STEP: Print the raw API response ---
        print("\n--- Raw API Response for Historical Data ---")
        print(json.dumps(data, indent=2))
        print("-------------------------------------------\n")
        # --- END DEBUGGING STEP ---


        if "Time Series (Daily)" in data:
            # Convert to pandas DataFrame
            df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient='index')
            df.index = pd.to_datetime(df.index)
            # Rename columns for easier access and convert to numeric
            df = df.rename(columns={
                '1. open': 'open',
                '2. high': 'high',
                '3. low': 'low',
                '4. close': 'close',
                '5. volume': 'volume', # 'adjusted close' and 'dividend amount' might not be present with TIME_SERIES_DAILY
                '6. volume': 'volume' # This might need to be '5. volume'
            })
            # Adjust column names and conversions based on TIME_SERIES_DAILY response
            # TIME_SERIES_DAILY typically has: '1. open', '2. high', '3. low', '4. close', '5. volume'
            # 'adjusted_close', 'dividend_amount', 'split_coefficient' are not typically included.
            numeric_cols = ['open', 'high', 'low', 'close', 'volume'] # Updated numeric columns
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce') # Coerce errors to NaN

            # If 'adjusted_close' is needed for plotting, you'll need to use 'close' instead
            # or handle the absence. For plotting, we'll now use 'close'
            df['adjusted_close'] = df['close'] # Create 'adjusted_close' column from 'close' for plotting compatibility


            df = df.sort_index() # Sort by date ascending
            return df
        elif "Error Message" in data:
            print(f"API Error for historical data '{symbol}': {data['Error Message']}")
        else:
            print(f"No historical data found for symbol '{symbol}'. Please check the symbol or API limits.")
        return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred fetching historical data: {http_err} - Status Code: {response.status_code}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred fetching historical data: {conn_err}. Please check your internet connection.")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred fetching historical data: {timeout_err}. The request took too long.")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred during historical data API request: {req_err}")
    return None

def display_stock_info(stock_data):
    """
    Displays key information about a stock in a user-friendly format.
    """
    if not stock_data:
        return

    symbol = stock_data.get('01. symbol', 'N/A')
    open_price = stock_data.get('02. open', 'N/A')
    high_price = stock_data.get('03. high', 'N/A')
    low_price = stock_data.get('04. low', 'N/A')
    price = stock_data.get('05. price', 'N/A')
    volume = stock_data.get('06. volume', 'N/A')
    latest_trading_day = stock_data.get('07. latest trading day', 'N/A')
    previous_close = stock_data.get('08. previous close', 'N/A')
    change = stock_data.get('09. change', 'N/A')
    change_percent = stock_data.get('10. change percent', 'N/A')

    print("\n--- Stock Information ---")
    print(f"Symbol: {symbol}")
    print(f"Current Price: ${price}")
    print(f"Open: ${open_price}")
    print(f"High: ${high_price}")
    print(f"Low: ${low_price}")
    print(f"Volume: {volume}")
    print(f"Latest Trading Day: {latest_trading_day}")
    print(f"Previous Close: ${previous_close}")
    print(f"Change: ${change}")
    print(f"Change Percent: {change_percent}")


def main():
    """
    Main function to run the Stock Market Data Analyser application.
    """
    print("Welcome to the Stock Market Data Analyser!")
    print("Commands: 'quote <symbol>', 'history <symbol>', 'exit'")
    print("Example: 'quote AAPL' or 'history GOOGL'")

    while True:
        user_input = input("\nEnter command: ").strip().lower()
        parts = user_input.split()
        command = parts[0] if parts else ''
        symbol = parts[1].upper() if len(parts) > 1 else ''

        if command == 'exit':
            print("Exiting Stock Market Data Analyser. Goodbye!")
            break
        elif command == 'quote':
            if not symbol:
                print("Please provide a stock symbol for 'quote' command (e.g., 'quote AAPL').")
                continue
            data = get_stock_quote(symbol)
            if data:
                display_stock_info(data)
        elif command == 'history':
            if not symbol:
                print("Please provide a stock symbol for 'history' command (e.g., 'history GOOGL').")
                continue
            historical_df = get_historical_data(symbol)
            if historical_df is not None:
                # Display a few rows of historical data
                print(f"\n--- Historical Data for {symbol} (Last 5 days) ---")
                print(historical_df.tail())
                # Call the plotting function from the new plotter module
                plot_historical_prices(historical_df, symbol)
            # Add a small delay to respect API rate limits (5 calls/minute for free tier)
            time.sleep(15) # Wait 15 seconds after a historical data call
        else:
            print("Invalid command. Please use 'quote <symbol>', 'history <symbol>', or 'exit'.")

if __name__ == "__main__":
    main()
