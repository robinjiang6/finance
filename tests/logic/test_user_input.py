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
    """Decorator that runs func with contextlib.redirect_stdout and patch to simulate standard input and output."""
    def new_func(*args, standard_inputs: list = None, **kwargs):
        if standard_inputs is None:
            with contextlib.redirect_stdout(io.StringIO()) as output:
                func(*args, **kwargs)
            return output.getvalue()
        else:
            with contextlib.redirect_stdout(io.StringIO()) as output:
                with patch('builtins.input', side_effect=standard_inputs):
                    func(*args, **kwargs)
            return output.getvalue()

    return new_func


class TestRunWithIO(unittest.TestCase):
    def test_run_works_with_positional_arguments(self):
        @run_with_io
        def multiply(x, y):
            print(x * y)

        self.assertEqual('12', multiply(3, 4).strip())

    def test_run_works_with_keyword_arguments(self):
        @run_with_io
        def multiply(*, first, second):
            print(first * second)

        self.assertEqual('12', multiply(first=3, second=4).strip())

    def test_run_works_with_inputs(self):
        @run_with_io
        def multiply():
            print(int(input()) * int(input()))

        self.assertEqual('12', multiply(standard_inputs=[3, 4]).strip())


class TestUserInput(unittest.TestCase):
    def test_something(self):
        pass


if __name__ == "__main__":
    unittest.main()
