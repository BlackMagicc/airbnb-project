from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
# from selenium import webdriver
from prettytable import PrettyTable
# from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait


class AirbnbFilter:
    driver = None

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def price_range(self, min_price, max_price):  # todo: fix...
        # Handle pop up
        try:
            pop_up = self.driver.find_element_by_xpath('//button[@class="_187sg6v"]')
            pop_up.click()
        except NoSuchElementException:
            pass
        price_button = self.driver.find_element_by_xpath('//div[@id="menuItemButton-price_range"]')
        price_button.click()

        # price_min = price_button.find_element_by_xpath('//button[@aria-label="Minimum Price"]')
        # ActionChains(self.driver).click_and_hold(price_min).pause(1).move_by_offset(-0.001, 0).release().perform()

        # self.driver.execute_script("arguments[0].click();", price_min)
        price_min = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.XPATH, '//button[@aria-label="Minimum Price"]')))
        self.driver.execute_script("arguments[0].setAttribute('aria-valuenow',arguments[1]);", price_min, '354')

        # price_max = price_button.find_element_by_xpath('//button[@aria-label="Maximum Price"]')
        price_max = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.XPATH, '//button[@aria-label="Maximum Price"]')))

        # ActionChains(self.driver).drag_and_drop_by_offset(price_max, -50, 0).pause(1).release().perform()

        # ActionChains(self.driver).click_and_hold(price_max).pause(1).move_by_offset(-0.001, 0).release().perform()
        # print(price_max.get_attribute('aria-valuenow'))

        # self.driver.execute_script("arguments[0].click();", price_max)
        # self.driver.execute_script("arguments[0].setAttribute('aria-valuetext',arguments[1]);", price_max, '$800 USD')

        def price_helper():
            while True:
                count = 0
                print('price_max = ' + price_max.get_attribute('aria-valuenow') + ' our_max_price = ' + str(
                    max_price) + ' count = ' + str(count))
                if price_max.get_attribute('aria-valuemax') < str(max_price):
                    ActionChains(self.driver).drag_and_drop_by_offset(price_max, count, 0).pause(1).release().perform()
                    count += .5
                elif price_max.get_attribute('aria-valuemax') > str(max_price):
                    ActionChains(self.driver).drag_and_drop_by_offset(price_min, count, 0).pause(1).release().perform()
                    count -= .5
                elif price_max.get_attribute('aria-valuemax') == str(max_price):
                    break

        save_button = self.driver.find_element_by_id("filter-panel-save-button")
        save_button.click()

    def rooms_and_beds(self, beds=0, bedrooms=0, bathrooms=0):
        try:
            beds_button = self.driver.find_element_by_css_selector(
                'button[data-testid="filterItem-rooms_and_beds-stepper-min_beds-0-increase-button"]'
            )
            for _ in range(beds):
                beds_button.click()

            bedrooms_button = self.driver.find_element_by_css_selector(
                'button[data-testid="filterItem-rooms_and_beds-stepper-min_bedrooms-0-increase-button"]'
            )
            for _ in range(bedrooms):
                bedrooms_button.click()

            bathrooms_button = self.driver.find_element_by_css_selector(
                'button[data-testid="filterItem-rooms_and_beds-stepper-min_bathrooms-0-increase-button"]'
            )
            for _ in range(bathrooms):
                bathrooms_button.click()
        except NoSuchElementException:
            pass

    def show_amenities(self):
        total_amenity_options = []
        amenities_group = self.driver.find_element_by_xpath('//div[@aria-label="Amenities"]')
        try:
            more_amenity_options = amenities_group.find_element_by_xpath('.//button[@class="_1rf289cv"]')
            more_amenity_options.click()
        except NoSuchElementException:
            pass

        total_amenity_options = amenities_group.find_elements_by_xpath(".//div[@class='_1097lmro']")

        table = PrettyTable()
        table.field_names = ['Amenities']
        for item in total_amenity_options:
            table.add_row([item.text])

        print(table)

    def amenities_filter(self, *amenities):
        total_amenity_options = []
        amenities_group = self.driver.find_element_by_xpath('//div[@aria-label="Amenities"]')
        total_amenity_options = amenities_group.find_elements_by_xpath(".//div[@class='_1097lmro']")

        for amenity in amenities:
            if amenity == 'none'.lower():
                break
            for amenity_option in total_amenity_options:
                if amenity.lower() == amenity_option.text.lower():
                    amenity_option.click()

    def show_facilities(self):
        total_facilities_options = []
        facilities_options = self.driver.find_element_by_xpath('//div[@aria-label="Facilities"]')
        try:
            more_facility_options = facilities_options.find_element_by_xpath('.//button[@class="_1rf289cv"]')
            more_facility_options.click()
        except NoSuchElementException:
            pass

        total_facilities_options = facilities_options.find_elements_by_xpath(".//div[@class='_1097lmro']")
        t = PrettyTable()
        t.field_names = ['Facilities']
        for item in total_facilities_options:
            t.add_row([item.text])
        print(t)

    def facilities_filter(self, *facilities):
        total_facilities_options = []
        facilities_options = self.driver.find_element_by_xpath('//div[@aria-label="Facilities"]')
        total_facilities_options = facilities_options.find_elements_by_xpath(".//div[@class='_1097lmro']")

        for facility in facilities:
            if facility == 'none'.lower():
                break
            for facility_option in total_facilities_options:
                if facility.lower() == facility_option.text.lower():
                    facility_option.click()

    def show_properties(self):
        total_property_type_options = []
        property_type_options = self.driver.find_element_by_xpath('//div[@aria-label="Property type"]')
        try:
            more_property_type_options = property_type_options.find_element_by_xpath('.//button[@class="_1rf289cv"]')
            more_property_type_options.click()
        except NoSuchElementException:
            pass
        total_property_type_options = property_type_options.find_elements_by_xpath(".//div[@class='_1097lmro']")
        t = PrettyTable()
        t.field_names = ['Property Types']
        for item in total_property_type_options:
            t.add_row([item.text])
        print(t)

    def property_type_filter(self, *properties):
        total_property_type_options = []
        property_type_options = self.driver.find_element_by_xpath('//div[@aria-label="Property type"]')
        total_property_type_options = property_type_options.find_elements_by_xpath(".//div[@class='_1097lmro']")

        for prop in properties:
            if prop == 'none'.lower():
                break
            for property_types in total_property_type_options:
                if prop.lower() == property_types.text.lower():
                    property_types.click()

    def show_unique_stays(self):
        total_unique_stay_options = []
        unique_stay_options = None
        try:
            unique_stay_options = self.driver.find_element_by_xpath('//div[@aria-label="Unique stays"]')
            more_unique_stay_options = unique_stay_options.find_element_by_xpath('.//button[@class="_1rf289cv"]')
            more_unique_stay_options.click()
            total_unique_stay_options = unique_stay_options.find_elements_by_xpath(".//div[@class='_1097lmro']")
            t = PrettyTable()
            t.field_names = ['Unique stays']
            for item in total_unique_stay_options:
                t.add_row([item.text])
            print(t)
        except NoSuchElementException:
            pass

    def unique_stays_filter(self, *unique_stays):
        total_unique_stay_options = []
        try:
            unique_stay_options = self.driver.find_element_by_xpath('//div[@aria-label="Unique stays"]')
            total_unique_stay_options = unique_stay_options.find_elements_by_xpath(".//div[@class='_1097lmro']")
            for stay in unique_stays:
                if stay == 'none'.lower():
                    break
                for stay_option in total_unique_stay_options:
                    if stay.lower() == stay_option.text.lower():
                        stay_option.click()
        except NoSuchElementException:
            pass

    def show_house_rules(self):
        total_house_rules_options = []
        house_rules_options = self.driver.find_element_by_xpath('//div[@aria-label="House rules"]')
        total_house_rules_options = house_rules_options.find_elements_by_xpath(".//div[@class='_1097lmro']")

        t = PrettyTable()
        t.field_names = ['House Rules']
        for item in total_house_rules_options:
            t.add_row([item.text])

        print(t)

    def house_rules_filter(self, *house_rules):
        total_house_rules_options = []
        house_rules_options = self.driver.find_element_by_xpath('//div[@aria-label="House rules"]')
        total_house_rules_options = house_rules_options.find_elements_by_xpath(".//div[@class='_1097lmro']")

        for house_rule in house_rules:
            if house_rule == 'none'.lower():
                break
            for house_rule_option in total_house_rules_options:
                if house_rule.lower() == house_rule_option.text.lower():
                    house_rule_option.click()

    def show_stays(self):
        show_stays_button = self.driver.find_element_by_css_selector(
            'button[data-testid="more-filters-modal-submit-button"]'
        )
        show_stays_button.click()
