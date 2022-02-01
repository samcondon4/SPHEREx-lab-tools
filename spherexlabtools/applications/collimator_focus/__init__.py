import os
import logging

# import experiment configuration names #
from .measure import RECORDERS, VIEWERS, PROCEDURES
from .hw import INSTRUMENT_SUITE
from .control import CONTROLLERS

# configure experiment logger #
LOG_FILE = os.path.join(os.getcwd(), "spherexlabtools", "applications",
                        "collimator_focus", "collimator_focus.log")
LOG_FORMAT = "%(levelname)s:%(asctime)s::%(name)s:%(message)s"
LOG_LEVEL = logging.INFO

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(LOG_LEVEL)
LOG_FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(LOG_FORMATTER)
LOGGER.addHandler(FILE_HANDLER)
