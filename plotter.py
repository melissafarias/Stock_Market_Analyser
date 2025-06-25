import pandas as pd
import matplotlib.pyplot as plt

def plot_historical_prices(df: pd.DataFrame, symbol: str):
    """
    Plots the historical adjusted closing prices using Matplotlib.

    Args:
        df (pd.DataFrame): DataFrame containing historical stock data.
        symbol (str): The stock ticker symbol.
    """
    if df is None or df.empty:
        print("No data to plot.")
        return

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['adjusted_close'], label='Adjusted Close Price', color='blue')
    plt.title(f'{symbol} Historical Adjusted Close Price')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

