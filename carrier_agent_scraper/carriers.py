import time
from bs4 import BeautifulSoup # parsing html
# selenium for automating web browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import os

base_path = os.path.expanduser("~\Downloads")
chromedriver_part = "chromedriver_win32\chromedriver.exe"
WEBDRIVER_EXECUTABLE_PATH = os.path.join(base_path, chromedriver_part)

def initialize_webdriver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--window-size=640,480")
    options.add_argument("--window-size=640,800")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(executable_path=WEBDRIVER_EXECUTABLE_PATH, options=options)
    return driver


class BristolWest:

    def __init__(self):
        pass

    def get_source_code(self, zipcode):
        # initialize and specify executable location because it's hard to add variables to PATH without admin rights
        driver = webdriver.Chrome(executable_path=WEBDRIVER_EXECUTABLE_PATH)
        driver.get("https://www.bristolwest.com/find-agent-broker")

        # wait until the search bar is found by id or 10 seconds have passed
        ls = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//input[@aria-label='Zip Code']")))  # the search bar's id
        search_bar = ls[1]
        search_bar.clear()
        search_bar.send_keys(zipcode)

        buttons = driver.find_elements_by_xpath("//button[@class='btn btn-primary px-3 btn-more-focus']")
        button = buttons[1]
        button.click()

        time.sleep(5)
        source_code = driver.page_source

        driver.close()

        return source_code


    def parse_name(self, div):
        name = div.find('div', class_="card-header text-left pb-1 strong").find('h2').text
        return name


    def parse_address(self, div):
        address = div.find('address').text.strip()
        return address


    def parse_number(self, div):
        number = div.find_all('div', class_="row")[0].find('a').text[2:]
        return number


    def parse_email(self, div):
        email = div.find_all('div', class_="row")[1].find('a').text
        return email


    def parse_city(self, div):
        city = div.find('address').find('br').next_sibling.strip().split(',')[0]
        return city


    def get_raw_address_string(self, address):
        driver = webdriver.Chrome(executable_path=WEBDRIVER_EXECUTABLE_PATH)
        driver.get("https://www.google.com/")

        ls = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//input[@aria-label='Search']")))  # the search bar's id

        search_bar = ls[0]
        search_bar.clear()
        search_bar.send_keys(address)
        search_bar.send_keys(Keys.RETURN)

        address_result = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//span[@class='desktop-title-subcontent']")))  # the search bar's id

        raw_address_string = address_result[0].text

        driver.close()

        return raw_address_string


    def parse_agent_zip(self, address):
        return address.split()[-1]


    def get_agent_zip(self, address):
        try:
            agent_zip_or_error = zipcode_lookup_dict[address]
            return agent_zip_or_error

        except KeyError:
            pass

        try:
            raw_address_string = get_raw_address_string(address)

        except:
            zipcode_lookup_dict[address] = 'error'
            return "error"

        agent_zip = parse_agent_zip(raw_address_string)
        zipcode_lookup_dict[address] = agent_zip

        return agent_zip


    def check_agent_city(self, city, searched_zip):
        zip_city = zp.filter_by(zip_code='43001')[0]['city']
        print(city, zip_city)

        return city == zip_city


    # Description: Checks for errors. If none, parses the string into chunks that become column names.
    # Parameters: source_code, string - HTML source code;
    # zipcode, string - a zip code
    # Returns: agencies_in_zip, list of lists - a list containing lists with entries
    # [name, address, phone number, zip code searched] for each result for the zip code.

    def parse_data(self, source_code, zipcode):
        soup = BeautifulSoup(source_code, 'html.parser')
        agencies_in_zip = []
        results_list = soup.find('div', class_="card-columns mt-3")
        results = results_list.find_all('div', class_="card agent-broker-card ng-star-inserted")

        for result in results:
            name = parse_name(result)
            address = parse_address(result)
            number = parse_number(result)
            email = parse_email(result)
            agent_zip = get_agent_zip(address)

            if agent_zip == 'error':
                entry = ['zip search error', 'zip search error', 'zip search error', 'zip search error', zipcode]
                agencies_in_zip.append(entry)

            if agent_zip == zipcode:
                entry = [name, address, number, email, zipcode]
                agencies_in_zip.append(entry)

        #         city = parse_city(result)

        #         if check_agent_city(city, zipcode):
        #             agent_zip = get_agent_zip(address)

        #             if agent_zip == zipcode:
        #                 entry = [name, address, number, email, zipcode]
        #                 agencies_in_zip.append(entry)

        if len(agencies_in_zip) == 0:
            agencies_in_zip.append(['none in zip', 'none in zip', 'none in zip', 'none in zip', zipcode])

        return agencies_in_zip


