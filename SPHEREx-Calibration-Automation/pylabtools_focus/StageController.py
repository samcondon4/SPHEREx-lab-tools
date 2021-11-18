""" This module provides a subclass, StageController, of the pymeasure Anaheim Automation DPSeriesMotorController class to implement 
    concurrency and additional properties that are out of scope for a pymeasure driver.

Sam Condon, 11/17/2021
"""

import logging
from time import sleep
import concurrent.futures as futures
from pymeasure.instruments.anaheimautomation import DPSeriesMotorController


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class StageController(DPSeriesMotorController):

    _turns_to_meters = None
    _absolute_units = None

    def __init__(self, resource_name, log_id, **kwargs):
        """ Instantiate a stage controller.

        :param resource_name: string resource name to pass to pymeasure driver.
        :param log_id: string with the name of the stage for log files.
        :param kwargs: pymeasure driver kwargs
        """
        super().__init__(resourceName=resource_name, **kwargs)
        self.log_id = log_id

    def absolute_to_steps(self, pos):
        """ Convert from absolute position on a linear stage to steps.

        :param pos: absolute position in units defined by the absolute_units property.
        :return:
        """
        pass

    def steps_to_absolute(self, steps):
        """ Convert from steps to an absolute position on a linear stage.

        :param steps:
        :return:
        """
        pass

    def slew(self, direction):
        """ Override of the base slew() method for concurrency.

        :param direction: same as base parameter.
        :return: None
        """
        pass

    def go(self):
        """ Override of the base go() method to implement concurrency.

        :return: None
        """
        self.write("G")
        with futures.ThreadPoolExecutor(max_workers=1) as executor:
            log.info("Stage %s moving %i steps %s from step position: %i" % (self.log_id, self.steps, self.direction,
                                                                             self.step_position))
            future = executor.submit(self.wait_for_completion, 10)
            futures.wait([future])
            log.info("Stage %s motion ended at new step position: %i" % self.step_position)

    def home(self, home_mode):
        """ Override of the home method to home using a slew to hard limit.

        :param home_mode: In this overridden version, this name is irrelevant.
        :return: None
        """
        pass

    def wait_for_completion(self, interval=0.5):
        """ Wait until the controller completes a movement.

        :param interval: (float) duration in seconds between controller busy queries.
        :return: None
        """
        while self.busy:
            sleep(interval)
