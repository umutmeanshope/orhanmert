import logging
import traceback

"""
Simple logger to log exceptions errors and events to keep track of things

Logging function can be partially implemented inside the UI to give the user a feedback

Logger also prints the logs on the terminal for the developer.

"""


logging.basicConfig(filename="logs.log",
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    filemode="w")

log = logging.getLogger()

log.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("logs.log")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

log.addHandler(file_handler)
log.addHandler(stream_handler)