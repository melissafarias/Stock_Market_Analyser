Stock Market Data Analyser
A Python command-line tool designed to fetch and display real-time stock quotes using the Alpha Vantage API. This project serves as a practical demonstration of API integration, data handling, and command-line application development in Python.

Features
Real-time Stock Quotes: Fetches current price, open, high, low, volume, and other key metrics for any valid stock ticker symbol.

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

Replace YOUR_ALPHA_VANTA_GE_API_KEY with your actual key. This file is excluded from version control for security.

Installation
Clone the repository:

git clone https://github.com/melissafarias/stock-market-analyser.git
cd stock-market-analyser


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

The application will prompt you to enter a stock ticker symbol. Type the symbol (e.g., AAPL, MSFT, GOOGL) and press Enter.

Welcome to the Stock Market Data Analyser!
Type 'exit' to quit.

Enter stock ticker symbol (e.g., AAPL, MSFT): AAPL
Fetching data for symbol: AAPL from Alpha Vantage...

--- Stock Information ---
Symbol: AAPL
Current Price: $192.5300
Open: $192.3600
High: $192.9000
Low: $190.2300
Volume: 49454181
Latest Trading Day: 2023-10-26
Previous Close: $190.6900
Change: $1.8400
Change Percent: 0.9649%

Enter stock ticker symbol (e.g., AAPL, MSFT): exit
Exiting Stock Market Data Analyser. Goodbye!

Type exit and press Enter to quit the application.

Project Structure
stock-market-analyser/
├── stock_analyser.py       # Main script for fetching and displaying stock data
├── requirements.txt        # Lists Python dependencies (e.g., requests)
├── config.ini              # (Local) Stores your Alpha Vantage API key (ignored by Git)
└── .gitignore              # Specifies files/directories to ignore in Git (e.g., venv/, config.ini)

