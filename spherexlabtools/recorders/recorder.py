import os
import logging
import pymysql
import numpy as np
import pandas as pd
from datetime import datetime

from ..thread import QueueThread
from spherexlabtools.parameters import *

logger = logging.getLogger(__name__)

SCHEMA_NAME = 'spherexlab'
SCHEMA_USER = 'root'
SCHEMA_PSWD = '$PHEREx_B111'


class SltRecorder(QueueThread):
    """ Abstract base-class for SPHERExLabTools specific recorders. This class generates the indices used in the
    :py:class:`pd.DataFrame` objects that are written out to results files with subclasses of this base. The indices
    that are tracked are as follows:

        - "RecordGroup": Used to index procedure sequences. This value is incremented whenever a new procedure sequence
          is set on the "sequence" attribute of the incoming record, or when this same attribute is set
          to None. The latter case corresponds to when the record was generated from within an individual
          procedure and not a procedure sequence.

        - "RecordGroupInd": Used to index a specific procedure within a procedure sequence. This value is incremented on
          every call of :py:meth:`SltRecorder.handle` or is reset to 0 if the "RecordGroup" value was
          just changed.

        - "RecordRow": Only used in the "data" dataframe and is determined by the shape of the incoming record.data

    :ivar record_group: Integer attribute corresponding to the "RecordGroup" index described above.
    :ivar record_group_ind: Integer attribute corresponding to the "RecordGroupInd" index described above.
    :ivar record_row: Integer (or array-like) attribute corresponding to the "RecordRow" index described above.
    :ivar data_index: Pandas index object for the record data.
    :ivar meta_index: Pandas index object for the record procedure and instrument parameters.
    :ivar sequence_index: Pandas index object for the record procedure sequence.
    :cvar _rgroup_str: String name used in dataframes to identify the "RecordGroup" index described above.
    :cvar _rgroupind_str: String name used in dataframes to identify the "RecordGroupInd" index described above.
    :cvar _rrow_str: String name used in dataframes to identify the "RecordRow" index described above.
    """

    _rgroup_str = "RecordGroup"
    _rgroupind_str = "RecordGroupInd"
    _rrow_str = "RecordRow"

    def __init__(self, cfg, exp, **kwargs):
        super().__init__(**kwargs)
        self.name = cfg["instance_name"]
        self.results_path = None
        self.opened_results = None
        self.prev_seq_ts = None
        self.record_row = None
        self.record_group = None
        self.record_group_ind = None
        self.record_group_changed = False
        self.data_index = None
        self.meta_index = None
        self.sequence_index = None

    def handle(self, record):
        """ Update the record_group, record_group_ind, and record_row attributes based on information provided in
            the record.
        """
        if record.recorder_write_path != self.results_path:
            self.results_path = record.recorder_write_path
            self.close_results()
            self.record_group, self.record_group_ind = self.open_results(self.results_path)

        # update record_group #
        self.record_group_changed = False
        if record.sequence["sequence"][0] == "None":
            self.prev_seq_ts = None
            self.record_group += 1
            self.record_group_changed = True
        elif self.prev_seq_ts != record.sequence_timestamp:
            self.prev_seq_ts = record.sequence_timestamp
            self.record_group += 1
            self.record_group_changed = True

        # update record_group_ind #
        if self.record_group_changed:
            self.record_group_ind = 0
        else:
            self.record_group_ind += 1

        # - in the case where the incoming data is a single numeric value, the record_row should be manually set to 1
        # - #
        try:
            self.record_row = record.data.shape[0]
        except AttributeError:
            self.record_row = 1

        # update the pandas index objects #
        self.data_index = pd.MultiIndex.from_product([[self.record_group], [self.record_group_ind],
                                                      np.arange(self.record_row)], names=[self._rgroup_str,
                                                                                          self._rgroupind_str,
                                                                                          self._rrow_str])

        self.meta_index = pd.MultiIndex.from_tuples([(self.record_group, self.record_group_ind)],
                                                    names=[self._rgroup_str, self._rgroupind_str])

        self.sequence_index = pd.Index([self.record_group], name=self._rgroup_str)

        # update the results file with the new indices #
        self.update_results(record)

    def open_results(self, results_path):
        """ Open the results file and return the record_group and record_group_ind. This method must be implemented in
        subclasses and must return those values after opening (or creating) the results file.

        :param results_path: Path to the results.
        :return: Return the initial record_group and record_group_ind for a new file.
        """
        raise NotImplementedError("The open_results() method must be implemented in a subclass!")

    def close_results(self):
        """ Close the currently opened results file. This method must be implemented in subclasses.
        """
        raise NotImplementedError("The close_results() method must be implemented in a subclass!")

    def update_results(self, record):
        """ Update the results file in the format determined by recorder subclasses.
        """
        raise NotImplementedError("The update_results() method must be implemented in a subclass!")


