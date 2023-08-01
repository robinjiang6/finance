# test_base.py
# Author: Robin Jiang
#
#
# This module contains some base unittest functions that can be used by other modules.
import unittest
from unittest.mock import patch
import contextlib
import io


def run_with_io(func):
    """Decorator that runs func with contextlib.redirect_stdout and patch to simulate standard input and output."""
    def new_func(*args, standard_inputs: list[str] = None, **kwargs):
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


if __name__ == "__main__":
    unittest.main()