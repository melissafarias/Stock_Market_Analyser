import requests
import json
import configparser
import pandas as pd
import matplotlib.pyplot as plt # Kept for potential internal use, but plotting is deferred to plotter.py
import time # For rate limiting
from plotter import plot_historical_prices, plot_indicator # Import the plotting functions from the new file

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
        # Uncomment the lines below if you need to see the full raw API response for debugging
        # print("\n--- Raw API Response for Historical Data ---")
        # print(json.dumps(data, indent=2))
        # print("-------------------------------------------\n")
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
                '5. volume': 'volume'
            })
            # Convert relevant columns to numeric, handling potential errors
            numeric_cols = ['open', 'high', 'low', 'close', 'volume']
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce') # Coerce errors to NaN

            # Create 'adjusted_close' column from 'close' for plotting compatibility
            df['adjusted_close'] = df['close']

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

def calculate_sma(df: pd.DataFrame, window: int, column='close'):
    """
    Calculates Simple Moving Average (SMA) for a given DataFrame and window.

    Args:
        df (pd.DataFrame): DataFrame with stock data.
        window (int): The period for the moving average.
        column (str): The column to calculate SMA on (e.g., 'close').

    Returns:
        pd.Series or None: A Series containing the SMA values, or None if input is invalid.
    """
    if df is None or df.empty or column not in df.columns:
        print(f"Error: Cannot calculate SMA. DataFrame is empty or missing '{column}' column.")
        return None
    if window <= 0:
        print("Error: SMA window must be a positive integer.")
        return None
    
    # Ensure the column is numeric before calculating SMA
    df[column] = pd.to_numeric(df[column], errors='coerce')
    sma_series = df[column].rolling(window=window).mean()
    return sma_series.dropna() # Drop NaN values that appear at the beginning of the series

def calculate_rsi(df: pd.DataFrame, window: int = 14, column='close'):
    """
    Calculates the Relative Strength Index (RSI) for a given DataFrame and window.

    Args:
        df (pd.DataFrame): DataFrame with stock data.
        window (int): The period for the RSI calculation (default 14).
        column (str): The column to calculate RSI on (e.g., 'close').

    Returns:
        pd.Series or None: A Series containing the RSI values, or None if input is invalid.
    """
    if df is None or df.empty or column not in df.columns:
        print(f"Error: Cannot calculate RSI. DataFrame is empty or missing '{column}' column.")
        return None
    if window <= 0:
        print("Error: RSI window must be a positive integer.")
        return None

    # Ensure the column is numeric
    df[column] = pd.to_numeric(df[column], errors='coerce')

    delta = df[column].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    rsi_series = 100 - (100 / (1 + rs))
    return rsi_series.dropna() # Drop NaN values

def main():
    """
    Main function to run the Stock Market Data Analyser application.
    """
    print("Welcome to the Stock Market Data Analyser!")
    print("Commands:")
    print("  'quote <symbol>'            - Get real-time stock quote.")
    print("  'history <symbol>'          - Get and plot historical close prices (last 100 days).")
    print("  'sma <symbol> <window>'     - Calculate and plot Simple Moving Average (e.g., 'sma AAPL 50').")
    print("  'rsi <symbol> <window>'     - Calculate and plot Relative Strength Index (e.g., 'rsi AAPL 14').")
    print("  'exit'                      - Quit the application.")

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
                print(f"\n--- Historical Data for {symbol} (Last 5 days) ---")
                print(historical_df.tail())
                plot_historical_prices(historical_df, symbol)
            time.sleep(15) # Alpha Vantage free tier: 5 calls/minute
        elif command == 'sma':
            if len(parts) < 3:
                print("Usage: 'sma <symbol> <window>' (e.g., 'sma AAPL 50').")
                continue
            window_str = parts[2]
            try:
                window = int(window_str)
                if window <= 0:
                    raise ValueError("Window must be a positive integer.")
            except ValueError:
                print(f"Error: Invalid window '{window_str}'. Please provide a positive integer for the window.")
                continue

            historical_df = get_historical_data(symbol, outputsize='full') # Use 'full' for more data for indicators
            if historical_df is not None:
                sma_data = calculate_sma(historical_df, window)
                if sma_data is not None:
                    # Pass original close prices and SMA to the plotter
                    plot_indicator(historical_df['close'], sma_data, symbol, f'SMA ({window} days)')
                else:
                    print(f"Could not calculate SMA for {symbol}.")
            time.sleep(15) # Alpha Vantage free tier: 5 calls/minute
        elif command == 'rsi':
            if len(parts) < 3:
                print("Usage: 'rsi <symbol> <window>' (e.g., 'rsi AAPL 14').")
                continue
            window_str = parts[2]
            try:
                window = int(window_str)
                if window <= 0:
                    raise ValueError("Window must be a positive integer.")
            except ValueError:
                print(f"Error: Invalid window '{window_str}'. Please provide a positive integer for the window.")
                continue

            historical_df = get_historical_data(symbol, outputsize='full') # Use 'full' for more data for indicators
            if historical_df is not None:
                rsi_data = calculate_rsi(historical_df, window)
                if rsi_data is not None:
                    # RSI is typically plotted on a separate subplot
                    plot_indicator(None, rsi_data, symbol, f'RSI ({window} days)', is_rsi=True)
                else:
                    print(f"Could not calculate RSI for {symbol}.")
            time.sleep(15) # Alpha Vantage free tier: 5 calls/minute
        else:
            print("Invalid command. Please use 'quote <symbol>', 'history <symbol>', 'sma <symbol> <window>', 'rsi <symbol> <window>', or 'exit'.")

if __name__ == "__main__":
    main()