class SQLRecorder(SltRecorder):
    table = None

    def __init__(self, cfg, exp, **kwargs):
        """ Initialize a recorder.
        """
        super().__init__(cfg, exp, **kwargs)

        # Begin by confirming schema exists and creating it if not.
        DB_NAME = SCHEMA_NAME

        cnx = pymysql.connect(user=SCHEMA_USER, password=SCHEMA_PSWD)
        cursor = cnx.cursor()
        try:
            cursor.execute("USE {}".format(DB_NAME))
            print("Database {} exists.".format(DB_NAME))
        except:
            print("Database {} does not exist.".format(DB_NAME))
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME

        # Check that table exists
        table = cfg['params'].get("table", None)
        if table is not None:
            self.table = table

        table_description = "CREATE TABLE  IF NOT EXISTS {0} (" \
                            "exp_id varchar(50)," \
                            " PRIMARY KEY (exp_id)" \
                            ") ENGINE=InnoDB".format(table)

        cursor.execute(table_description)

        cnx.close()

    def connect_mysql(self):
        ''' Connect to server
        '''
        db = pymysql.connect(user=SCHEMA_USER, password=SCHEMA_PSWD, database=SCHEMA_NAME)
        self.db = db
        self.cursor = db.cursor()

    def disconnect_mysql(self):
        ''' Disconnect from server
        '''
        self.cursor.close()

    def add_missing_columns(self, table_name_server, columns_dict):
        ''' Check that columns exist, and add them if they do not.
        '''
        self.connect_mysql()
        self.cursor.execute("DESCRIBE {}".format(table_name_server))
        indexList = self.cursor.fetchall()
        table_dict = {}

        for row in indexList:
            table_dict[row[0]] = row[1]

        for column_name_local in columns_dict:
            if column_name_local not in table_dict:
                add_column_dict = {table_name_server: {column_name_local: columns_dict[column_name_local]}}
                sql_add_column_commands = self.get_add_column_command(add_column_dict)
                for i in sql_add_column_commands:
                    self.cursor.execute(sql_add_column_commands[i])

        self.disconnect_mysql()

    def get_add_column_command(self, mod_dict):
        ''' Return command to add column to table.  Uses the type_lookup table to assign data type to column definition
        '''
        type_lookup = {float: "float", str: "varchar (50)", int: "int", bool: "tinyint",
                       FloatParameter: "float", Parameter: "varchar (50)", IntegerParameter: "int",
                       BooleanParameter: "tinyint"}
        for table_name in mod_dict:
            print('table_name mod is:', table_name)
            alter_statement_columns = {}
            for column_name in mod_dict[table_name]:
                print('column_name mod is:', column_name)
                if 'timestamp' in column_name:
                    type_mod = 'varchar (50)'
                elif 'date' in column_name:
                    type_mod = 'date'
                else:
                    try:
                        type_mod = type_lookup[type(mod_dict[table_name][column_name])]
                    except:
                        logger.error("Add column type conversion still breaking!")
                        type_mod = "float"

                alter_statement = """
                ALTER TABLE {0} 
                ADD {1} {2};
                """.format(table_name, column_name, type_mod)
                # print('alter_statement is', alter_statement)
                alter_statement_columns[column_name] = alter_statement
            return alter_statement_columns

    def upsert(self, table, **kwargs):
        """ Add rows to table given the key-value pairs in kwargs
        """
        keys = ["%s" % k for k in kwargs]
        values = ["'%s'" % v for v in kwargs.values()]
        sql = list()
        sql.append("INSERT INTO %s (" % table)
        sql.append(", ".join(keys))
        sql.append(") VALUES (")
        sql.append(", ".join(values))

        return "".join(sql) + ")"

    def build_sql_table_command(self, ini_dict):
        ''' Return command to add new table(s) to schema
        '''

        for itable, ilist in ini_dict.items():
            sql_command = 'CREATE TABLE ' + itable + ' ('

            for icol in ilist:
                sql_command += icol + " " + ilist[icol] + ", "

            sql_command += 'PRIMARY KEY (exp_id)) ENGINE=InnoDB'

            self.TABLES[itable] = sql_command

    def sql_insert_row_command(self, table_name, commands_dict0):
        '''
        Construct SQL command, e.g.;
        """INSERT INTO spectral_cal
            (exp_id, timestamp, date, sequence, wavelength, grating, order_sort_filter, ndf_position)
            VALUES ('20220420_153633_12','2022-04-20 15:36:33','2022-04-20','sequencename', 5.2, 580 ,'3','1')"""
        and write Table to Database.
        '''

        commands_dict = {key: value for (key, value) in commands_dict0.items() if value is not None}

        return self.upsert(table_name, **commands_dict)

    def execute_sql_statements(self, statement_dict):
        ''' Execute SQL statements by looping through statement_dict
        '''
        for key, statement_text in statement_dict.items():
            if 'add_row' in key:
                try:
                    # Connect to database
                    self.connect_mysql()

                    # Creation of cursor object
                    cursorObject = self.cursor

                    # Execute the SQL statement
                    cursorObject.execute(statement_text)
                    self.db.commit()

                except Exception as e:
                    print("Exeception occured:{}".format(e))
                    self.db.rollback()
                    print('Rolling Back', statement_text)

                finally:
                    # Disconnect from database
                    self.disconnect_mysql()

    def open_results(self, results_path):
        """ Open existing or create new .mat file.
        """
        rec_group = 0
        rec_group_ind = 0

        return rec_group, rec_group_ind

    def close_results(self):
        pass

    def update_results(self, record):
        """ SqlHandle
        """
        print(f"SEQUENCE TIMESTAMP = {record.sequence_timestamp}")
        print(f"PROCEDURE TIMESTAMP = {record.procedure_timestamp}")
        # sql_dict = record.emit_kwargs.get("sql_dict", None)
        table = record.emit_kwargs.get("table", None)
        if table is not None:
            self.table = table

        sql_dict = record.inst_params
        if sql_dict is None:
            sql_dict = {}

        for iproc in record.proc_params:
            if type(record.proc_params[iproc]) == bool:
                if record.proc_params[iproc] == True:
                    sql_dict["_".join(['proc', iproc])] = 1
                if record.proc_params[iproc] == False:
                    sql_dict["_".join(['proc', iproc])] = 0
            else:
                sql_dict["_".join(['proc', iproc])] = record.proc_params[iproc]
            # print('proc is ', "_".join(['proc', iproc]), sql_dict["_".join(['proc', iproc])])

        if 'exp_id' not in sql_dict:
            sql_dict['exp_id'] = "_".join([datetime.now().strftime("%Y%m%d_%H%M%S"), str(self.record_group_ind)])

        if 'storage_path' not in sql_dict:
            sql_dict['storage_path'] = record.recorder_write_path

        # sql_dict['sequence'] = record.sequence
        if record.emit_kwargs.get("keep_recordgroup_info", False):
            sql_dict['RecordGroupNum'] = self.record_group
            sql_dict['RecordGroupInd'] = self.record_group_ind

        # Check for missing columns and add if needed
        self.add_missing_columns(self.table, sql_dict)

        # Execute sql command to add row
        sql_command = self.sql_insert_row_command(self.table, sql_dict)
        sql_command_dict = {'add_row': sql_command}
        self.execute_sql_statements(sql_command_dict)


