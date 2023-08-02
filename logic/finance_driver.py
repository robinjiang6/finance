# finance_driver.py
# Author: Robin Jiang
#
#
# This module is for using the yahoo finance API to search
# for stock prices for a given StockSearch (from user_input)

import yfinance
import datetime
from logic.user_input import StockSearch


class TickerError(Exception):
    """Raised when a ticker symbol is invalid"""
    pass


def get_change_in_capital(search: StockSearch) -> float:
    """Uses the information in search to calculate change in capital based on yfinance."""
    ticker = yfinance.Ticker(search.symbol)
    if ticker.info is None:
        raise TickerError(f'"{search.symbol}" is not a valid symbol.')

    month, day = _format_month_and_day()

    # search for one year from search.year to search.year + 1
    history = ticker.history(start=f"{search.year}-{month}-{day}",
                             end=f"{search.year + 1}-{month}-{day}")
    info = ticker.info
    if 'currentPrice' not in info:
        current_price = info['previousClose']
    else:
        current_price = info['currentPrice']

    return calculate_change(history.iloc[0]["Open"], current_price, search.dollars)


def calculate_change(starting_price: int | float, ending_price: int | float, amount_invested: int | float) -> float:
    """Returns the amount of money resulting after investing at starting_price."""
    return round(amount_invested * (ending_price/starting_price), 2)


def _format_month_and_day() -> tuple[str | int, str | int]:
    """returns a tuple of month, day in (DD, YY) form"""
    month = datetime.date.today().month
    day = datetime.date.today().day
    if month < 10:
        month = '0' + str(month)
    if day < 10:
        day = '0' + str(day)
    return month, day


__all__ = [TickerError.__name__, get_change_in_capital.__name__, calculate_change.__name__]