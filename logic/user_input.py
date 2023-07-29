# user_input.py
# Author: Robin Jiang
#
#
# This module contains a class that interacts with the user in the shell and
# stores user input.

import datetime


class UserInput:
    def __init__(self):
        self._previous_inputs = set()

    @staticmethod
    def get_ticker_symbol() -> str:
        """Asks the user for a ticker symbol less than or equal to 5 characters.
        Does not enforce the symbol being for a valid company."""
        _input = input("Enter a stock symbol: ")
        while len(_input) > 5:
            _input = input("Please enter a valid stock symbol of length 5 or less: ")
        return _input

    @staticmethod
    def get_buy_year() -> int:
        """Asks the user for a year to buy the stock from 1700 to the current year"""
        year = -1
        while not (1700 < year < datetime.datetime.today().year):
            try:
                year = int(input("Enter a year to buy the stock: "))
            except ValueError:
                print("please enter a valid year")
        return year
