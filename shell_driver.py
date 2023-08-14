# shell_driver.py
# Author: Robin Jiang
#
# This module drives the shell version of the app

from logic.finance_driver import CalculateReturn, DateError, TickerError
from logic.user_input import get_user_input
import requests


def run() -> None:
    search = get_user_input()


    try:
        s = CalculateReturn(search)
        returns = s.get_returns()
        print(f"If you had invested ${search.principal_investment} into {search.symbol} in "
              f"{search.date.year} with a monthly investment of ${search.monthly_investment},"
              f" you would now have ${returns}")
        percentage = round(((s.get_returns() - s.total_investment) / s.total_investment) * 100, 2)
        delta = "increased"
        if percentage < 0:
            delta = "decreased"
        print(
            f"In total, you invested ${s.total_investment}, which means your investment {delta} by {abs(percentage)}%")

        # print(s._info)
        # for item in s.investment_log:
        #     print(item)
    except DateError as d:
        print(f"The date must be after {d.start_date}.")
    except (TickerError, requests.exceptions.HTTPError):
        print("Please enter a valid stock symbol.")


if __name__ == "__main__":
    run()