class CsvRecorder(SltRecorder):
    """ Csv recorder class. This recorder writes out 4 csv files corresponding to the inst_params,
    proc_params, data, and sequence attributes of the records that are placed on the recorder queue.
    """

    _inst_params_appnd = "_inst_params"
    _proc_params_appnd = "_proc_params"
    _data_appnd = "_data"
    _seq_appnd = "_sequence"

    def __init__(self, cfg, exp, **kwargs):
        super().__init__(cfg, exp, **kwargs)

    def open_results(self, results_path):
        """ Try to open all of the csvs for a measurement within the results_path directory. Use the opened_results
            attribute as a flag for if the csvs existed already.
        """
        inst_fn = results_path + self._inst_params_appnd + ".csv"
        proc_fn = results_path + self._proc_params_appnd + ".csv"
        data_fn = results_path + self._data_appnd + ".csv"
        seq_fn = results_path + self._seq_appnd + ".csv"
        try:
            inst_df = pd.read_csv(inst_fn)
            proc_df = pd.read_csv(proc_fn)
            data_df = pd.read_csv(data_fn)
            seq_df = pd.read_csv(seq_fn)
        except FileNotFoundError:
            rec_group = -1
            rec_group_ind = 0
            self.opened_results = False
        else:
            rec_group = proc_df[self._rgroup_str].values[-1]
            rec_group_ind = proc_df[self._rgroupind_str].values[-1]
            self.opened_results = True

        return rec_group, rec_group_ind

    def close_results(self):
        """ Don't need this for the csv recorder.
        """
        pass

    def update_results(self, record):
        """ Write out to the four csv files associated with the record.
        """
        # create a dictionary that maps record attributes to their corresponding dataframes #
        dfs_map = {
            self._inst_params_appnd: [record.inst_params, self.meta_index],
            self._proc_params_appnd: [record.proc_params, self.meta_index],
            self._data_appnd: [record.data, self.data_index],
            self._seq_appnd: [record.sequence, self.sequence_index]
        }
        filtered_dfs_map = {}
        # - remove all components from the above dictionary if they are None - #
        for rec_append, rec_stuff in dfs_map.items():
            if rec_stuff[0] is not None:
                filtered_dfs_map[rec_append] = rec_stuff
        dfs_map = filtered_dfs_map
        for rec_append, rec_stuff in dfs_map.items():
            if type(rec_stuff[0]) is pd.DataFrame:
                dfs_map[rec_append][0] = pd.DataFrame({key: val.values for key, val in rec_stuff[0].items()},
                                                      index=rec_stuff[1])
            else:
                dfs_map[rec_append][0] = pd.DataFrame(rec_stuff[0], index=rec_stuff[1])

        # key-words for to_csv() #
        mode = "a" if self.opened_results else "w"
        hdr = True if not self.opened_results else False
        if hdr:
            self.opened_results = True

        # remove the sequence dataframe from the dictionary since the output will only be updated if the record
        # group changed. #
        seq_df = dfs_map.get(self._seq_appnd, None)
        if seq_df is not None:
            seq_df = dfs_map.pop(self._seq_appnd)
        for key, val in dfs_map.items():
            val[0].to_csv(record.recorder_write_path + key + ".csv", mode=mode, header=hdr, index=True)

        # update the sequence csv only if the record group changed #
        if self.record_group_changed and seq_df is not None:
            seq_df[0].to_csv(record.recorder_write_path + self._seq_appnd + ".csv", mode=mode, header=hdr, index=True)


