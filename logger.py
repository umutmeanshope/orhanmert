import logging
import traceback


def trace():

    return traceback.format_exc()


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