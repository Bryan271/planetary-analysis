# selenium_module.py

from selenium import webdriver
import datetime

from selenium.common.exceptions import TimeoutException, WebDriverException
from logger import Logger

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class SeleniumHandler:
    def __init__(self, root):
        self.retry_counter = 0
        self.root = root
        self.driver = None
        self.cycle_start_time = None

        self.logger = Logger("SeleniumHandler")
        self.screenshot_interval = 1 * 60  # 1 minute

        # Define links and counters
        self.links = [
            ("https://www.ventusky.com/?p=27;-102;2&l=pressure", "aaa_", "screenshot_counter_a"),
            ("https://www.ventusky.com/?p=27;-102;2&l=radar", "bbb_", "screenshot_counter_b"),
            ("https://www.ventusky.com/?p=36.2;-97.2;3&l=radar", "ccc_", "screenshot_counter_c"),
            ("https://www.ventusky.com/?p=39.4;-96.3;4&l=radar", "ddd_", "screenshot_counter_d"),
            ("https://www.ventusky.com/?p=43.42;-76.38;6&l=radar", "eee_", "screenshot_counter_e")
        ]
        self.current_link_index = 0

        # Initialize counters for each link
        self.screenshot_counter_a = 3067
        self.screenshot_counter_b = 3067
        self.screenshot_counter_c = 3067
        self.screenshot_counter_d = 3067
        self.screenshot_counter_e = 3067

    def set_screenshot_interval(self, interval):
        self.screenshot_interval = interval

    def open_link(self):
        start_time = datetime.datetime.now()  # Record the start time for this link

        if not self.driver:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
            try:
                link, _, _ = self.links[self.current_link_index]
                self.driver.get(link)
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                self.logger.log_info(f"Opened the link {link} in the browser.")
                self.retry_counter = 0  # Reset the retry counter if the page loads successfully
            except (TimeoutException, WebDriverException) as e:
                self.logger.log_error("The website took too long to load.")
                self.close_link()
                if self.retry_counter < 1:  # Only retry once
                    self.retry_counter += 1
                    self.continue_screenshot()  # Retry opening the link
                else:
                    self.logger.log_error("Retry limit reached. Waiting for the next interval.")
                    elapsed_time = (datetime.datetime.now() - start_time).seconds
                    wait_time = max(0, 60 - elapsed_time)
                    # wait_time = 60 - elapsed_time
                    self.root.after(wait_time * 1000, self.continue_screenshot)
                    self.retry_counter = 0

    def close_link(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.logger.log_info("Closed the browser.")

    def take_screenshot(self):
        if self.driver:
            _, prefix, counter_name = self.links[self.current_link_index]
            counter_value = getattr(self, counter_name)
            screenshot_name = f"{prefix}{str(counter_value).zfill(6)}.png"
            self.driver.save_screenshot(screenshot_name)
            self.logger.log_info(f"Saved screenshot as {screenshot_name}.")
            setattr(self, counter_name, counter_value + 1)
            self.close_link()

            # Increment the current link index
            self.current_link_index = (self.current_link_index + 1) % len(self.links)
            self.logger.log_info(f"Current link index set to {self.current_link_index}.")

            # Calculate the time since the cycle started
            elapsed_time = (datetime.datetime.now() - self.cycle_start_time).seconds

            if self.current_link_index == 0:  # If we've cycled through all links
                # Calculate the remaining time for the entire cycle to complete in 5 minutes
                remaining_time = max(0, 300 - elapsed_time)
                self.logger.log_info(f"Waiting for {remaining_time} seconds before starting the cycle again.")
                self.root.after(remaining_time * 1000, self.continue_screenshot)
                self.cycle_start_time = None
            else:
                # Calculate the time left to wait for the next link to open
                wait_time = 60 - (elapsed_time % 60)
                self.logger.log_info(f"Waiting for {wait_time} seconds before opening the next link.")
                self.root.after(wait_time * 1000, self.continue_screenshot)



    def continue_screenshot(self):
        self.logger.log_info("In continue_screenshot method.")
        if self.cycle_start_time is None:
            self.cycle_start_time = datetime.datetime.now()
            self.logger.log_info("Starting a new cycle.")

        self.open_link()
        self.logger.log_info("Waiting for 15 seconds before taking a screenshot.")
        self.root.after(15000, self.take_screenshot)
