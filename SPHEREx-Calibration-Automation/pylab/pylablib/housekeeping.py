""" housekeeping.py:

    This module implements the HousekeepingProcess class. This class provides a base class for any data logging
    processes that must run continuously.

Sam Condon, 07/04/2021
"""
import asyncio
import pandas as pd


class Housekeeping:
    task = None
    log_methods = {}
    time_sync_method = None

    def __init__(self):
        self.log_path = None
        self.log_method = None
        self.get_log_method = None
        self.log_lock = asyncio.Lock()

    def set_log_path(self, log_path):
        self.log_path = log_path

    def get_log_path(self):
        return self.log_path

    def set_log_method(self, identifier, log_method):
        self.log_method = {"identifier": identifier, "method": log_method}

    async def on_data_log(self):
        """on_data_log: Turn on data logging for a Housekeeping instance by adding the instance log method to the
                        class log_methods dictionary.

        """
        async with self.log_lock:
            identifier = self.log_method["identifier"]
            log_method = self.log_method["method"]
            Housekeeping.log_methods[identifier] = {"method": log_method, "lock": self.log_lock}

    async def off_data_log(self):
        """off_data_log: Turn off data logging for a Housekeeping instance by removing the instance log method from the
                         class log_methods dictionary.

        """
        async with self.log_lock:
            Housekeeping.log_methods.pop(self.log_method["identifier"])

    @classmethod
    def start(cls):
        cls.task = asyncio.create_task(cls.log())

    @classmethod
    def stop(cls):
        cls.task.cancel()

    @classmethod
    async def log(cls):
        while True:
            for method in cls.log_methods:
                await cls.log_methods[method]["lock"].acquire()
                cls.log_methods[method]["method"]()
                cls.log_methods[method]["lock"].release()
            await asyncio.sleep(0.2)