class Dairyland:
    def __init__(self):
        pass

    def get_source_code(self, zipcode):
        # initialize and specify executable location because it's hard to add variables to PATH without admin rights
        driver = initialize_webdriver()
        driver.get("https://www.dairylandinsurance.com/")

        find_agent_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='javascript:FindAnAgent.ShowFindAgentDialog()']")))
        find_agent_button.click()

        # wait until the search bar is found by id or 10 seconds have passed
        search_bar = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "famZipCode")))  # the search bar's id
        search_bar.clear()
        search_bar.send_keys(zipcode)

        button = driver.find_element_by_xpath("//div[@class='col-sm-1 Submit']/button[@class='btn btn-primary']")
        button.click()

        time.sleep(5)
        source_code = driver.page_source

        driver.close()

        return source_code

    def parse_name(self, div):
        name = div.find('span', class_='AgencyName').text
        return name

    def parse_number(self, div):
        number = div.find('div', class_='Phone').find('span').text
        return number

    def parse_address(self, div):
        address = div.find('div', class_='AddrLine1').text
        span_list = div.find('div', class_='AddrLine2').next_sibling.next_sibling.find_all('span')
        for span in span_list:
            address += " " + span.text
        return address

    def parse_agent_zip(self, address):
        agent_zip = address.split()[-1]
        return agent_zip

    def parse_data(self, source_code, zipcode):
        soup = BeautifulSoup(source_code, 'html.parser')
        agencies_in_zip = []

        results = soup.find_all('div', class_='row Agent')

        for agency in results:
            name = self.parse_name(agency)
            address = self.parse_address(agency)
            number = self.parse_number(agency)
            agent_zip = self.parse_agent_zip(address)

            if agent_zip == zipcode:
                entry = [name, address, number, zipcode]
                agencies_in_zip.append(entry)

        if len(agencies_in_zip) == 0:
            agencies_in_zip.append(['none in zip', 'none in zip', 'none in zip', zipcode])

        return agencies_in_zip


class Founders():
    def __init__(self):
        pass

    def get_source_code(self, zipcode):
        # initialize and specify executable location because it's hard to add variables to PATH without admin rights
        driver = initialize_webdriver()
        driver.get("https://www.foundersinsurance.com/AgentFinder/Default.aspx")

        # wait until the search bar is found by id or 10 seconds have passed
        search_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_txtZip")))  # the search bar's id
        search_bar.clear()
        search_bar.send_keys(zipcode)

        button = driver.find_element_by_id('ctl00_ContentPlaceHolder1_btnSearch')
        button.click()

        time.sleep(5)

        # Checking for Kemper page errors that occur when some zip codes are searched.
        #     logs = driver.get_log('browser')
        #     for log in logs:
        #         if log['level'] == "SEVERE":
        #             print("Kemper page error for " + str(zipcode) + ". Moving on.")
        #             driver.close()
        #             return 'Error'

        source_code = driver.page_source

        # checking for "no results found" message
        #     try:
        #         error_message = driver.find_element_by_xpath(
        #         '/html/body/app-root/div/find-agent-wizard/search-stepper/section/div/search-agent-map/div/div')
        #         if error_message.text == "No agents found, please refine your search parameters.":
        #             print("No results found for " + str(zipcode) + ". Moving on.")
        #             driver.close()
        #             return 'No Results'
        #     except:
        #         pass

        driver.close()

        return source_code

    def parse_number(self, entry):

        for item in entry:

            if item[:5] == 'PHONE':
                return item[7:]

        return 'not available'

    def parse_email(self, entry):

        for item in entry:

            if item[:5] == 'EMAIL':
                return item[7:]

        return 'not available'

    def parse_zipcode(self, string):
        zipcode = string.split()[-1]
        zipcode = zipcode.split("-")[0]

        #     if len(zipcode) != 5:
        #         raise ValueError("Zipcode length not right: " + str(zipcode))

        return zipcode

    def clean_entry(self, entry, searched_zipcode):
        name = entry[0]
        address = entry[1] + " " + entry[2]
        number = self.parse_number(entry)
        email = self.parse_email(entry)
        zipcode = self.parse_zipcode(entry[2])

        if zipcode != searched_zipcode:
            zipcode = self.parse_zipcode(entry[3])
            address += " " + entry[3]

        if zipcode != searched_zipcode:
            raise ValueError("Something wrong with zip code: " + str(zipcode))

        cleaned_entry = [name, address, number, email, zipcode]

        return cleaned_entry, zipcode

    def parse_data(self, source_code, zipcode):
        soup = BeautifulSoup(source_code, 'html.parser')
        agencies_in_zip = []

        no_results = soup.find("span", id="ctl00_ContentPlaceHolder1_lblNoAgents")

        if no_results is not None:  # Test for no results.
            agencies_in_zip.append(['no results', 'no results', 'no results', 'no results', zipcode])
            return agencies_in_zip

        table = soup.find("table", id="ctl00_ContentPlaceHolder1_gvAgents")

        for row in table.select('tbody tr')[1:]:
            spans = row.select('td span')
            entry = []

            for span in spans:
                entry.append(span.text)
            entry, entry_zip = self.clean_entry(entry, zipcode)

            if entry_zip == zipcode:
                agencies_in_zip.append(entry)

        if len(agencies_in_zip) == 0:
            agencies_in_zip.append(['no results', 'no results', 'no results', 'no results', zipcode])

        return agencies_in_zip


