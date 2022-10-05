""" This module implements specific recorders that write to databases.
"""

import os
import logging
import pandas as pd
from sqlalchemy.exc import ProgrammingError, OperationalError

import spherexlabtools.log as slt_log
from spherexlabtools.recorders import Recorder

log_name = f"{slt_log.LOGGER_NAME}.{__name__.split('.')[-1]}"
logger = logging.getLogger(log_name)

class SQLRecorder(Recorder):
    """ Writes the merged dataframe to a SQL database.
    """

    _if_exists = "append"

    def __init__(self, cfg, exp, table, engine, type_dict=None, **kwargs):
        """ Initialize the SQL recorder.

        :param cfg: Config dictionary.
        :param exp: Experiment control package.
        :param table: String name of the table to write to.
        :param engine: Object used as the 'engine' argument of all pandas sql calls.
        :param type_dict: Dictionary of SQLAlchemy types for the dataframe columns.
        :param kwargs: Key words for base recorder initialization.
        """
        super().__init__(cfg, exp, extension="", merge=True, **kwargs)
        self.table = table
        self.engine = engine
        self.type_dict = type_dict

    def should_open(self, record):
        """ For now, the table and engine are fixed, so only need to open results once. Thus, we can just
        return (True, True) if self.opened_results is None. Then, use self.opened_results as a flag to indicate
        that we already probed the initial RecordGroup and RecordGroupInd values.

        :param record:
        :return:
        """
        if self.opened_results is None:
            ret = (True, True)
            self.opened_results = True
        else:
            ret = (False, True)

        return ret

    def open_results(self, exists):
        """ Query the RecordGroup and RecordGroupInd columns of the table. If there are no entries in the table,
        then an index error will be thrown, which is caught and rec_group and rec_group_ind are set to -1 accordingly.

        :param exists: Not used here, but need to match call signature of base.
        :return: RecordGroup and RecordGroupInd values as a tuple.
        """
        open_query = "SELECT %s, %s from %s ORDER BY %s DESC, %s DESC LIMIT 1" % (
            self._rgroup_col_str, self._rgroupind_col_str, self.table, self._rgroup_col_str, self._rgroupind_col_str
        )
        try:
            df = pd.read_sql_query(open_query, self.engine)
        except Exception as e:
            logger.error("Error in SQLRecorder open query: %s" % e)
            raise e

        try:
            rec_group = float("".join([c for c in df[self._rgroup_col_str].values[0] if c.isnumeric()]))
            rec_group_ind = float("".join([c for c in df[self._rgroupind_col_str].values[0] if c.isnumeric()]))
        except IndexError:
            rec_group = -1
            rec_group_ind = -1

        return rec_group, rec_group_ind

    def close_results(self):
        """ Close the engine.
        :return:
        """
        self.engine.close()

    def update_results(self):
        """ Write the merged dataframe to the database.
        :return:
        """
        self.merged_df.to_sql(self.table, self.engine, dtype=self.type_dict, if_exists=self._if_exists)
