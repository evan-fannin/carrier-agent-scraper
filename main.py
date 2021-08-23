# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from carrier_agent_scraper.app import App
import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder nad stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


_zips_json = resource_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "zips.json.bz2"))


if __name__ == '__main__':
    carrier = input("Enter carrier name: \n")
    state = input("Enter state abbreviation: \n")
    app = App(carrier, state)
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