class PyhkRecorder(QueueThread):
    """ Basic recorder to log data to a .txt file in a Pyhk database.
    """

    _data_dir = "/data/hk"
    _delimiter_map = {
        " ": "%20"
    }
    _separator = "\t"

    def __init__(self, cfg, exp, **kwargs):
        """ Initialize a Pyhk recorder.
        """
        self.name = cfg["instance_name"]
        super().__init__(**kwargs)

    def handle(self, record):
        """ Handle incoming records by appending to the appropriate .txt.
        """
        data = record.data
        ts = record.timestamp

        sens_name = record.__dict__.get("alias", record.name)
        sens_type = record.type
        for c, dc in self._delimiter_map.items():
            sens_name = sens_name.replace(c, dc)

        # convert timestamp to datetime and create the file-path #
        dt = datetime.fromtimestamp(ts)
        dt_str = dt.strftime("%Y:%m:%d")
        dt_str_split = dt_str.split(":")
        fp = os.path.join(self._data_dir, dt_str_split[0], dt_str_split[1], dt_str_split[2], sens_type,
                          sens_name + ".txt")

        # convert data to DataFrame if it is not already that type #
        data = pd.DataFrame(
            {"timestamp": [ts], "data": [data]}
        )

        data.to_csv(fp, mode="a", sep=self._separator, header=False, index=False)


