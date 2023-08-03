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


class CalculateReturn:
    """class that calculates return on investment"""

    def __init__(self, search: StockSearch):
        self._search = search
        self._ticker = yfinance.Ticker(search.symbol)
        self._info = self._ticker.info
        if self._info is None:
            raise TickerError(f'"{search.symbol}" is not a valid symbol.')

    def __getitem__(self, key):
        """Returns the item stored in self._info at key, or raises KeyError if key does not exist."""
        return self._info[key]

    def get_returns(self) -> float:
        """Uses the information in search to calculate change in capital based on yfinance."""

        month, next_month, day = _format_month_and_day()

        # search for one year from search.year to search.year + 1
        history = self._get_history(self._search.year, month, day, end_year=self._search.year + 1)

        if 'currentPrice' not in self._info:
            current_price = self._info['previousClose']
        else:
            current_price = self._info['currentPrice']

        return self.calculate_change(history.iloc[0]["Open"], current_price)

    def calculate_change(self, starting_price: int | float, ending_price: int | float) -> float:
        """Returns the amount of money resulting after investing at starting_price."""
        if self._search.monthly_investment == 0:
            return round(self._search.principal_investment * (ending_price / starting_price), 2)
        else:
            # WORK ON THIS
            pass


    def _get_history(self, year: int, month: int | str, day: int | str, end_year: int = None, end_month: int | str = None) -> 'pandas.Dataframe':
        """Gets the history of a stock from the given date. If no end date is given, 1 month later will be chosen.
        Month and day must be either double-digit or in 0X form"""

        if end_month is None:
            end_month = month
        if end_year is None:
            if end_month != month and end_month == 1:
                end_year = year + 1
            else:
                end_year = year
        return self._ticker.history(start=f"{year}-{month}-{day}",
                                    end=f"{end_year}-{end_month}-{day}")


def _format_month_and_day() -> tuple[str | int, str | int, str | int]:
    """returns a tuple of month, next_month, and day in (MM, MM, DD) form"""
    month = datetime.date.today().month
    next_month = month + 1
    if next_month == 13:
        next_month = 1
    day = datetime.date.today().day
    if month < 10:
        month = '0' + str(month)
    if next_month < 10:
        next_month = '0' + str(next_month)
    if day < 10:
        day = '0' + str(day)
    return month, next_month, day


__all__ = [TickerError.__name__, CalculateReturn.__name__]
