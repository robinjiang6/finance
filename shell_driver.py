# shell_driver.py
# Author: Robin Jiang
#
# This module drives the shell version of the app

from logic.finance_driver import CalculateReturn
from logic.user_input import get_user_input


def run() -> None:
    search = get_user_input()
    s = CalculateReturn(search)
    print(f"If you had invested ${search.principal_investment} into {search.symbol} in "
          f"{search.year} with a monthly investment of ${search.monthly_investment}, you would now have ${s.get_returns()}")
    percentage = round(((s.get_returns() - s.total_investment)/s.total_investment) * 100, 2)
    delta = "increased"
    if percentage < 0:
        delta = "decreased"
    print(f"In total, you invested ${s.total_investment}, which means your investment {delta} by {abs(percentage)}%")

    # for item in s.investment_log:
    #     print(item)


if __name__ == "__main__":
    run()
