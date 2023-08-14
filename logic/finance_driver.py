# finance_driver.py
# Author: Robin Jiang
#
#
# This module is for using the yahoo finance API to search
# for stock prices for a given StockSearch (from user_input)

import yfinance
import datetime
from dateutil.relativedelta import relativedelta
from logic.user_input import StockSearch
from collections import namedtuple

# an Investment namedtuple represents a date and a dollar amount invested into a given stock
Investment = namedtuple("Investment", ["date", "amount"])

# Global constant representing one month of time difference
ONE_MONTH = relativedelta(months=1)


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
        self._investment_log = None

    def __getitem__(self, key):
        """Returns the item stored in self._info at key, or raises KeyError if key does not exist."""
        return self._info[key]

    def get_returns(self) -> float:
        """Uses the information in search to calculate change in capital based on yfinance."""
        if self._returns is not None:
            # returns already calculated value if in cache
            return self._returns

        if 'currentPrice' not in self._info:
            current_price = self._info['previousClose']
        else:
            current_price = self._info['currentPrice']

        return self.calculate_change(ending_price=current_price, start_date=self._search.date)

    def calculate_change(self, ending_price: int | float, start_date: datetime.date) -> float:
        """Returns the amount of money resulting after investing at starting_price."""
        # temp_investment_log will be converted to a tuple at the end of the method
        # and stored in self._investment_log
        temp_investment_log = []

        # search from start_date to now
        history = self._ticker.history(start=start_date, end=datetime.date.today())

        # self._returns is initially set to just the principal investment
        # and self._total_investment is set to just the principal investment
        self._total_investment = self._search.principal_investment
        self._returns = self._search.principal_investment * (ending_price / history.iloc[0]["Open"])
        temp_investment_log.append(Investment(start_date, self._search.principal_investment))

        if self._search.monthly_investment != 0:
            today = datetime.date.today()
            target_date = start_date

            # index will represent the days in the history
            index = 32

            while index < len(history) and history.iloc[index].name.date() < today:
                # WORK ON THIS RIGHT HERE

                # If a price for target_date cannot be found, the closest day after target_date will be used.
                # This is meant to simulate real life, where you cannot buy a stock in the past,
                # so the closest date before target_date will not be used.
                target_date += ONE_MONTH
                # after this loop, the selected date will be greater than or equal to target date
                while history.iloc[index].name.date() >= target_date:
                    index -= 1
                index += 1
                temp_investment_log.append(Investment(history.iloc[index].name.date(), self._search.monthly_investment))
                self._returns += self._search.monthly_investment * (ending_price / history.iloc[index]['Open'])
                self._total_investment += self._search.monthly_investment
                index += 32

        self._returns = round(self._returns, 2)
        self._investment_log = tuple(temp_investment_log)
        return self._returns

    @property
    def total_investment(self) -> int:
        """Returns the total investment (principal + months)"""
        return self._total_investment

    @property
    def investment_log(self) -> tuple:
        """Returns the log of investment throughout the months"""
        return self._investment_log


__all__ = [TickerError.__name__, CalculateReturn.__name__]
