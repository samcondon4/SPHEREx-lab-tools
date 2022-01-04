""" This module implements generalized SQL command-building code for querying mySQL database.

        :class:`.PylabSQLQuery`: Top-level container class with code to build and execute SQL queries
"""

import os
import pdb
import pandas as pd
import pymysql
from ..calibration.spectral.pylablib.settings import SCHEMA_USER, SCHEMA_NAME, SCHEMA_PSWD

class PylabSQLQuery:
    """ This module implements generalized SQL command-building code for querying mySQL database.

    """

    def __init__(self):
        self.sql_query = ''''''

    def query_database(self, tables_in, nicknames=None, conditions=None):
        """
        :param tables_in: (list) list of dicts containing desired tables:columns to query, e.g.,
                tables_in = [pylab, cs260, ndf, sr510, sr830]
                where:
                pylab = {'control_software':['timestamp','date','sequence']}
                ndf = {'ndf':['position']}
                cs260 = {'cs260':['wavelength','grating','order_sort_filter','shutter']}
                sr510 = {'sr510':['start_time','sample_rate','time_constant','sensitivity','storage_path']}
                sr830 = {'sr830':['start_time','sample_rate','time_constant','sensitivity','storage_path']}

        :param nicknames: (list) an (optional) short-form prefix for row naming, e.g.;
                nicknames = ["cs", "mono", "ndf", "sr510", "sr830"]

        :param conditions: (dict) an (optional) dictionary of conditions, e.g.,
                conditions = {"where": {"cs": {"timestamp": ">= CURDATE()"}}}

        """
        db = pymysql.connect(user=SCHEMA_USER, password=SCHEMA_PSWD, database=SCHEMA_NAME)

        self.build_sql_query(tables_in, nicknames, conditions)

        dataframe_out = pd.read_sql(self.sql_query, db)
        db.close()

        return dataframe_out

    def build_sql_query(self, tables_in, nicknames=None, conditions=None):
        self.sql_query = ''''''
        if type(tables_in) == list:
            tables_dict = {}
            for itable in tables_in:
                for key, value in itable.items():
                    if key in tables_dict:
                        tables_dict[key].extend(value)
                    else:
                        tables_dict[key] = value
        elif type(tables_in) == dict:
            tables_dict = tables_in
        else:
            print("ERROR!  NEED LIST OR DICT")
            break

        self.sql_query += self.select_tables_string(tables_dict, nickname=nicknames)

        if len(tables_dict) > 1:
            self.sql_query += self.join_tables_string(list(tables_dict.keys()), nickname=nicknames)

        if conditions:
            self.sql_query += self.add_query_conditions(conditions)

    def select_tables_string(self, tables, select_all=False, nickname=None, include_exp_id=True):
        if select_all == True:
            return '''SELECT *
            '''
        else:
            if not nickname:
                nickname = list(tables.keys())
            str_out = '''SELECT '''
            if include_exp_id:
                str_out += '''{}.exp_id, '''.format(nickname[0])
            i = 0
            for key, vals in tables.items():
                for v in vals:
                    str_out += ''' {0}.{1} as {0}_{1},'''.format(nickname[i], v)
                i += 1
            return str_out[:-1]  # Remove last commma

    def join_tables_string(self, table_names, nickname=None):
        if not nickname:
            nickname = table_names
        str_out = ''' 
        FROM {0} {1} '''.format(table_names[0], nickname[0])
        for i in range(len(table_names))[1:]:
            str_out += '''        
            LEFT JOIN {2} AS {3} 
            ON {1}.exp_id = {3}.exp_id '''.format(table_names[i - 1], nickname[i - 1], table_names[i], nickname[i])
        return str_out

    def add_query_conditions(self, conditions_dict):
        str_out = ''' 
        '''
        for key, value in conditions_dict.items():
            str_out += '''{} '''.format(key)
            for table, tval in value.items():
                for cname, cval in tval.items():
                    str_out += '''{}.{} {}'''.format(table, cname, cval)
        return str_out