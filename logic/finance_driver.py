# finance_driver.py
# Author: Robin Jiang
#
#
# This module is for using the yahoo finance API to search
# for stock prices for a given StockSearch (from user_input)

import yfinance
import datetime
from logic.user_input import StockSearch
from collections import namedtuple

Investment = namedtuple("Investment", )


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
        self._total_investment = 0
        self._returns = None
        self._investment_log = []

    def __getitem__(self, key):
        """Returns the item stored in self._info at key, or raises KeyError if key does not exist."""
        return self._info[key]

    def get_returns(self) -> float:
        """Uses the information in search to calculate change in capital based on yfinance."""

        if 'currentPrice' not in self._info:
            current_price = self._info['previousClose']
        else:
            current_price = self._info['currentPrice']

        return self.calculate_change(current_price)

    def calculate_change(self, ending_price: int | float) -> float:
        """Returns the amount of money resulting after investing at starting_price."""
        if self._returns is not None:
            # returns already calculated value if in cache
            return self._returns

        month, day = _format_month_and_day()

        # search from search.year to now
        history = self._ticker.history(start=datetime.date(self._search.year, month, day),
                                       end=datetime.date.today())
        # self._returns is initially set to just the principal investment
        # and self._total_investment is set to just the principal investment
        self._total_investment = self._search.principal_investment
        self._returns = round(self._search.principal_investment * (ending_price / history.iloc[0]["Open"]), 2)

        if self._search.monthly_investment == 0:
            self._returns = round(self._returns, 2)
            return self._returns
        else:
            year = self._search.year
            # carry_over_investment is to be invested at the next available chance
            # in case a stock is unavailable for a whole month
            carry_over_investment = 0
            while int(month) < datetime.date.today().month or year < datetime.date.today().year:
                month_history = self._get_history(year=year, month=month, day=day, end_month=next_month)
                if len(month_history) == 0:
                    # empty dataframe, there is no data from this month, so rollover investment to next available month
                    carry_over_investment += self._search.monthly_investment
                else:
                    # there is data for this month, so the monthly investment,
                    # as well as the rollover investment is invested
                    month_price = month_history.iloc[0]["Open"]
                    self._total_investment += self._search.monthly_investment + carry_over_investment
                    self._returns += round(((self._search.monthly_investment + carry_over_investment) *
                                            (ending_price / month_price)), 2)
                    carry_over_investment = 0

                # updating the date for the next month
                month, next_month, day = _format_month_and_day(month=int(next_month))
                if int(month) == 1:
                    # next year since month is January
                    year += 1
            self._returns = round(self._returns, 2)
            return self._returns

    @property
    def total_investment(self) -> int:
        """Returns the total investment (principal + months)"""
        return self._total_investment


def _format_month_and_day() -> tuple[str | int, str | int]:
    """returns a tuple of month and day in (MM, DD) form"""
    month = datetime.date.today().month
    day = datetime.date.today().day
    if month < 10:
        month = '0' + str(month)
    if day < 10:
        day = '0' + str(day)
    return month, day


__all__ = [TickerError.__name__, CalculateReturn.__name__]
