""" Standalone script to synchronize existing mySQL server tables with new changes.

        :class:`.PylabSyncSQL`: Top-level container class with code to compare server and update if
        found to be different.
"""

import sys
import os
import pdb
import pandas as pd
import pymysql
from configparser import ConfigParser
#from calibration.spectral.pylablib.settings import SCHEMA_USER, SCHEMA_NAME, SCHEMA_PSWD
# ImportError: attempted relative import with no known parent package
SCHEMA_NAME = 'spectral_cal'
SCHEMA_USER = 'root'
SCHEMA_PSWD = '$PHEREx_B111'
path_local_ini = os.path.join('..', 'calibration', 'spectral', 'pylablib', 'sql_tables.ini')

def main(path_ini_file=path_local_ini):

    syncSQL = PylabSyncSQL()
    syncSQL.sync_mysql_server(path_ini_file=path_ini_file)
    #syncSQL.connect_mysql()
    #tables_server = syncSQL.describe_existing_schema()
    #tables_local = syncSQL.get_latest_ini_dict(path_ini_file)
    #syncSQL.diff_existing_and_required(tables_server, tables_local)
    #pdb.set_trace()

class PylabSyncSQL:
    """ Synchronize existing mySQL server tables with differences in local file (default sql_tables.ini)."""

    def __init__(self):
        self.TABLES_SERVER = {}
        self.TABLES_LOCAL = {}

    def sync_mysql_server(self, path_ini_file=path_local_ini):

        self.connect_mysql()
        self.TABLES_SERVER = self.describe_existing_schema()
        self.TABLES_LOCAL = self.get_latest_ini_dict(path_ini_file)
        self.diff_existing_and_required()

    def connect_mysql(self):
        db = pymysql.connect(user=SCHEMA_USER, password=SCHEMA_PSWD, database=SCHEMA_NAME)
        self.cursor = db.cursor()

    def describe_existing_schema(self):
        # Get details of database (i.e., bool or float or timestamp, etc.)
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        TABLES_FORMAT = {}
        for i in tables:
            table_name = str(i).split("'")[1::2][0]
            self.cursor.execute("DESCRIBE {}".format(table_name))
            indexList = self.cursor.fetchall()
            table_dict = {}
            for row in indexList:
                table_dict[row[0]] = row[1]
            print(table_dict)
            TABLES_FORMAT[table_name] = table_dict

        return TABLES_FORMAT

    def get_latest_ini_dict(self, path_ini):

        config = ConfigParser()
        config.read(path_ini)

        TABLES_FORMAT_INI = {}
        for section in config.sections():
            dict_sect = {}
            for (each_key, each_val) in config.items(section):
                dict_sect[each_key] = each_val.replace('"', '')
            TABLES_FORMAT_INI[section] = dict_sect

        return TABLES_FORMAT_INI

    def diff_existing_and_required(self, TABLES_SERVER=None, TABLES_INI=None):
        if not TABLES_SERVER:
            TABLES_SERVER = self.TABLES_SERVER
        if not TABLES_INI:
            TABLES_INI = self.TABLES_LOCAL

        for key_ini in TABLES_INI:
            if key_ini not in TABLES_SERVER:
                print('missing', TABLES_INI[key_ini])
            elif (TABLES_INI[key_ini] == TABLES_SERVER[key_ini]):
                pass
                # print(TABLES_INI[key_ini])
                # print(TABLES_SERVER[key_ini])
            else:
                pass

        pdb.set_trace()

    def get_modify_table_command(self):
        ''' Change Table and/or Column Name/Details'''
        pass

    def get_update_table_command(self):
        ''' Change Table and/or Column Entries'''
        pass

if __name__ == "__main__":
    main()
else:
    logging.info("Note: `mapit` module not being run as main executable.")
