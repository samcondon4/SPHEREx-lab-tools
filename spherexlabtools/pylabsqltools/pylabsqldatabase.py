
import os
import pdb
import pandas as pd
import pymysql
from configparser import ConfigParser

class PylabSQLQuery:
    vint = ['status_byte', 'position']
    vchar6 = ['order_sort_filter', 'shutter', 'series']
    vchar50 = ['exp_id', 'sequence', 'series']
    vbool = ['cs260', 'warm_1', 'warm_2', 'cold_1']
    vdatetime = ['start_time', 'timestamp']
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
                if any(ele in icol for ele in vchar6):
                    sql_command += icol + ' varchar(6), '

                elif any(ele in icol for ele in vchar50):
                    sql_command += icol + ' varchar(50), '

                elif any(ele in icol for ele in vbool):
                    sql_command += icol + ' bool, '

                elif any(ele in icol for ele in vdatetime):
                    sql_command += icol + ' datetime, '

                elif any(ele in icol for ele in vint):
                    sql_command += icol + ' int, '

                elif 'path' in icol:
                    sql_command += icol + ' varchar(120), '

                else:
                    sql_command += icol + ' float, '

            sql_command += 'PRIMARY KEY (exp_id)) ENGINE=InnoDB'

            TABLES[itable] = sql_command