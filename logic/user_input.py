# user_input.py
# Author: Robin Jiang
#
#
# This module contains a class that interacts with the user in the shell and
# stores user input.

import datetime
TICKER_MAX_LENGTH = 5


def get_user_input() -> 'StockSearch':
    _search = StockSearch(get_ticker_symbol(), get_buy_year(),
                          get_principal_investment(), get_monthly_investment())
    return _search


def get_ticker_symbol() -> str:
    """Asks the user for a ticker symbol less than or equal to 5 characters.
    Does not enforce the symbol being for a valid company."""
    _input = input("Enter a stock symbol: ")
    while len(_input) > TICKER_MAX_LENGTH:
        _input = input("Please enter a valid stock symbol of length 5 or less: ")
    return _input


def get_buy_year() -> int:
    """Asks the user for a year to buy the stock from 1700 to the current year"""
    year = -1
    while not (1700 < year <= datetime.date.today().year):
        try:
            year = int(input("Enter a year to buy the stock: "))
        except ValueError:
            print("please enter a valid year")
    return year


def get_principal_investment() -> int:
    """Asks the user for an initial dollar amount to have invested in the stock."""
    while True:
        try:
            return int(input("Enter a principal dollar amount to invest: "))
        except ValueError:
            print("please enter a valid amount")


def get_monthly_investment() -> int:
    """Asks the user for a monthly dollar amount to have invested in the stock."""
    while True:
        try:
            return int(input("Enter a monthly dollar amount to invest: "))
        except ValueError:
            print("please enter a valid amount")


class StockSearch:
    """Immutable class that represents one search."""
    def __init__(self, symbol: str, year: int, principal_investment: int, monthly_investment: int = 0):
        """When instantiated, a StockSearch represents a Ticker symbol, year, and dollars amount immutably."""

        if (type(symbol) is not str or len(symbol) > TICKER_MAX_LENGTH
                or type(year) is not int or type(principal_investment) is not int or type(monthly_investment) is not int):
            raise ValueError("make sure inputs are valid")

        self._symbol = symbol
        self._year = year
        self._principal_investment = principal_investment
        self._monthly_investment = monthly_investment

    def __hash__(self):
        return hash((self._symbol, self._year, self._principal_investment, self._monthly_investment))

    def __eq__(self, other):
        return (isinstance(other, type(self)) and
                (self._symbol, self._year, self._principal_investment, self._monthly_investment) ==
                (other.symbol, other.year, other.principal_investment, other.monthly_investment))

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def year(self) -> int:
        return self._year

    @property
    def principal_investment(self) -> int:
        return self._principal_investment

    @property
    def monthly_investment(self) -> int:
        return self._monthly_investment


__all__ = [get_user_input.__name__, get_monthly_investment.__name__, get_principal_investment.__name__,
           get_buy_year.__name__, get_ticker_symbol.__name__, StockSearch.__name__]
