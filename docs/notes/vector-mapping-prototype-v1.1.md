The Automated Vector Mapping Prototype v1.1 is a specialized application
designed to automate the process of capturing web-based vector maps at
user-defined intervals. Utilizing a combination of a graphical user
interface (GUI) and web automation, the program allows users to specify
the frequency of screenshots and then captures images from predefined
web URLs. The program is modular in design, with distinct components
handling the GUI, web automation via Selenium, and event logging. This
outline provides a detailed breakdown of each module, offering insights
into their individual functionalities and their interplay in the broader
context of the application.

**1. main.py**

-   **Purpose**: This is the entry point of the application. It
    initializes the main GUI window and starts the GUI event loop.

-   **Components**:

    -   **Tkinter Root Window Initialization**: Creates the main window
        for the application.

    -   **AutomaticScreenshotGUI Instance**: Initializes the GUI class,
        which sets up the user interface and its functionalities.

    -   **GUI Event Loop**: Keeps the GUI running and responsive to user
        interactions.

**2. gui_module.py**

-   **Purpose**: This module defines the graphical user interface (GUI)
    of the application, allowing the user to set parameters and control
    the screenshot process.

-   **Components**:

    -   **AutomaticScreenshotGUI Class**:

        -   **Initialization**: Sets up the Selenium handler and
            initializes the GUI components.

        -   **create_widgets()**: Defines and positions the GUI
            elements, such as labels, entry fields, and buttons.

        -   **center_window_title()**: Adjusts the position and size of
            the main window to center it on the screen.

        -   **start_screenshot()**: Retrieves the user-defined interval
            and starts the screenshot process.

        -   **stop_screenshot()**: Stops the screenshot process and
            closes the browser.

**3. selenium_module.py**

-   **Purpose**: This module handles the web browser automation using
    Selenium. It opens specified URLs, waits for them to load, and takes
    screenshots.

-   **Components**:

    -   **SeleniumHandler Class**:

        -   **Initialization**: Sets up the Selenium WebDriver and
            initializes the logger.

        -   **set_screenshot_interval()**: Allows setting the interval
            between screenshots.

        -   **open_link()**: Opens the specified URL in the browser and
            waits for it to load. Implements error handling for timeouts
            and other exceptions.

        -   **close_link()**: Closes the browser window.

        -   **take_screenshot()**: Captures a screenshot of the
            currently opened web page and saves it with a specific
            naming convention.

        -   **continue_screenshot()**: Continues the screenshot process
            by opening the next link and setting up the next screenshot
            capture.

**4. logger.py**

-   **Purpose**: This module provides logging functionalities. It
    creates and manages log files to record events, errors, and other
    relevant information during the program\'s execution.

-   **Components**:

    -   **Logger Class**:

        -   **Initialization**: Sets up the logger with specific
            formatting and handlers for both file and console logging.

        -   **create_log_directory()**: Ensures the existence of a
            directory for storing log files.

        -   **log_info()**: Logs informational messages.

        -   **log_warning()**: Logs warning messages.

        -   **log_error()**: Logs error messages.

        -   **log_exception()**: Logs exceptions along with their
            tracebacks.

> **main.py-module**

\# main.py

\# This file serves as the entry point for the application.

\# It initializes the main window, sets up the GUI, and starts

\# the event loop. The actual GUI logic and other functionalities

\# will be handled in the respective modules.

import tkinter as tk

from gui_module import AutomaticScreenshotGUI

\# Create the main window

root = tk.Tk()

