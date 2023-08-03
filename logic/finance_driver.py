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

    def get_returns(self) -> float:
        """Uses the information in search to calculate change in capital based on yfinance."""

        month, day = _format_month_and_day()

        # search for one year from search.year to search.year + 1
        history = self._ticker.history(start=f"{self._search.year}-{month}-{day}",
                                       end=f"{self._search.year + 1}-{month}-{day}")
        if 'currentPrice' not in self._info:
            current_price = self._info['previousClose']
        else:
            current_price = self._info['currentPrice']

        return self.calculate_change(history.iloc[0]["Open"], current_price, self._search.dollars)

    def calculate_change(self, starting_price: int | float, ending_price: int | float, amount_invested: int | float) -> float:
        """Returns the amount of money resulting after investing at starting_price."""
        return round(amount_invested * (ending_price / starting_price), 2)


def _format_month_and_day() -> tuple[str | int, str | int]:
    """returns a tuple of month, day in (DD, YY) form"""
    month = datetime.date.today().month
    day = datetime.date.today().day
    if month < 10:
        month = '0' + str(month)
    if day < 10:
        day = '0' + str(day)
    return month, day


__all__ = [TickerError.__name__, CalculateReturn.__name__]
