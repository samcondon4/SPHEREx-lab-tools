""" This module provides a set of subclasses of the pymeasure Anaheim Automation DPSeriesMotorController class to implement
    concurrency and additional properties that are out of scope for a pymeasure driver.
Sam Condon, 11/17/2021
"""

import logging
import threading
from pymeasure.instruments.anaheimautomation import DPSeriesMotorController


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class LinearStageController(DPSeriesMotorController):
    """ Represents a Anaheim DP Series Motor Controller driving a linear stage. This class overrides the home()
        method and implements unit conversions between controller steps and distance along the linear stage.
    :param resource_name: string resource name to pass to pymeasure driver.
    :param homedir: string with value "CW" or "CCW" corresponding to the direction the motor is spun during a
                    homing operation.
    :param kwargs: pymeasure driver kwargs

    :var homedir: Direction that the controller should turn the motor in a homing operation. Valid values are "CW" and
                  "CCW" (default = "CCW")
    :var homespeed: Speed that the controller will turn the motor in a homing operation. Default = 500
    :var turns_per_step: motor turns per individual controller step.
    :var units_per_turn: distance in specified units that the linear stage travels in a single turn of the motor.

    """

    # homing attributes #
    homedir = None
    homespeed = 500

    # unit conversion constants #
    turns_per_step = None
    units_per_turn = None
    units = None

    # dictionary of locks for thread-safety #
    locks = {}

    def __init__(self, resource_name, homedir, encoder_motor_ratio=1.0, encoder_enabled=False, **kwargs):
        """ Instantiate a stage controller.
        """
        self.resource_name = resource_name
        if resource_name not in LinearStageController.locks.keys():
            LinearStageController.locks[resource_name] = threading.Lock()
        super().__init__(resourceName=resource_name, **kwargs)
        self.homedir = homedir
        self.encd_enabled = encoder_enabled
        self.encd_mot_ratio = encoder_motor_ratio

    def absolute_to_steps(self, pos):
        """ Convert from absolute position on a linear stage to steps.
        :param pos: absolute position in units defined by the absolute_units property.
        :return:
        """
        return int(pos*(1/self.units_per_turn)*(1/self.turns_per_step))

    def steps_to_absolute(self, steps):
        """ Convert from steps to an absolute position on a linear stage.
        :param steps:
        :return:
        """
        if self.encd_enabled:
            steps = steps / self.encd_mot_ratio
        return steps*self.turns_per_step*self.units_per_turn

    def home(self, home_mode=None, block_interval=3):
        """ Override of the home method to home using a slew to hard limit.
        :param home_mode: In this overridden version, this name is irrelevant.
        :param block_interval: Seconds between "busy" queries. Same argument as interval in wait_for_completion.
        :return: None
        """
        prev_maxspeed = self.maxspeed
        self.maxspeed = self.homespeed
        self.move(self.homedir)
        self.wait_for_completion(interval=block_interval)
        self.reset_position()
        self.maxspeed = prev_maxspeed

    def write(self, command):
        """Override the instrument base write method to add the motor controller's address to the
        command string.

        :param command: command string to be sent to the motor controller.
        """
        log.debug("LinearStageController acquiring lock for write.")
        with LinearStageController.locks[self.resource_name]:
            super().write(command)
        log.debug("LinearStageController released lock for write.")

    def values(self, command, **kwargs):
        """ Override the instrument base values method to add the motor controller's address to the
        command string.

        :param command: command string to be sent to the motor controller.
        """
        log.debug("LinearStageController acquiring lock for values.")
        with LinearStageController.locks[self.resource_name]:
            vals = super().values(command, **kwargs)
        log.debug("LinearStageController released lock for values.")
        return vals

    def ask(self, command):
        """ Override the instrument base ask method to add the motor controller's address to the
        command string.

        :param command: command string to be sent to the instrument
        """
        logging.debug("LinearStageController acquiring lock for ask.")
        with LinearStageController.locks[self.resource_name]:
            val = super().ask(command)
        logging.debug("LinearStageController released lock for ask.")
        return val
