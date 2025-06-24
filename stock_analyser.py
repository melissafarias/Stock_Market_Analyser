import requests
import json
import configparser


# --- API Key Configuration ---
# It's recommended to store API keys in a separate configuration file (e.g., config.ini)
config = configparser.ConfigParser()
try:
    config.read('config.ini')
    API_KEY = config['api_keys']['alpha_vantage_key']
except FileNotFoundError:
    print("Error: config.ini not found. Please create it with your API key.")
    API_KEY = None # Set to None to prevent further execution without a key
except KeyError:
    print("Error: 'alpha_vantage_key' not found in config.ini under '[api_keys]' section.")
    API_KEY = None # Set to None
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
    if API_KEY is None: # Change this check
        print("API key not loaded. Please ensure config.ini is correctly set up.")
        return None

    # Function: GLOBAL_QUOTE provides real-time stock data
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": API_KEY
    }
    print(f"Fetching data for symbol: {symbol} from Alpha Vantage...")
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        # Alpha Vantage returns an empty dictionary or an error message if symbol not found
        if "Global Quote" in data and data["Global Quote"]:
            return data["Global Quote"]
        elif "Error Message" in data:
            print(f"API Error for '{symbol}': {data['Error Message']}")
        else:
            print(f"No data found for symbol '{symbol}'. Please check the symbol.")
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

def display_stock_info(stock_data):
    """
    Displays key information about a stock in a user-friendly format.

    Args:
        stock_data (dict): A dictionary containing the stock's quote data.
    """
    if not stock_data:
        return

    # Alpha Vantage returns keys like '01. symbol', '05. price'
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
    print("Type 'exit' to quit.")

    while True:
        symbol = input("\nEnter stock ticker symbol (e.g., AAPL, MSFT): ").strip().upper()
        if symbol == 'EXIT':
            print("Exiting Stock Market Data Analyser. Goodbye!")
            break

        if not symbol:
            print("Please enter a stock symbol.")
            continue

        data = get_stock_quote(symbol)
        if data:
            display_stock_info(data)

if __name__ == "__main__":
    main()
