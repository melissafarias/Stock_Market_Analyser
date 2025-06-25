Stock Market Data Analyser
A Python command-line tool designed to fetch and display real-time stock quotes, historical price data, and technical indicators using the Alpha Vantage API. This project serves as a practical demonstration of API integration, data handling, technical analysis, and command-line application development in Python.

Features
Real-time Stock Quotes: Fetches current price, open, high, low, volume, and other key metrics for any valid stock ticker symbol.

Historical Price Data: Retrieves daily unadjusted historical closing prices for a given stock symbol.

Note: Due to Alpha Vantage free tier limitations, the historical data retrieved (TIME_SERIES_DAILY) is unadjusted for splits and dividends. The adjusted data endpoint (TIME_SERIES_DAILY_ADJUSTED) is a premium feature.

Price Visualization: Plots historical unadjusted closing prices using Matplotlib, showing trends over time.

Simple Moving Average (SMA): Calculates and plots SMA for specified periods, overlaying it on the stock's closing price chart.

Relative Strength Index (RSI): Calculates and plots RSI, including overbought (70) and oversold (30) levels, on a separate chart for clear analysis.

Error Handling: Includes robust error handling for API request failures, network issues, and invalid stock symbols.

Command-Line Interface: Simple and intuitive command-line interface for easy interaction.

Getting Started
Follow these instructions to get a copy of the project up and running on your local machine.

Prerequisites
Before you begin, ensure you have the following installed:

Python 3.x: You can download it from python.org.

pip: Python's package installer (usually comes with Python).

git: For cloning the repository (download from git-scm.com).

Alpha Vantage API Key
This project relies on the Alpha Vantage API for stock data. You'll need a free API key:

Go to the Alpha Vantage website: https://www.alphavantage.co/support/#api-key

Sign up and obtain your free API key.

Important: Create a file named config.ini in the root of your project folder and add your API key to it like this:

[api_keys]
alpha_vantage_key = YOUR_ALPHA_VANTAGE_API_KEY

Replace YOUR_ALPHA_VANTAGE_API_KEY with your actual key. This file is excluded from version control for security.

Installation
Clone the repository:

git clone https://github.com/YOUR_USERNAME/stock-market-analyser.git
cd stock-market-analyser

(Replace YOUR_USERNAME with your GitHub username)

Create a virtual environment (recommended):

python -m venv venv

Activate the virtual environment:

On Windows (Command Prompt/PowerShell):

.\venv\Scripts\activate

On macOS/Linux (Bash/Zsh):

source venv/bin/activate

Install the required Python packages:

pip install -r requirements.txt

Configure your API key:
Ensure you have created the config.ini file as described in the Alpha Vantage API Key section above.

Usage
Once installed, you can run the application from your terminal:

python stock_analyser.py

The application will prompt you to enter commands.

Welcome to the Stock Market Data Analyser!
Commands:
  'quote <symbol>'            - Get real-time stock quote.
  'history <symbol>'          - Get and plot historical close prices (last 100 days).
  'sma <symbol> <window>'     - Calculate and plot Simple Moving Average (e.g., 'sma AAPL 50').
  'rsi <symbol> <window>'     - Calculate and plot Relative Strength Index (e.g., 'rsi AAPL 14').
  'exit'                      - Quit the application.

Enter command: history AAPL
Fetching historical data for symbol: AAPL from Alpha Vantage (outputsize=compact)...

--- Raw API Response for Historical Data ---
{
  "Meta Data": {
    "1. Information": "Daily Prices (open, high, low, close) and Volumes",
    "2. Symbol": "AAPL",
    "3. Last Refreshed": "2024-06-25",
    "4. Output Size": "Compact",
    "5. Time Zone": "US/Eastern"
  },
  "Time Series (Daily)": {
    "2024-06-25": {
      "1. open": "209.1100",
      "2. high": "211.3900",
      "3. low": "208.6100",
      "4. close": "209.1000",
      "5. volume": "32906800"
    },
    // ... (more data)
  }
}
-------------------------------------------

--- Historical Data for AAPL (Last 5 days) ---
                  open     high      low    close    volume  adjusted_close
2024-06-18  214.6000  216.8900  213.0000  216.6700  76579601        216.6700
2024-06-20  213.9200  216.8800  212.7200  214.2900  63412500        214.2900
2024-06-21  210.0000  210.6100  207.1200  207.4900  99878200        207.4900
2024-06-24  207.7200  212.6300  207.1100  208.1400  81191000        208.1400
2024-06-25  209.1100  211.3900  208.6100  209.1000  32906800        209.1000

// A Matplotlib plot window will also appear.

Enter command: sma AAPL 50
Fetching historical data for symbol: AAPL from Alpha Vantage (outputsize=full)...

// A Matplotlib plot window showing price and SMA will appear.

Enter command: rsi GOOGL 14
Fetching historical data for symbol: GOOGL from Alpha Vantage (outputsize=full)...

// A Matplotlib plot window showing RSI will appear.

Type exit and press Enter to quit the application.

Project Structure
stock-market-analyser/

├── stock_analyser.py       # Main script for fetching data, calculating indicators, and application logic

├── plotter.py              # Contains functions for plotting historical data and indicators

├── requirements.txt        # Lists Python dependencies (e.g., requests, pandas, matplotlib)

├── config.ini              # (Local) Stores your Alpha Vantage API key (ignored by Git)

└── .gitignore              # Specifies files/directories to ignore in Git (e.g., venv/, config.ini)
