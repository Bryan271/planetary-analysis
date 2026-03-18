# Automated Vector Mapping Prototype v1.1

Reference outline for the GUI + Selenium prototype that captures map imagery on a cadence.

## Module overview
### `main.py`
- Initializes the Tkinter root window.
- Instantiates the GUI controller.
- Starts the Tk event loop.

```python
import tkinter as tk
from gui_module import AutomaticScreenshotGUI

def main():
    root = tk.Tk()
    root.title("Vector Mapping Prototype v1.1")
    AutomaticScreenshotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

### `gui_module.py`
- Builds the operator UI (interval input, start/stop buttons).
- Centers the window and wires up callbacks into the Selenium handler.
- Delegates screenshot scheduling to `SeleniumHandler`.

```python
class AutomaticScreenshotGUI:
    def __init__(self, root):
        self.root = root
        self.selenium_handler = SeleniumHandler(self.root)
        self._create_widgets()
        self._center_window()

    def _create_widgets(self):
        # interval entry + start/stop buttons defined here
        ...

    def start_screenshot(self):
        interval_minutes = int(self.interval_entry.get() or 5)
        self.selenium_handler.set_screenshot_interval(interval_minutes * 60)
        self.selenium_handler.continue_screenshot()

    def stop_screenshot(self):
        self.selenium_handler.close_link()
```

### `selenium_module.py`
- Manages Chrome WebDriver lifecycle.
- Opens URLs, waits for DOM readiness, captures screenshots, and handles retries.

```python
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class SeleniumHandler:
    def __init__(self, root):
        self.root = root
        self.driver = None
        self.logger = Logger("SeleniumHandler")
        self.screenshot_interval = 5 * 60
        self.screenshot_counter = 1461

    def open_link(self):
        if not self.driver:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
        try:
            self.driver.get("https://www.ncei.noaa.gov/maps/radar/")
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            self.logger.log_info("Opened the link in the browser.")
        except (TimeoutException, WebDriverException) as exc:
            self.logger.log_error("The website took too long to load.")
            self.close_link()
            self.root.after((self.screenshot_interval - 15) * 1000, self.continue_screenshot)

    def take_screenshot(self):
        if not self.driver:
            return
        screenshot_name = f"aaa_{self.screenshot_counter:06d}.png"
        self.driver.save_screenshot(screenshot_name)
        self.logger.log_info(f"Saved screenshot as {screenshot_name}.")
        self.screenshot_counter += 1
        self.close_link()
        self.root.after((self.screenshot_interval - 15) * 1000, self.continue_screenshot)
```

### `logger.py`
- Shared logging utility writing to both console and rotating files under `logs/`.
- Provides `log_info`, `log_warning`, `log_error`, and `log_exception`.

## Next implementation steps
1. Parameterize the URL list + capture cadence via config files.
2. Replace hard-coded screenshot names with a structured manifest.
3. Expand logging (rotation, metrics) and add integration tests for retries and shutdown.
