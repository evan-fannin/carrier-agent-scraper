"""
Run the main loop.
"""
from carrier_agent_scraper import io
from carrier_agent_scraper import zipcodes as zp
from carrier_agent_scraper import scraper

import os
import sys, traceback


class App:

    def __init__(self, tk_window, carrier, state):
        self.tk_window = tk_window
        self.carrier = self.format_carrier_name(carrier)
        self.state = state
        # self.WEBDRIVER_EXECUTABLE_PATH = self.set_webdriver_path()
        self.DATA_UPLOAD_DOWNLOAD_PATH = self.set_upload_download_path()
        self.create_file_directories()

    def create_file_directories(self):
        base_path = os.path.expanduser("~\Documents")
        all_carriers = os.path.join(base_path, "carrier_scraping_agent_data")

        if not os.path.isdir(all_carriers):
            os.mkdir(all_carriers)

        carrier_directory = os.path.join(all_carriers, self.carrier)

        if not os.path.isdir(carrier_directory):
            os.mkdir(carrier_directory)

    # def set_webdriver_path(self):
    #     base_path = os.path.expanduser("~\Downloads")
    #     specific_path = "chromedriver_win32\chromedriver.exe"
    #     webdriver_exec_path = os.path.join(base_path, specific_path)
    #     return webdriver_exec_path


    def set_upload_download_path(self):
        state = self.state.lower()
        base_path = os.path.expanduser("~\Documents\\carrier_scraping_agent_data")
        specific_path = f"{self.carrier}\\{state}.csv"
        data_upload_download_path = os.path.join(base_path, specific_path)
        return data_upload_download_path

    def run(self):
        df = io.load_dataframe(self.DATA_UPLOAD_DOWNLOAD_PATH)
        number_completed = io.get_number_completed(df)  # get number of zip codes already searched
        agencies = io.dataframe_to_list(df)  # for input to get_agencies_in_state()
        agencies = self.get_agencies_in_state(self.state, number_completed, agencies)  # new search
        df = io.create_dataframe(agencies) # save results
        io.save_dataframe(df, self.DATA_UPLOAD_DOWNLOAD_PATH)  # write to files

    def format_carrier_name(self, carrier):
        carrier = carrier.lower()
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

        # print(str(number_left) + " zipcodes left to process.\n")

        agencies = []

        for zipcode in zipcodes:
            try:
                data = self.get_zip_data(zipcode)
            except Exception as error:
                # print('Failure.')
                # print(repr(error))
                # traceback.print_exc(file=sys.stdout)
                return agencies

            agencies.extend(data)

            number_completed += 1
            progress_string = ("Processed results for " + str(zipcode) + ";\t"
                               + str(number_completed) + " of " + str(total))
            self.tk_window.update_progress(progress_string)

        return agencies

    def get_agencies_in_state(self, state, number_completed, agencies):
        zipcodes = zp.get_zipcodes_in_state(state)

        if number_completed == len(zipcodes):
            print("All done")
            return agencies

        agencies.extend(self.get_agencies_in_state_helper(zipcodes, number_completed))

        return agencies





