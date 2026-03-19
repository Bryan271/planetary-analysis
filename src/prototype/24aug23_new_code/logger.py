# logger.py

import logging
import os
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, log_name):
        self.log_dir = "logs"
        self.create_log_directory()  # Create the log directory if it doesn't exist

        # Set up the logger
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG)

        # Create a rotating file handler for writing logs with a max size of 5 MB and 3 backup files
        file_handler = RotatingFileHandler(f"{self.log_dir}/{log_name}.log", maxBytes=5*1024*1024, backupCount=3)
        file_handler.setLevel(logging.DEBUG)

        # Create a console handler for printing logs
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def create_log_directory(self):
        """Creates a directory for logs if it doesn't exist."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            print(f"Created log directory: {self.log_dir}")

    def log_info(self, message):
        print(message)  # Print to console
        self.logger.info(message)  # Log to file

    def log_warning(self, message):
        print(f"WARNING: {message}")  # Print to console with a "WARNING" prefix
        self.logger.warning(message)  # Log to file

    def log_error(self, message):
        print(f"ERROR: {message}")  # Print to console with an "ERROR" prefix
        self.logger.error(message)  # Log to file

    def log_exception(self, message):
        print(f"EXCEPTION: {message}")  # Print to console with an "EXCEPTION" prefix
        self.logger.exception(message)  # Log to file with traceback
