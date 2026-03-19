#selenium_module.py

# This module integrates the logging mechanism from logger.py to log events and exceptions. 
# The print statements are retained to provide terminal outputs for debugging and tracking the program's flow

#selenium_module.py

from selenium import webdriver
import datetime

from selenium.common.exceptions import TimeoutException, WebDriverException
# from selenium.common.exceptions import TimeoutException
from logger import Logger

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class SeleniumHandler:
    def __init__(self, root):
        self.retry_counter = 0
        self.root = root
        self.driver = None
        self.screenshot_counter = 1461
        self.logger = Logger("SeleniumHandler")
        self.screenshot_interval = 5 * 60  # Default value

    def set_screenshot_interval(self, interval):
        self.screenshot_interval = interval

    def open_link(self):
        if not self.driver:
            print("(open_link)")
            self.driver = webdriver.Chrome()
            print("   running self.driver")
            print("   self.driver value: ", self.driver)
            self.driver.maximize_window()
            try:
                    # Testing URL
                    # self.driver.get("http://www.nonexistentwebsite12345.com/") # URL used to test TimeoutException
                    
                self.driver.get("https://www.ncei.noaa.gov/maps/radar/")

                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                self.logger.log_info("Opened the link in the browser.")
                self.retry_counter = 0  # Reset the retry counter if the page loads successfully
            except (TimeoutException, WebDriverException) as e:
                self.logger.log_error("The website took too long to load.")
                self.close_link()
                if self.retry_counter < 1:  # Only retry once
                    self.retry_counter += 1
                    self.continue_screenshot()  # Retry opening the link
                else:
                    self.logger.log_error("Retry limit reached. Waiting for the next interval.")
                    remaining_interval = self.screenshot_interval - 15
                    self.root.after(remaining_interval * 1000, self.continue_screenshot)
                    self.retry_counter = 0


    def close_link(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            print("(close_link)")
            print("   self.driver value: ", self.driver)
            self.logger.log_info("Closed the browser.")

    def take_screenshot(self):
        if self.driver:
            now = datetime.datetime.now()
            print("(take_screenshot)")
            print("   self.driver value: ", self.driver)
            screenshot_name = f"aaa_{str(self.screenshot_counter).zfill(6)}.png"
            self.driver.save_screenshot(screenshot_name)
            print("   screenshot file ", screenshot_name, " is saved at: ", now.strftime("%H:%M:%S"))
            self.logger.log_info(f"Saved screenshot as {screenshot_name}.")
            self.screenshot_counter += 1
            print("   Next file number value: ", self.screenshot_counter)
            self.close_link()
            remaining_interval = self.screenshot_interval - 15
            self.root.after(remaining_interval * 1000, self.continue_screenshot)

    def continue_screenshot(self):
        print("(continue_screenshot)")
        self.open_link()
        self.root.after(15000, self.take_screenshot)


