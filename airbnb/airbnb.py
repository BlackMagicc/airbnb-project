import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
import datetime
import airbnb.constants as const
from .airbnb_filter import *
from .airbnb_report import AirbnbReport
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import date
from prettytable import PrettyTable
import time


class Airbnb(webdriver.Chrome):
    def __init__(self, teardown=False):
        self.driver = webdriver.Chrome()
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Airbnb, self).__init__(options=options)
        self.implicitly_wait(10)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def select_place_to_go(self, place_to_go):
        try:
            element = WebDriverWait(self, 2).until(
                EC.presence_of_element_located((By.ID, "bigsearch-query-detached-query-input"))
            )
        except:
            # self.driver.quit()
            pass

        search_field = self.find_element_by_id("bigsearch-query-detached-query-input")

        try:
            search_field.send_keys(place_to_go)
        except StaleElementReferenceException:
            search_field = self.find_element_by_xpath("//div[@class='_gor68n']")
            search_field.send_keys(place_to_go)

    def select_dates(self, check_in_date, check_out_date):
        # while True:
        #     try:
        #         datetime.datetime.strptime(check_in_date, '%Y-%m-%d')
        #     except ValueError:
        #         raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        #     else:
        #         break
        today = date.today()
        dtf = pd.date_range(start=today, end=check_in_date, freq="D")
        # range from today to check in
        # tells us how many times we have to loop to first check in date
        initial_month_range = (dtf[-1].to_period('M') - dtf[0].to_period('M')).n

        dtr = pd.date_range(start=check_in_date, end=check_out_date, freq="D")
        # range from check in date to check out date
        # will tell us how many times we have to loop to next month
        month_range = (dtr[-1].to_period('M') - dtr[0].to_period('M')).n

        check_in_button = self.find_element_by_xpath(
            '//div[@data-testid="structured-search-input-field-split-dates-0"]'
        )
        check_in_button.click()
        while initial_month_range > 1:
            next_month_button = self.find_element_by_css_selector(
                'button[aria-label="Next"]'
            )
            next_month_button.click()
            initial_month_range -= 1
        check_in_day = WebDriverWait(self, 3).until(
            EC.element_to_be_clickable((By.XPATH, f'//div[@data-testid="datepicker-day-{check_in_date}"]'))
        )
        check_in_day.click()

        if month_range >= 1:
            while month_range >= 1:
                next_month_button = WebDriverWait(self, 3).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@class="_13tn83am"]'))
                ).click()
                month_range -= 1

        check_out_day = WebDriverWait(self, 3).until(
            EC.element_to_be_clickable((By.XPATH, f'//div[@data-testid="datepicker-day-{check_out_date}"]'))
        )
        check_out_day.click()

    def select_guests(self, count=0):
        guest_button = self.find_element_by_class_name(
            "_37ivfdq"
        )
        guest_button.click()

        guest_button_increase = self.find_element_by_css_selector(
            'button[aria-label="increase value"]'
        )

        for _ in range(count):
            guest_button_increase.click()

    def search(self):
        search_button = self.find_element_by_css_selector(
            'button[data-testid="structured-search-input-search-button"]'
        )
        search_button.click()

    def more_filters(self):
        filter_button = None
        try:
            rooms_and_beds_button = WebDriverWait(self, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Rooms and beds"]'))
            )
            rooms_and_beds_button.click()
            filtration = AirbnbFilter(driver=self)
            filtration.rooms_and_beds(4, 2, 2)

            save_button = WebDriverWait(self, 3).until(
                EC.element_to_be_clickable((By.ID, "filter-panel-save-button"))
            )
            save_button.click()
        except (NoSuchElementException, TimeoutException):
            pass

        filter_button = self.find_element_by_xpath('//div[@id="menuItemButton-dynamicMoreFilters"]')
        filter_button.click()

    def apply_filters(self):
        filtration = AirbnbFilter(driver=self)
        # filtration.price_range(300, 855)
        # filtration.rooms_and_beds(int(input('How many beds are you looking for? ')),
        #                           int(input('How many bedrooms are you looking for? ')),
        #                           int(input('How many bathrooms are you looking for? ')))
        # filtration.show_amenities()
        # filtration.amenities_filter(input("Which of the available amenities would you like? (Enter 'none' to skip) "))
        # filtration.show_facilities()
        # filtration.facilities_filter(input("What type of facility are you interested in? (Enter 'none' to skip) "))
        # filtration.show_properties()
        # filtration.property_type_filter(input("What type of property? (Enter 'none' to skip) "))
        # filtration.show_unique_stays()
        # filtration.unique_stays_filter(input("Unique stay? (Enter 'none' to skip) "))
        # filtration.show_house_rules()
        # filtration.house_rules_filter(input("Preferred house rules? (Enter 'none' top skip) "))
        # filtration.show_stays()

        filtration.rooms_and_beds(4, 2, 2)
        filtration.show_amenities()
        filtration.amenities_filter('wifi', 'tv')
        filtration.show_facilities()
        filtration.facilities_filter('pool')
        filtration.show_properties()
        filtration.property_type_filter('house', 'apartment')
        filtration.show_unique_stays()
        filtration.unique_stays_filter('none')
        filtration.show_house_rules()
        filtration.house_rules_filter('none')
        filtration.show_stays()

    def report_results(self):
        airbnb_listings = self.find_element_by_class_name(
            '_twmmpk'
        )
        report = AirbnbReport(airbnb_listings)
        table = PrettyTable(
            field_names=["Airbnb Name", "Airbnb Price", "Total Airbnb Price",
                         'Airbnb Rating', 'Airbnb Link']
        )
        table.add_rows(report.pull_airbnb_details())
        print(table)
