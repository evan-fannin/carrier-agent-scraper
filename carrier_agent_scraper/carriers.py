import time
from bs4 import BeautifulSoup # parsing html
# selenium for automating web browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


WEBDRIVER_EXECUTABLE_PATH = r'\Users\ntmkef30\Downloads\chromedriver_win32\chromedriver.exe'


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
        driver = webdriver.Chrome(executable_path=WEBDRIVER_EXECUTABLE_PATH)
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
            name = parse_name(agency)
            address = parse_address(agency)
            number = parse_number(agency)
            agent_zip = parse_agent_zip(address)

            if agent_zip == zipcode:
                entry = [name, address, number, zipcode]
                agencies_in_zip.append(entry)

        if len(agencies_in_zip) == 0:
            agencies_in_zip.append(['none in zip', 'none in zip', 'none in zip', zipcode])

        return agencies_in_zip