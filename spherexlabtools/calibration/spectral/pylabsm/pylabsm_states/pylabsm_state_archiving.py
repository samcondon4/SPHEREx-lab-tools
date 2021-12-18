"""pylabsm_state_archiving:

    This module implements the archiving state class.

"""

import pdb
import os
from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState
from pylablib.settings import SCHEMA_USER, SCHEMA_NAME, SCHEMA_PSWD

class Archiving(SmCustomState):
    '''SQL Database Tables are connected by the exp_id. '''

    def __init__(self, sm, identifier="archiving", **kwargs):
        super().__init__(sm, self, identifier, **kwargs)

    async def archiving_action(self, action_arg):
        ''' Call write_to_sql_server '''

        #self.write_to_sql_server(action_arg['Archiving'])
        self.write_to_mysql_server(SCHEMA_USER, SCHEMA_PSWD, SCHEMA_NAME, action_arg['Archiving'])

    #def write_to_sql_server(self, archiving_dict):
    #    ''' Pass archiving dictionary to PylabSQLTools function write_to_mysql_server'''
    #    self.write_to_mysql_server(SCHEMA_USER, SCHEMA_PSWD, SCHEMA_NAME, archiving_dict)
