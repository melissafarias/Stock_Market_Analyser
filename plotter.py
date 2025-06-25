import pandas as pd
import matplotlib.pyplot as plt

def plot_historical_prices(df: pd.DataFrame, symbol: str):
    """
    Plots the historical unadjusted closing prices using Matplotlib.

    Args:
        df (pd.DataFrame): DataFrame containing historical stock data.
        symbol (str): The stock ticker symbol.
    """
    if df is None or df.empty:
        print("No data to plot.")
        return

    plt.figure(figsize=(12, 6))
    # Use 'close' or 'adjusted_close' (which is now derived from 'close' for free tier)
    plt.plot(df.index, df['adjusted_close'], label=f'{symbol} Unadjusted Close Price', color='blue')
    plt.title(f'{symbol} Historical Unadjusted Close Price')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_indicator(price_series: pd.Series, indicator_series: pd.Series, symbol: str, indicator_name: str, is_rsi: bool = False):
    """
    Plots a financial indicator. Can plot SMA with price, or RSI on its own subplot.

    Args:
        price_series (pd.Series): The stock's close price series (optional, for SMA plots).
        indicator_series (pd.Series): The series containing the indicator values.
        symbol (str): The stock ticker symbol.
        indicator_name (str): Name of the indicator (e.g., 'SMA (50 days)', 'RSI (14 days)').
        is_rsi (bool): True if the indicator is RSI (to plot on a separate subplot with RSI specific lines).
    """
    if indicator_series is None or indicator_series.empty:
        print(f"No data to plot for {indicator_name}.")
        return

    if is_rsi:
        # Plot RSI on a separate subplot as it has a different scale
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(indicator_series.index, indicator_series, label=indicator_name, color='purple')
        ax.axhline(70, linestyle='--', alpha=0.6, color='red', label='Overbought (70)')
        ax.axhline(30, linestyle='--', alpha=0.6, color='green', label='Oversold (30)')
        ax.fill_between(indicator_series.index, 70, indicator_series, where=(indicator_series >= 70), color='red', alpha=0.1)
        ax.fill_between(indicator_series.index, 30, indicator_series, where=(indicator_series <= 30), color='green', alpha=0.1)
        ax.set_title(f'{symbol} {indicator_name}')
        ax.set_xlabel('Date')
        ax.set_ylabel(indicator_name)
        ax.set_ylim(0, 100) # RSI is typically between 0 and 100
        ax.grid(True)
        ax.legend()
        plt.tight_layout()
    else:
        # Plot SMA on the same chart as price
        fig, ax = plt.subplots(figsize=(12, 6))
        if price_series is not None and not price_series.empty:
            ax.plot(price_series.index, price_series, label=f'{symbol} Close Price', color='blue')
        ax.plot(indicator_series.index, indicator_series, label=indicator_name, color='orange', linestyle='--')
        ax.set_title(f'{symbol} Close Price with {indicator_name}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price (USD)')
        ax.grid(True)
        ax.legend()
        plt.tight_layout()

    plt.show()
