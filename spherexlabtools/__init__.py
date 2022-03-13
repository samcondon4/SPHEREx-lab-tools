""" spherexlabtools
"""
import os
import logging


# version number #
__version__ = "0.6"

# configure logging #
LOG_FILE = "slt.log"
LOG_FORMAT = "%(levelname)s:%(asctime)s::%(name)s:%(message)s"
LOG_LEVEL = logging.INFO
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)
logging.info("SPHERExLABTOOLS VERSION %s" % __version__)

# Base package namespace
from .experiment import create_experiment
