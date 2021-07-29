""" housekeeping.py:

    This module implements the HousekeepingProcess class. This class provides a base class for any data logging
    processes that must run continuously.

Sam Condon, 07/04/2021
"""
import asyncio
import pandas as pd
import numpy as np
from datetime import datetime


class Housekeeping:
    task = None
    log_methods = {}
    time_sync_method = None

    def __init__(self):
        self.log_path = None
        self.log_method = None
        self.get_log_method = None
        self.logging = False
        self.log_df = None
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
            self.logging = True

    async def off_data_log(self):
        """off_data_log: Turn off data logging for a Housekeeping instance by removing the instance log method from the
                         class log_methods dictionary.

        """
        async with self.log_lock:
            Housekeeping.log_methods.pop(self.log_method["identifier"])
            print(Housekeeping.log_methods)
            self.logging = False

    async def get_log(self, start=None, end=None, final_val=False):
        """get_log: Get logged data between the specified start and ending times. Or just get the final value.
        """
        try:
            df = pd.read_csv(self.log_path)
        except FileNotFoundError as e:
            print(e)
        else:
            async with self.log_lock:
                if final_val:
                    df = df.iloc[-1]
                else:
                    time_stamps = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f") for ts in df["Time-stamp"].values]
                    indices = np.where([start < time_stamps[i] < end for i in range(len(time_stamps))])[0]
                    df = df.iloc[indices[0]:indices[-1]]
                return df

    def append_to_log(self, append_df):
        """append_to_log: Add data to the logged hk file.
        """
        if self.log_df is None:
            try:
                self.log_df = pd.read_csv(self.log_path)
            except (pd.errors.EmptyDataError, FileNotFoundError) as e:
                header = True
            else:
                header = False
        else:
            header = False
        append_df.to_csv(self.log_path, mode='a', header=header, index=False)

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
                await cls.log_methods[method]["method"]()
            await asyncio.sleep(0.2)

