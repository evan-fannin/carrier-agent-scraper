"""
Run the main loop.
"""
from carrier_agent_scraper import io
from carrier_agent_scraper import zipcodes as zp
from carrier_agent_scraper import scraper

from bs4 import BeautifulSoup # parsing html

import pandas as pd

# selenium for automating web browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

import time
import sys, traceback


class App:

    def __init__(self, carrier, state):
        self.carrier = self.format_carrier_name(carrier)
        self.state = state
        self.WEBDRIVER_EXECUTABLE_PATH = r'\Users\ntmkef30\Downloads\chromedriver_win32\chromedriver.exe'
        self.DATA_UPLOAD_DOWNLOAD_PATH = self.set_upload_download_path()

    def set_upload_download_path(self):
        state = self.state.lower()
        data_upload_download_path = f"\\Users\\ntmkef30\\Documents\\{self.carrier}\\{state}.csv"
        return data_upload_download_path

    def run(self):
        df = io.load_dataframe(self.DATA_UPLOAD_DOWNLOAD_PATH)
        number_completed = io.get_number_completed(df)  # get number of zip codes already searched
        agencies = io.dataframe_to_list(df)  # for input to get_agencies_in_state()
        agencies = self.get_agencies_in_state(self.state, number_completed, agencies)  # new search
        df = io.create_dataframe(agencies) # save results
        io.save_dataframe(df, self.DATA_UPLOAD_DOWNLOAD_PATH)  # write to files

    def format_carrier_name(self, carrier):
        word_list = carrier.split()
        formatted_name = "_".join(word_list)
        return formatted_name


    def get_zip_data(self, zipcode):
        data = scraper.scrape_and_parse(self.carrier, zipcode)
        return data

    def get_agencies_in_state_helper(self, zipcodes, number_completed=0):
        total = len(zipcodes)  # total number of zip codes being processed.

        # remove already processed zip codes.
        for n in range(number_completed):
            zipcodes.pop(0)

        number_left = len(zipcodes)

        print(str(number_left) + " zipcodes left to process.\n")

        agencies = []

        for zipcode in zipcodes:
            try:
                data = self.get_zip_data(zipcode)
            except Exception as error:
                print('Failure.')
                print(repr(error))
                traceback.print_exc(file=sys.stdout)
                return agencies

            agencies.extend(data)

            number_completed += 1
            print("Processed results for " + str(zipcode) + ";\t" +
                  str(number_completed) + " of " + str(total))

        return agencies

    def get_agencies_in_state(self, state, number_completed, agencies):
        zipcodes = zp.get_zipcodes_in_state(state)

        if number_completed == len(zipcodes):
            print("All done")
            return agencies

        agencies.extend(self.get_agencies_in_state_helper(zipcodes, number_completed))

        return agencies





