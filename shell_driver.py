# shell_driver.py
# Author: Robin Jiang
#
# This module drives the shell version of the app

from logic.finance_driver import get_change_in_capital
from logic.user_input import UserInput


def run() -> None:
    search = UserInput().get_user_input()
    print(f"If you had invested ${search.dollars} into {search.symbol} in "
          f"{search.year}, you would now have ${get_change_in_capital(search)}")


if __name__ == "__main__":
    run()
