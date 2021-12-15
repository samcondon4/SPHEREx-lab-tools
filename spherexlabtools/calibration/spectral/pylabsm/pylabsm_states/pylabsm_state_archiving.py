"""pylabsm_state_archiving:

    This module implements the archiving state class.

"""

import os
from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState
from pylablib.settings import SCHEMA_USER, SCHEMA_NAME, SCHEMA_PSWD, TABLES_PATH

class Archiving(SmCustomState):
    '''SQL Database Tables are connected by the exp_id. '''

    TABLES_PATH = os.path.join("..","..","pylablib","sql_tables.ini")

    def __init__(self, sm, identifier="archiving", **kwargs):
        super().__init__(sm, self, identifier, **kwargs)

        self.tables_dict = self.define_sql_tables_and_rows_from_ini(TABLES_PATH)

    async def archiving_action(self, action_arg):
        ''' Call write to server, which loops through action_arg["Archiving"] '''

        self.write_to_sql_server(action_arg)

    def write_to_sql_server(self, action_arg):
        action_dict = action_arg['Archiving']

        self.connect_mysql_server(SCHEMA_USER, SCHEMA_PSWD, SCHEMA_NAME)

        for table_name, exposures_list in action_dict.items():
            for columns_dict in exposures_list:
                self.write_to_mysql_server(table_name, columns_dict)

        self.close_mysql_server()



