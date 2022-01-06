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

class PylabSyncSQL:
    """ Synchronize existing mySQL server tables with differences in local file (default sql_tables.ini)."""

    def __init__(self):
        self.TABLES_SERVER = {}
        self.TABLES_LOCAL = {}

    def sync_mysql_server(self, path_ini_file=path_local_ini):

        self.connect_mysql()
        self.TABLES_SERVER = self.describe_existing_schema()
        self.TABLES_LOCAL = self.get_local_ini_dict(path_ini_file)
        updates_dict = self.diff_existing_and_required()
        queries_dict = self.get_alter_queries(updates_dict)
        self.execute_sql_statements(queries_dict)
        pdb.set_trace()

    def connect_mysql(self):
        db = pymysql.connect(user=SCHEMA_USER, password=SCHEMA_PSWD, database=SCHEMA_NAME)
        self.cursor = db.cursor()

    def disconnect_mysql(self):
        self.cursor.close()

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

    def get_local_ini_dict(self, path_ini):

        config = ConfigParser()
        config.read(path_ini)

        TABLES_FORMAT_LOCAL = {}
        for section in config.sections():
            dict_sect = {}
            for (each_key, each_val) in config.items(section):
                dict_sect[each_key] = each_val.replace('"', '')
            TABLES_FORMAT_LOCAL[section] = dict_sect

        return TABLES_FORMAT_LOCAL

    def diff_existing_and_required(self, TABLES_SERVER=None, TABLES_LOCAL=None):
        if not TABLES_SERVER:
            TABLES_SERVER = self.TABLES_SERVER
        if not TABLES_LOCAL:
            TABLES_LOCAL = self.TABLES_LOCAL

        for key_ini in TABLES_LOCAL:
            if key_ini not in TABLES_SERVER:
                print('missing', TABLES_LOCAL[key_ini])
            elif (TABLES_LOCAL[key_ini] == TABLES_SERVER[key_ini]):
                pass
                # print(TABLES_LOCAL[key_ini])
                # print(TABLES_SERVER[key_ini])
            else:
                pass

        missing_tables = {}
        missing_columns = {}
        # different_tables = {}
        different_columns = {}

        for key_ini in TABLES_LOCAL:

            if key_ini not in TABLES_SERVER:
                print('missing table:', key_ini, ' ', TABLES_LOCAL[key_ini])
                missing_tables[key_ini] = TABLES_LOCAL[key_ini]
            else:
                # print(TABLES_FORMAT_LOCAL[key_ini] == TABLES_FORMAT_SERVER[key_ini], key_ini)

                for ifield in TABLES_LOCAL[key_ini]:
                    if ifield in TABLES_SERVER[key_ini]:
                        if (TABLES_LOCAL[key_ini][ifield] == TABLES_SERVER[key_ini][ifield]) or (
                                ('tinyint' in TABLES_SERVER[key_ini][ifield]) & (
                                'bool' in TABLES_LOCAL[key_ini][ifield])):
                            # print(ifield, " no changes")
                            pass
                        else:
                            print(key_ini, ': ', ifield, ": change ", TABLES_SERVER[key_ini][ifield], " to ",
                                  TABLES_LOCAL[key_ini][ifield])
                            if key_ini not in different_columns:
                                different_columns = {key_ini: {}}
                            different_columns[key_ini][ifield] = TABLES_LOCAL[key_ini][ifield]
                    else:
                        print(key_ini, ': ', ifield, " missing column")
                        if key_ini not in missing_columns:
                            missing_columns = {key_ini: {}}
                        missing_columns[key_ini][ifield] = TABLES_LOCAL[key_ini][ifield]

        change_dict = {'add_table': missing_tables, 'add_column': missing_columns, 'change_column': different_columns}
        return change_dict

    def get_alter_queries(self, update_dict):

        output_dict = {}

        for mod_type, mod_dict in update_dict.items():

            alter_statement_columns = {}

            if 'add_table' in mod_type and bool(len(mod_dict)):
                print(mod_type)

                for itable, ilist in mod_dict.items():
                    alter_statement = 'CREATE TABLE ' + itable + ' ('

                    for icol in ilist:
                        alter_statement += icol + " " + ilist[icol] + ", "

                    alter_statement += 'PRIMARY KEY (exp_id)) ENGINE=InnoDB'

                    alter_statement_columns[itable] = alter_statement

            elif 'add_column' in mod_type and bool(len(mod_dict)):
                print(mod_type)
                for table_name in mod_dict:
                    alter_statement_columns = {}
                    for column_name in mod_dict[table_name]:
                        # Alter the student table by adding one more column
                        alter_statement = """
                        ALTER TABLE {0} 
                        ADD {1} {2};
                        """.format(table_name, column_name, mod_dict[table_name][column_name])

                        alter_statement_columns[column_name] = alter_statement

            elif 'change_column' in mod_type and bool(len(mod_dict)):
                # ALTER TABLE `spectral_cal`.`sr510`
                # CHANGE COLUMN `storage_path` `storage_path` VARCHAR(120) NULL DEFAULT NULL ;
                #
                print(mod_type)
                for table_name in mod_dict:
                    alter_statement_columns = {}
                    for column_name in mod_dict[table_name]:
                        alter_statement = """
                        ALTER TABLE {0} 
                        MODIFY COLUMN {1} {1} {2} NULL DEFAULT NULL;
                        """.format(table_name, column_name, mod_dict[table_name][column_name])

                        alter_statement_columns[column_name] = alter_statement

            if bool(len(mod_dict)):
                output_dict[mod_type] = alter_statement_columns
            # pdb.set_trace()

        return output_dict

    def execute_sql_statements(self, change_dict):
        for statement_category, statement_dict in change_dict.items():

            for key, statement_text in statement_dict.items():
                try:

                    self.connect_mysql()
                    # Creation of cursor object
                    cursorObject = self.cursor

                    # Execute the SQL ALTER statement
                    print(statement_text)
                    cursorObject.execute(statement_text)
                    pdb.set_trace()

                except Exception as e:

                    print("Exeception occured:{}".format(e))

                finally:

                    self.disconnect_mysql()

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
