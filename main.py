# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from carrier_agent_scraper.app import App
import os
import sys
import tkinter as tk
from gui.display import Application


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
    root = tk.Tk()
    root.title = "Carrier Scraper"
    root.lift()
    w = 300  # width for the Tk root
    h = 300  # height for the Tk root

    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) + (ws / 4)
    y = (hs / 2) - (h / 2)

    # set the dimensions of the screen
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    app = Application(master=root)
    app.mainloop()
    # carrier = input("Enter carrier name: \n")
    # state = input("Enter state abbreviation: \n")
    # app = App(carrier, state)
    # app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
