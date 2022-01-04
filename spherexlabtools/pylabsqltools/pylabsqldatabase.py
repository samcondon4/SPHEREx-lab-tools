""" This module implements generalized SQL command-building code for querying mySQL database.

        :class:`.PylabSQLDabase`: Top-level container class with code to build and execute SQL queries
"""

import os
import pdb
import pandas as pd
import pymysql
from configparser import ConfigParser

class PylabSQLDabase:

    def __init__(self):
        self.TABLES = {}

    def get_ini_dict(self, path_ini='..\\calibration\\spectral\\pylablib\\sql_tables.ini'):

        config = ConfigParser()
        config.read(path_ini)

        dict_out = {}
        for section in config.sections():
            dict_sect = {}
            for (each_key, each_val) in config.items(section):
                dict_sect[each_key] = each_val

            dict_out[section] = list(dict_sect.keys())  # dict_sect

        return dict_out

    def build_sql_command(self, ini_dict):

        for itable, ilist in ini_dict.items():
            sql_command = 'CREATE TABLE ' + itable + ' ('

            for icol in ilist:
                sql_command += icol + " " + ilist[icol] + ", "

            sql_command += 'PRIMARY KEY (exp_id)) ENGINE=InnoDB'

            self.TABLES[itable] = sql_command