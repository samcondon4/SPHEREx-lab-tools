"""pylabsm_state_initializing:

    This module provides the initialization state class.

"""
import asyncio
import os
import sys

from spherexlabtools.state import SmCustomState
from spherexlabtools.instruments import PylabInstrument
from spherexlabtools.instruments import PymeasureInstrumentSub


class Initializing(SmCustomState):

    TABLES_PATH = os.path.join(os.getcwd(), "spherexlabtools", "applications", "spectral_cal", "config",
                               "sql_tables.ini")

    def __init__(self, sm, identifier="initializing", **kwargs):
        super().__init__(sm, self, identifier, **kwargs)

    def initialize_sql_server(self, action_arg):

        action_arg["Tables"] = self.define_sql_tables_and_rows_from_ini(action_arg["Tables"], self.TABLES_PATH)

    async def initialize_instruments(self, action_arg):
        print("initializing instruments...")
        instruments = action_arg["Instruments"]
        for key in instruments:
            print(key)
            try:
                if issubclass(type(instruments[key]), PylabInstrument):
                    await instruments[key].open()
                    inst_params = await instruments[key].get_parameters("All")

                elif issubclass(type(instruments[key]), PymeasureInstrumentSub):
                    inst_params = instruments[key].quick_properties

                else:
                    inst_params = None
                # Place initial instrument parameters on the tx queue or dictionary for external processing
                if type(self.DataQueueTx) is asyncio.Queue:
                    self.DataQueueTx.put_nowait({key: inst_params})
                elif type(self.DataQueueTx) is dict:
                    self.DataQueueTx[key] = inst_params
            except Exception as e:
                print(e)
                sys.exit()
        print("initialization complete")