class Kemper:
    def __init__(self):
        pass

    def get_source_code(self, zipcode):
        # initialize and specify executable location because it's hard to add variables to PATH without admin rights
        driver = initialize_webdriver()
        driver.get("https://www.kemper.com/get-started/find-an-agent")

        # wait until the search bar is found by id or 10 seconds have passed
        search_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "edit-search-by-location-zip")))  # the search bar's id
        search_bar.clear()
        search_bar.send_keys(zipcode)

        # no id so had to use xpath. Useful when a close parent element has an id.
        checkbox = driver.find_element_by_xpath("//div[@id='edit-select-insurance-products']/div[1]/label[1]")
        checkbox.click()

        button = driver.find_element_by_id('edit-actions-submit')
        button.click()

        # self-contained element used by the Google Maps API, loads content at runtime with javascript
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='block-kemper-cohesion-subtheme-content']/iframe")))

        iframe_src = iframe.get_attribute('src')
        driver.get(iframe_src)
        time.sleep(5)  # sleeping to wait for page load. same as WebDriverWait, but there's no specific element to look
        # for, and we can't guarantee that once one element is found everything is loaded.

        # Checking for Kemper page errors that occur when some zip codes are searched.
        logs = driver.get_log('browser')
        for log in logs:
            if log['level'] == "SEVERE":
                print("Kemper page error for " + str(zipcode) + ". Moving on.")
                driver.close()
                return 'Error'

        source_code = driver.page_source

        # checking for "no results found" message
        try:
            error_message = driver.find_element_by_xpath(
                '/html/body/app-root/div/find-agent-wizard/search-stepper/section/div/search-agent-map/div/div')
            if error_message.text == "No agents found, please refine your search parameters.":
                print("No results found for " + str(zipcode) + ". Moving on.")
                driver.close()
                return 'No Results'
        except:
            pass

        driver.close()

        return source_code

    def filter_for_zipcode_match(self, ls, zipcode):
        filtered_ls = []

        for entry in ls:
            entry_zip = entry[3]

            if entry_zip == zipcode:
                filtered_ls.append(entry)

        return filtered_ls

    def parse_data(self, source_code, zipcode):
        if source_code == 'No Results':
            return [['No results', 'No results', 'No results', zipcode]]

        if source_code == 'Error':
            return [['Error', 'Error', 'Error', zipcode]]

        soup = BeautifulSoup(source_code, 'html.parser')

        table = soup.find_all('table', class_='table table-hover')[
            1]  # there are two tables found on the page. Selecting
        # the second one.

        agencies_in_zip = []

        for row in table.select('tr'):
            entry = [e.text for e in row.select("th, td")]  # this is a list comprehension. Native python shortcut.
            del entry[-1]  # garbage

            # What follows is crazy string manipulation that's very specific to the particular format found on the web page.
            # It just takes what originally is one string and breaks it into name and address. Number is separate from the start.
            # There might be better way, but this works... for now.

            if entry[0] == '':  # skips the first element in the table because it's not an agency.
                continue

            string = entry[0]
            split_list = string.split("  ")
            name = split_list[0].strip()
            address = split_list[-2] + " " + split_list[-1]
            split_list = address.split('(')
            address = split_list[0].strip()

            if entry[1] != '':
                number = entry[1]
            else:
                number = "Not available"

            entry_zip = address.split()[-1]

            entry = [name, address, number, entry_zip]

            agencies_in_zip.append(entry)

        agencies_in_zip = self.filter_for_zipcode_match(agencies_in_zip, zipcode)

        if len(agencies_in_zip) == 0:
            agencies_in_zip = [['No results', 'No results', 'No results', zipcode]]

        return agencies_in_zip


