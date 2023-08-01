# test_user_input.py
# Author: Robin Jiang
#
# unit testing for user_input.py

from logic.user_input import *
import unittest
import contextlib
import io
from unittest.mock import patch


def run_with_io(func):
    """Decorator that runs func with contextlib.redirect_stdout and patch to simulate standard input and output.
    new function returns a tuple of length 2, with a list at index = 0 containing standard output from the program
    and whatever the original function outputted at index = 1."""
    def new_func(*args, standard_inputs: list = None, **kwargs):
        if standard_inputs is None:
            with contextlib.redirect_stdout(io.StringIO()) as output:
                func_return = func(*args, **kwargs)
            return output.getvalue(), func_return
        else:
            with contextlib.redirect_stdout(io.StringIO()) as output:
                with patch('builtins.input', side_effect=standard_inputs):
                    func_return = func(*args, **kwargs)
            return output.getvalue(), func_return

    return new_func


class TestRunWithIO(unittest.TestCase):
    def test_run_works_with_positional_arguments(self):
        @run_with_io
        def multiply(x, y):
            print(x * y)
            return x * y

        self.assertEqual('12', multiply(3, 4)[0].strip())
        self.assertEqual(12, multiply(3, 4)[1])

    def test_run_works_with_keyword_arguments(self):
        @run_with_io
        def multiply(*, first, second):
            print(first * second)
            return first * second

        self.assertEqual('12', multiply(first=3, second=4)[0].strip())
        self.assertEqual(12, multiply(first=3, second=4)[1])

    def test_run_works_with_inputs(self):
        @run_with_io
        def multiply():
            first = int(input())
            second = int(input())
            print(first * second)
            return first * second

        self.assertEqual('12', multiply(standard_inputs=[3, 4])[0].strip())
        self.assertEqual(12, multiply(standard_inputs=[3, 4])[1])


class TestUserInput(unittest.TestCase):
    def test_get_ticker_symbol(self):
        @run_with_io
        def outside_func():
            return UserInput.get_ticker_symbol()

        self.assertEqual("AAPL", outside_func(standard_inputs=["AAPL"])[1])
        self.assertEqual("12345", outside_func(standard_inputs=["123456", "12345", "AAPL"])[1])

    def test_get_buy_year(self):
        @run_with_io
        def outside_func():
            return UserInput.get_buy_year()

        self.assertEqual(1701, outside_func(standard_inputs=["1701"])[1])
        self.assertEqual(2023, outside_func(standard_inputs=["2023"])[1])
        self.assertEqual(1850, outside_func(standard_inputs=["1850"])[1])
        self.assertEqual(1701, outside_func(standard_inputs=["1699", "1700", "2025", "1701"])[1])

    def test_get_dollar_amount(self):
        @run_with_io
        def outside_func():
            return UserInput.get_dollar_amount()

        self.assertEqual(1701, outside_func(standard_inputs=["1701"])[1])
        self.assertEqual(2023, outside_func(standard_inputs=["2023"])[1])
        self.assertEqual(1850, outside_func(standard_inputs=["1850"])[1])
        self.assertEqual(1699, outside_func(standard_inputs=["1699", "1700", "2025", "1701"])[1])
        self.assertEqual(1701, outside_func(standard_inputs=["abdfb", "@#$dg", "202df5", "1701"])[1])

    def test_stock_search(self):
        s = StockSearch("AAPL", 1995, 100)
        self.assertEqual("AAPL", s.symbol)
        self.assertEqual(1995, s.year)
        self.assertEqual(100, s.dollars)
        a = StockSearch("AAPL", 1995, 100)
        self.assertEqual(s, a)
        self.assertIsNot(s, a)

    def test_get_user_input(self):
        s = StockSearch("AAPL", 1995, 100)

        @run_with_io
        def outside_func():
            return UserInput().get_user_input()

        self.assertEqual(s, outside_func(standard_inputs=["AAPL", "1995", "100"])[1])
        self.assertEqual(s, outside_func(standard_inputs=["AAAAAA", "AAPL", "1700", "1995", "asdfsd", "100"])[1])


if __name__ == "__main__":
    unittest.main()
