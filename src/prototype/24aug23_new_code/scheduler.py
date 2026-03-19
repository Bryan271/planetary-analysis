# scheduler.py
import time
from selenium_module import SeleniumHandler

def start_cycle(handler):
    handler.continue_screenshot()

if __name__ == "__main__":
    # Initialize the SeleniumHandler
    handler = SeleniumHandler(None)  # Assuming you don't have a root GUI object

    while True:
        print("Starting a new cycle...")
        cycle_start_time = time.time()
        start_cycle(handler)
        elapsed_time = time.time() - cycle_start_time
        sleep_time = max(0, 300 - elapsed_time)  # Ensure the cycle lasts exactly 300 seconds
        time.sleep(sleep_time)
