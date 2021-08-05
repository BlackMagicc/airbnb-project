from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement


class AirbnbReport:
    def __init__(self, boxes_section_element: WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements_by_class_name(
            '_1kmzzkf'
        )

    def pull_airbnb_details(self):
        collection = []
        for deal_box in self.deal_boxes:
            airbnb_name = deal_box.find_element_by_xpath(
                './/meta[@itemprop="name"]'
            ).get_attribute('content')

            airbnb_price_per_night = deal_box.find_element_by_xpath(
                './/div[@class="_12oal24"]'
            ).find_element_by_xpath(
                './/span[@class="_155sga30"]'
            ).get_attribute('innerHTML') + ' per night'
            try:
                total_airbnb_price = deal_box.find_element_by_xpath(
                    './/div[@class="_12oal24"]'
                ).find_element_by_xpath(
                    './/div[@class="_1asxs4e"]'
                ).find_element_by_xpath(
                    './/span[@aria-hidden="true"]'
                ).get_attribute('innerHTML')
            except NoSuchElementException:
                total_airbnb_price = deal_box.find_element_by_xpath(
                    './/div[@class="_12oal24"]'
                ).find_element_by_xpath(
                    './/span[@class="_155sga30"]'
                ).text + ' per month'
            try:
                airbnb_rating = deal_box.find_element_by_xpath(
                    './/div[@class="_12oal24"]'
                ).find_element_by_xpath(
                    './/div[@class="_h34mg6"]'
                ).find_element_by_xpath(
                    './/span[@class="_18khxk1"]'
                ).get_attribute('aria-label')
            except NoSuchElementException:
                airbnb_rating = 'Rating N/A'

            airbnb_link = deal_box.find_element_by_xpath(
                './/meta[@itemprop="url"]'
            ).get_attribute('content')

            collection.append(
                [airbnb_name, airbnb_price_per_night, total_airbnb_price,
                 airbnb_rating, airbnb_link]
            )
        return collection
