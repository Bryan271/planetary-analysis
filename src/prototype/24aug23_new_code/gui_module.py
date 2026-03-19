# gui_module.py

# When we set up the logger.py module, it will provide logging functions that can be used to log various events, errors, or other relevant information. 
#    Once logger.py is established, we can then revisit modules like gui_module.py and selenium_module.py to integrate these logging functions.
#    For instance, in the selenium_module.py code you referenced, the comment # Here, you can add the logging mechanism is a placeholder indicating where we might add a call to a logging function from logger.py to log the occurrence of a TimeoutException.
#    By doing this, we ensure that all significant events, errors, and other relevant data are logged systematically across all modules. This approach provides a centralized way to handle logging and makes it easier to maintain and expand the codebase in the future.
#    So, to reiterate, after setting up the logger.py, we will integrate its functions into the existing modules wherever logging is deemed necessary

# using 'grid' geometry for future added features

# gui_module.py

import tkinter as tk
from selenium_module import SeleniumHandler

class AutomaticScreenshotGUI:
    def __init__(self, root):
        print("initializing environment CLASS: (__init__(self, root))")
        self.root = root
        self.selenium_handler = SeleniumHandler(self.root)
        # print("   self.screenshot_counter value: ", self.selenium_handler.screenshot_counter)
        print("   self.screenshot_counter_a value: ", self.selenium_handler.screenshot_counter_a)


        self.create_widgets()
        print("   (create_widgets)")
        self.center_window_title()
        print("   (center_window_title)")

    def create_widgets(self):
        # Screenshot Interval Entry
        interval_label = tk.Label(self.root, text="Mapping Interval (minutes):")
        interval_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.interval_entry = tk.Entry(self.root)
        self.interval_entry.grid(row=0, column=1, padx=10, pady=10)
        self.interval_entry.insert(tk.END, "5")

        # Start Screenshot Button
        start_button = tk.Button(self.root, text="Start Mapping Analysis", command=self.start_screenshot, width=20, height=3)
        start_button.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        # Stop Screenshot Button
        stop_button = tk.Button(self.root, text="Stop Mapping Analysis", command=self.stop_screenshot, width=20, height=3)
        stop_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

    def center_window_title(self):
        window_width = 650
        window_height = 450
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2 - 30
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def start_screenshot(self):
        print("(start_screenshot)")
        interval_minutes = self.interval_entry.get()
        try:
            self.selenium_handler.set_screenshot_interval(int(interval_minutes) * 60)
        except ValueError:
            print("Invalid interval. Using default value.")
        self.selenium_handler.continue_screenshot()

    def stop_screenshot(self):
        self.screenshot_started = False
        self.selenium_handler.close_link()  # Close the link
        print("(stop_screenshot)")
