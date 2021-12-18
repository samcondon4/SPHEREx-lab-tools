""" Idea for streamlining sql stuff.
"""
import os
import pdb

import pymysql
from configparser import ConfigParser
#from pylablib.settings import SCHEMA_USER, SCHEMA_NAME, SCHEMA_PSWD, TABLES_PATH

class PylabSQLTools:
    """ This class provides a mechanism for interacting with and storing data on a specified sql server.
    """

    db = None

    def connect_mysql_server(self, SCHEMA_USER, SCHEMA_PSWD, SCHEMA_NAME):
        """ This method opens a connection with the sql server specified at ip.

        :param: ip: ip address of sql server? Don't know if this is the right type of argument to start a connection, but you get the idea.
        :return: None
        """

        self.db = pymysql.connect(user=SCHEMA_USER, password=SCHEMA_PSWD, database=SCHEMA_NAME)

    def close_mysql_server(self):
        """ This method closes the connection with the open sql server.
        :return: None
        """

        self.db.close()

    def write_to_mysql_server(self, SCHEMA_USER, SCHEMA_PSWD, SCHEMA_NAME, archiving_dict):
        """ This method implements a write to the sql server.

        :param: table: sql table to write to.
        :param: key: which column within the table to write to.
        :param: value: data value to write.
        :return: None
        """

        try:
            self.connect_mysql_server(SCHEMA_USER, SCHEMA_PSWD, SCHEMA_NAME)
        except pymysql.InternalError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            pdb.set_trace()

        cursor = self.db.cursor()
        for table_name, exposures_list in archiving_dict.items():
            print("writing to "+table_name)
            for columns_dict in exposures_list:
                sql = self.convert_dict_to_sql_command(table_name, **columns_dict)
                #print(sql)
                try:
                    cursor.execute(sql)
                    self.db.commit()
                    print('success!')
                except pymysql.InternalError as e:
                    print(sql)
                    print('Got error {!r}, errno is {}'.format(e, e.args[0]))
                    # Rollback in case there is any error
                    self.db.rollback()
                    print('Rolling Back')

        self.close_mysql_server()

    def define_sql_tables_and_rows_from_ini(self, dict_out, tables_path):

        config = ConfigParser()
        config.read(tables_path)

        for section in config.sections():
            dict_sect = {}
            for (each_key, each_val) in config.items(section):
                dict_sect[each_key] = each_val

            dict_out[section] = list(dict_sect.keys())  # dict_sect

        return dict_out

    def convert_dict_to_sql_command(self, table, **kwargs):
        """ update/insert rows into objects table (update if the row already exists)
            given the key-value pairs in kwargs """
        keys = ["%s" % k.replace(" ","_") for k in kwargs]
        values = ["'%s'" % v for v in kwargs.values()]
        sql = list()
        sql.append("INSERT INTO %s (" % table)
        sql.append(", ".join(keys))
        sql.append(") VALUES (")
        sql.append(", ".join(values))
        return "".join(sql) + ")"