class HDF5Recorder(SltRecorder):
    """ HDF5 recorder utilizing the SltRecorder base class.
    """

    def __init__(self, cfg, exp, **kwargs):
        super().__init__(cfg, exp, **kwargs)

    def open_results(self, results_path):
        """ Open existing or create a new .h5 file.
        """
        fn = results_path + ".h5"
        self.opened_results = pd.HDFStore(fn)
        rec_group = -1
        rec_group_ind = 0
        try:
            rec_group, rec_group_ind = self.opened_results["proc_params"].index[-1]
        except KeyError:
            pass
        return rec_group, rec_group_ind

    def update_results(self, record):
        """ Update the .h5 results file with information from the new record.
        """
        data_df = pd.DataFrame(record.data, index=self.data_index)
        pp_df = pd.DataFrame(record.proc_params, index=self.meta_index)
        ip_df = pd.DataFrame(record.inst_params, index=self.meta_index)
        seq_df = pd.DataFrame(record.sequence, index=self.sequence_index)
        seq_str = seq_df["sequence"].values[0]
        self.opened_results.append("data", data_df)
        self.opened_results.append("proc_params", pp_df)
        self.opened_results.append("inst_params", ip_df)
        try:
            if self.record_group > self.opened_results["sequence"].shape[0]:
                self.opened_results.append("sequence", seq_df, #min_itemsize={"sequence": len(seq_str[0])},
                                           encoding="utf-8")
        except KeyError:
            self.opened_results.append("sequence", seq_df, #min_itemsize={"sequence": len(seq_str[0])},
                                       encoding="utf-8")

    def close_results(self):
        """ Close the .h5 results file.
        """
        if self.opened_results is not None:
            self.opened_results.close()


class HDF5Recorder_Old(QueueThread):
    """ Basic HDF5 recorder class.
    """

    META_GROUP = "Meta"
    GROUP_DELIMITER = "/"
    META_PROC_SEQ_SUBGROUP = f"{META_GROUP}{GROUP_DELIMITER}ProcSeq"
    META_PROC_PARAMS_SUBGROUP = f"{META_GROUP}{GROUP_DELIMITER}ProcParams"
    META_INST_PARAMS_SUBGROUP = f"{META_GROUP}{GROUP_DELIMITER}InstParams"
    DATA_GROUP = "Data"

    def __init__(self, cfg, exp, **kwargs):
        """ Initialize a recorder.
        """
        super().__init__(**kwargs)
        self.filename = cfg["filename"]
        self.exp = exp
        self.store = pd.HDFStore(self.filename)
        # if this is a new hdf file, with no Meta group, add the group #
        if (self.GROUP_DELIMITER + self.META_GROUP) not in self.store.keys():
            meta_series = pd.Series({"Records": 0})
            self.store.put(self.META_GROUP, meta_series)
            self.record_num = 0
        else:
            self.record_num = self.store.get(self.META_GROUP)["Records"]

        # data index within the record #
        self.record_group_ind = 0
        # number of data entries in a record #
        self.record_group_size = 1

    def handle(self, record):
        """ HDF5 recorder handle.
        """
        kwargs = record.emit_kwargs
        # get record group size #
        if "group_records" in kwargs:
            self.record_group_size = kwargs.pop("group_records")

        # append to the Meta group ##################################################################################
        params_index = pd.MultiIndex.from_tuples([(self.record_num, self.record_group_ind)], names=["RecordNum",
                                                                                                    "RecordInd"])
        proc = record.proc
        seq = record.sequence
        proc_params = record.proc_params
        inst_params = record.inst_params
        proc_seq_group_df = pd.DataFrame({
            "Procedure": proc,
            "Sequence": seq,
        }, index=params_index)
        proc_params_group_df = pd.DataFrame(proc_params, index=params_index)
        inst_params_group_df = pd.DataFrame(inst_params, index=params_index)
        self.store.append(self.META_PROC_SEQ_SUBGROUP, proc_seq_group_df)
        self.store.append(self.META_PROC_PARAMS_SUBGROUP, proc_params_group_df)
        self.store.append(self.META_INST_PARAMS_SUBGROUP, inst_params_group_df)

        # append to the Data group ##################################################################################
        data = record.data
        shape = data.shape
        index = pd.MultiIndex.from_product([[self.record_num], [self.record_group_ind], np.arange(shape[0])],
                                           names=["RecordGroupNum", "RecordGroupInd", "Row"])
        data_df = pd.DataFrame(data, index=index)
        self.store.append(self.DATA_GROUP + self.GROUP_DELIMITER + record.name, data_df)

        # update the record index ###################################################################################
        record_complete = False
        if self.record_group_ind < (self.record_group_size - 1):
            self.record_group_ind += 1
        else:
            self.record_group_ind = 0
            record_complete = True

        # update record number #
        if record_complete:
            self.record_num += 1
