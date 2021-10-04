"""pylabsm_state_initializing:

    This module provides the initialization state class.

"""
import asyncio

import pymeasure.instruments.instrument

import pylabinst.pylabinst_instrument_base
from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState


class Initializing(SmCustomState):

    def __init__(self, sm, identifier="initializing", **kwargs):
        super().__init__(sm, self, identifier, **kwargs)

    async def initialize_instruments(self, action_arg):
        try:
            print("initializing instruments...")
            instruments = action_arg["Instruments"]
            for key in instruments:
                if issubclass(type(instruments[key]), pylabinst.pylabinst_instrument_base.Instrument):
                    await instruments[key].open()
                    inst_params = await instruments[key].get_parameters("All")

                elif issubclass(type(instruments[key]), pymeasure.instruments.instrument.Instrument):
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
        print("initialization complete")