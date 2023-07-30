# user_input.py
# Author: Robin Jiang
#
#
# This module contains a class that interacts with the user in the shell and
# stores user input.

import datetime
TICKER_MAX_LENGTH = 5


class UserInput:
    def __init__(self):
        self._previous_inputs = set()

    def get_user_input(self) -> 'StockSearch':
        _search = StockSearch(UserInput.get_ticker_symbol(), UserInput.get_buy_year(), UserInput.get_dollar_amount())
        self._previous_inputs.add(_search)
        return _search

    @staticmethod
    def get_ticker_symbol() -> str:
        """Asks the user for a ticker symbol less than or equal to 5 characters.
        Does not enforce the symbol being for a valid company."""
        _input = input("Enter a stock symbol: ")
        while len(_input) > TICKER_MAX_LENGTH:
            _input = input("Please enter a valid stock symbol of length 5 or less: ")
        return _input

    @staticmethod
    def get_buy_year() -> int:
        """Asks the user for a year to buy the stock from 1700 to the current year"""
        year = -1
        while not (1700 < year <= datetime.date.today().year):
            try:
                year = int(input("Enter a year to buy the stock: "))
            except ValueError:
                print("please enter a valid year")
        return year

    @staticmethod
    def get_dollar_amount() -> int:
        """Asks the user for a dollar amount to have invested in the stock."""
        while True:
            try:
                return int(input("Enter a dollar amount to invest: "))
            except ValueError:
                print("please enter a valid amount")


class StockSearch:
    """Immutable class that represents one search."""
    def __init__(self, symbol: str, year: int, dollars: int):
        """When instantiated, a StockSearch represents a Ticker symbol, year, and dollars amount immutably."""

        if (type(symbol) is not str or len(symbol) > TICKER_MAX_LENGTH
                or type(year) is not int or type(dollars) is not int):
            raise ValueError("make sure inputs are valid")

        self._symbol = symbol
        self._year = year
        self._dollars = dollars

    def __hash__(self):
        return hash((self._symbol, self._year, self._dollars))

    def __eq__(self, other):
        return (isinstance(other, type(self)) and
                (self._symbol, self._year, self._dollars) == (other.symbol, other.year, other.dollars))

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def year(self) -> int:
        return self._year

    @property
    def dollars(self) -> int:
        return self._dollars


__all__ = [UserInput.__name__, StockSearch.__name__]
