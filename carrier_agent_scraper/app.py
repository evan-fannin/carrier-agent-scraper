"""
Run the main loop.
"""
from .dataframe_io import DataFrameIO
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

import zipcodes as zp # gives, among other things, zip codes of states.

import sys, traceback

import os

class App:

    def __init__(self):
        self.carrier = carrier
        self.state = state
        self.WEBDRIVER_EXECUTABLE_PATH = r'\Users\ntmkef30\Downloads\chromedriver_win32\chromedriver.exe'
        self.DATA_UPLOAD_DOWNLOAD_PATH = r"\Users\ntmkef30\Documents\national_general_agency_data\oh_data.csv"



    def run():
        df_io = DataFrameIO(column_names, self.DATA_UPLOAD_DOWNLOAD_PATH)
        number_completed = df_io.get_number_completed() # get number of zip codes already searched
        agencies = dataframe_to_list(df) # for input to get_agencies_in_state()
        agencies = get_agencies_in_state(STATE, number_completed, agencies) # new search
        df = create_dataframe(agencies) # save results
        save_dataframe(df) # write to files






    def get_zip_data(zipcode):
        source_code = get_source_code(zipcode)
        data = parse_data(source_code, zipcode)
        return data


    def get_agencies_in_state_helper(zipcodes, number_completed=0):
        total = len(zipcodes)  # total number of zip codes being processed.

        # remove already processed zip codes.
        for n in range(number_completed):
            zipcodes.pop(0)

        number_left = len(zipcodes)

        print(str(number_left) + " zipcodes left to process.\n")

        agencies = []

        for zipcode in zipcodes:
            try:
                data = get_zip_data(zipcode)
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


    def get_agencies_in_state(state, number_completed, agencies):
        zipcodes = get_zipcodes_in_state(state)

        if number_completed == len(zipcodes):
            print("All done")
            return agencies

        agencies.extend(get_agencies_in_state_helper(zipcodes, number_completed))

        return agencies