root.title(\"Vector Mapping Prototype v1.1\")

print(\"root.title\")

\# Create an instance of the GUI class

gui = AutomaticScreenshotGUI(root)

print(\"gui\")

\# Start the GUI event loop

root.mainloop()

> **gui_module.py-module**

\# gui_module.py

\# When we set up the logger.py module, it will provide logging
functions that can be used to log various events, errors, or other
relevant information.

\#    Once logger.py is established, we can then revisit modules like
gui_module.py and selenium_module.py to integrate these logging
functions.

\#    For instance, in the selenium_module.py code you referenced, the
comment \# Here, you can add the logging mechanism is a placeholder
indicating where we might add a call to a logging function from
logger.py to log the occurrence of a TimeoutException.

\#    By doing this, we ensure that all significant events, errors, and
other relevant data are logged systematically across all modules. This
approach provides a centralized way to handle logging and makes it
easier to maintain and expand the codebase in the future.

\#    So, to reiterate, after setting up the logger.py, we will
integrate its functions into the existing modules wherever logging is
deemed necessary

\# using \'grid\' geometry for future added features

\# gui_module.py

import tkinter as tk

from selenium_module import SeleniumHandler

class AutomaticScreenshotGUI:

    def \_\_init\_\_(self, root):

        print(\"initializing environment CLASS: (\_\_init\_\_(self,
root))\")

        self.root = root

        self.selenium_handler = SeleniumHandler(self.root)

        print(\"   self.screenshot_counter value: \",
self.selenium_handler.screenshot_counter)

        self.create_widgets()

        print(\"   (create_widgets)\")

        self.center_window_title()

        print(\"   (center_window_title)\")

    def create_widgets(self):

        \# Screenshot Interval Entry

        interval_label = tk.Label(self.root, text=\"Mapping Interval
(minutes):\")

        interval_label.grid(row=0, column=0, padx=10, pady=10,
sticky=tk.W)

        self.interval_entry = tk.Entry(self.root)

        self.interval_entry.grid(row=0, column=1, padx=10, pady=10)

        self.interval_entry.insert(tk.END, \"5\")

        \# Start Screenshot Button

        start_button = tk.Button(self.root, text=\"Start Mapping
Analysis\", command=self.start_screenshot, width=20, height=3)

        start_button.grid(row=1, column=0, columnspan=2, padx=20,
pady=10)

        \# Stop Screenshot Button

        stop_button = tk.Button(self.root, text=\"Stop Mapping
Analysis\", command=self.stop_screenshot, width=20, height=3)

        stop_button.grid(row=2, column=0, columnspan=2, padx=20,
pady=10)

    def center_window_title(self):

        window_width = 650

        window_height = 450

        screen_width = self.root.winfo_screenwidth()

        screen_height = self.root.winfo_screenheight()

        x = (screen_width - window_width) // 2

        y = (screen_height - window_height) // 2 - 30

        self.root.geometry(f\"{window_width}x{window_height}+{x}+{y}\")

    def start_screenshot(self):

        print(\"(start_screenshot)\")

        interval_minutes = self.interval_entry.get()

        try:

           
self.selenium_handler.set_screenshot_interval(int(interval_minutes) \*
60)

        except ValueError:

            print(\"Invalid interval. Using default value.\")

        self.selenium_handler.continue_screenshot()

    def stop_screenshot(self):

        self.screenshot_started = False

        self.selenium_handler.close_link()  # Close the link

        print(\"(stop_screenshot)\")

> **selenium_module.py-module**

#selenium_module.py

\# This module integrates the logging mechanism from logger.py to log
events and exceptions.

\# The print statements are retained to provide terminal outputs for
debugging and tracking the program\'s flow

#selenium_module.py

from selenium import webdriver

import datetime

from selenium.common.exceptions import TimeoutException,
WebDriverException

\# from selenium.common.exceptions import TimeoutException

from logger import Logger

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

class SeleniumHandler:

    def \_\_init\_\_(self, root):

        self.retry_counter = 0

        self.root = root

        self.driver = None

        self.screenshot_counter = 1461

        self.logger = Logger(\"SeleniumHandler\")

        self.screenshot_interval = 5 \* 60  # Default value

    def set_screenshot_interval(self, interval):

        self.screenshot_interval = interval

    def open_link(self):

        if not self.driver:

            print(\"(open_link)\")

            self.driver = webdriver.Chrome()

            print(\"   running self.driver\")

            print(\"   self.driver value: \", self.driver)

            self.driver.maximize_window()

            try:

                    \# Testing URL

                    \#
self.driver.get(\"http://www.nonexistentwebsite12345.com/\") \# URL used
to test TimeoutException

                   

               
self.driver.get(\"https://www.ncei.noaa.gov/maps/radar/\")

                WebDriverWait(self.driver,
30).until(EC.presence_of_element_located((By.TAG_NAME, \"body\")))

                self.logger.log_info(\"Opened the link in the
browser.\")

                self.retry_counter = 0  # Reset the retry counter if the
page loads successfully

            except (TimeoutException, WebDriverException) as e:

                self.logger.log_error(\"The website took too long to
load.\")

                self.close_link()

                if self.retry_counter \< 1:  # Only retry once

                    self.retry_counter += 1

                    self.continue_screenshot()  # Retry opening the link

                else:

                    self.logger.log_error(\"Retry limit reached. Waiting
for the next interval.\")

                    remaining_interval = self.screenshot_interval - 15

                    self.root.after(remaining_interval \* 1000,
self.continue_screenshot)

                    self.retry_counter = 0

    def close_link(self):

        if self.driver:

            self.driver.quit()

            self.driver = None

            print(\"(close_link)\")

            print(\"   self.driver value: \", self.driver)

            self.logger.log_info(\"Closed the browser.\")

    def take_screenshot(self):

        if self.driver:

            now = datetime.datetime.now()

            print(\"(take_screenshot)\")

            print(\"   self.driver value: \", self.driver)

            screenshot_name =
f\"aaa\_{str(self.screenshot_counter).zfill(6)}.png\"

            self.driver.save_screenshot(screenshot_name)

            print(\"   screenshot file \", screenshot_name, \" is saved
at: \", now.strftime(\"%H:%M:%S\"))

            self.logger.log_info(f\"Saved screenshot as
{screenshot_name}.\")

            self.screenshot_counter += 1

            print(\"   Next file number value: \",
self.screenshot_counter)

            self.close_link()

            remaining_interval = self.screenshot_interval - 15

            self.root.after(remaining_interval \* 1000,
self.continue_screenshot)

    def continue_screenshot(self):

        print(\"(continue_screenshot)\")

        self.open_link()

        self.root.after(15000, self.take_screenshot)

> **logger.py-module**

\# logger.py

\# Set up a logger with a specific format for the log messages.

\# Provide functions to log different types of messages (e.g., info,
error).

\# Handle the creation of separate log files for different purposes or
modules.

import logging

import os

class Logger:

    def \_\_init\_\_(self, log_name):

        self.log_dir = \"logs\"

        self.create_log_directory()  # Create the log directory if it
doesn\'t exist

        \# Set up the logger

        self.logger = logging.getLogger(log_name)

        self.logger.setLevel(logging.DEBUG)

        \# Create a file handler for writing logs

        file_handler =
logging.FileHandler(f\"{self.log_dir}/{log_name}.log\")

        file_handler.setLevel(logging.DEBUG)

        \# Create a console handler for printing logs

        console_handler = logging.StreamHandler()

        console_handler.setLevel(logging.DEBUG)

        \# Create a formatter

        formatter = logging.Formatter(\'%(asctime)s - %(levelname)s -
%(message)s\')

        file_handler.setFormatter(formatter)

        console_handler.setFormatter(formatter)

        \# Add the handlers to the logger

        self.logger.addHandler(file_handler)

        self.logger.addHandler(console_handler)

    def create_log_directory(self):

        \"\"\"Creates a directory for logs if it doesn\'t exist.\"\"\"

        if not os.path.exists(self.log_dir):

            os.makedirs(self.log_dir)

            print(f\"Created log directory: {self.log_dir}\")

    def log_info(self, message):

        print(message)  # Print to console

        self.logger.info(message)  # Log to file

    def log_warning(self, message):

        print(f\"WARNING: {message}\")  # Print to console with a
\"WARNING\" prefix

        self.logger.warning(message)  # Log to file

    def log_error(self, message):

        print(f\"ERROR: {message}\")  # Print to console with an
\"ERROR\" prefix

        self.logger.error(message)  # Log to file

    def log_exception(self, message):

        print(f\"EXCEPTION: {message}\")  # Print to console with an
\"EXCEPTION\" prefix

        self.logger.exception(message)  # Log to file with traceback
