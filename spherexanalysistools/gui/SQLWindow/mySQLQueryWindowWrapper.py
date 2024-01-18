import pdb
import os
import sshtunnel
from sshtunnel import SSHTunnelForwarder
import numpy as np
import pandas as pd
import logging
import paramiko
import pysftp
import pymysql
import json
from pathlib import Path
from datetime import datetime, timedelta
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from .mySQLQueryWindow import Ui_MainWindow
from .sql_query_scripts import sql_query_commands_dict

SCHEMA_NAME = 'spherexlab'
SCHEMA_USER = 'root'
SCHEMA_PSWD = '$PHEREx_B111'

detector_sn = {'0':'18831'}
# timestamp_or_datetime = 'TIMESTAMP'
timestamp_or_datetime = 'DATETIME'

class SQLQueryWindow(Ui_MainWindow):

    scripted_queries = {}
    query_dict = {"SELECT": "",
                  "FROM": "",
                  "INNER JOIN": "",
                  "WHERE": "",
                  "GROUP BY": "",
                  "ORDER BY": ""
                  }
    download_dict = {'FRAME_DATA': {},
                     'LAB_OUTPUT': {},
                     'RAW_DATA': {}}

    detector_dict = {}
    engineering_detectors = ['ID00_18831', 'ID0_XXXXX', 'ID08_22145', 'ID09-21708']
    flight_detectors = ['ID01-XXXXX', 'ID02-XXXXX', 'ID03-XXXXX', 'ID04-XXXXX', 'ID05-XXXXX', 'ID06-XXXXX']

    def __init__(self):
        #super(SQLQueryWindow, self).__init__(self)
        super().__init__()
        self.mainwindow = QtWidgets.QMainWindow()
        self.setupUi(self.mainwindow)

        self._server = {}
        self.updateServer()
        self.comboBox_Server_Location.currentIndexChanged.connect(self.updateServer)
        self.populateSchemaNameComboBox()
        self.populateTableNameComboBox()
        self.loadAllQueryText()
        self.updateDownloadDict()
        self.selectDetectors()
        self.readCannedQueries()

        self.dataFrame = pd.DataFrame()
        self.getTableColumnNames()
        self.saved_query = self.textEdit_SQL_Query.toPlainText()
        self.last_query = self.textEdit_SQL_Query.toPlainText()

        self.dateTimeEdit_start.setDateTime(datetime.now()-timedelta(hours=1))
        self.dateTimeEdit_end.setDateTime(datetime.now())

        self.button_RunQuery.clicked.connect(self.loadDataBase)
        self.button_SaveQuery.clicked.connect(self.saveQueryText)
        #self.button_LoadQuery.clicked.connect(self.loadQueryText)
        self.button_ClearQuery.clicked.connect(self.clearQueryText)
        self.button_ClearTable.clicked.connect(self.clearTable)

        self.button_Import_All.clicked.connect(self.loadAllQueryText)
        self.button_Import_Last_Hour.clicked.connect(self.loadLastHourQueryText)
        self.button_Import_Last_Day.clicked.connect(self.loadLastDayQueryText)
        #self.button_Import_Last_Query.clicked.connect(self.loadLastQueryText)
        self.button_Import_Between.clicked.connect(self.loadBetweenDateTime)
        self.button_Import_Wavelengths.clicked.connect(self.loadBetweenWavelengths)
        self.button_Include_Lockin.clicked.connect(self.addLockin)
        self.button_Include_Blue.clicked.connect(self.addBlue)
        self.button_Include_Green.clicked.connect(self.addGreen)

        self.button_LoadCSV.clicked.connect(self.loadCSV)
        self.button_ExportCSV.clicked.connect(self.exportCSV)
        self.button_DownloadData.clicked.connect(self.downloadData)

        # Add columns to query statement by doubleclicking
        self.listView_table.doubleClicked.connect(self.clickColumn)

        # If files to download change update download dict.
        self.checkBox_PIX_all_frames.stateChanged.connect(self.updateDownloadDict)
        self.checkBox_include_frame_data_RST.stateChanged.connect(self.updateDownloadDict)
        self.checkBox_include_frame_data_SUR.stateChanged.connect(self.updateDownloadDict)
        self.checkBox_lab_output_unCorr.stateChanged.connect(self.updateDownloadDict)
        self.checkBox_lab_output_phantom.stateChanged.connect(self.updateDownloadDict)
        self.checkBox_lab_output_refCorr.stateChanged.connect(self.updateDownloadDict)
        self.checkBox_lab_output_phanCorr.stateChanged.connect(self.updateDownloadDict)
        self.spinBox_PIX_frames_lo.valueChanged.connect(self.updateDownloadDict)
        self.spinBox_PIX_frames_hi.valueChanged.connect(self.updateDownloadDict)

        # Update lists when combobox changes
        self.comboBox_Server_Location.currentIndexChanged.connect(self.populateSchemaNameComboBox)
        self.comboBox_Server_Location.currentIndexChanged.connect(self.populateTableNameComboBox)
        self.comboBox_Server_Location.currentIndexChanged.connect(self.getTableColumnNames)
        self.comboBox_database_name.currentIndexChanged.connect(self.populateTableNameComboBox)
        self.comboBox_database_name.currentIndexChanged.connect(self.getTableColumnNames)
        self.comboBox_table_name.currentIndexChanged.connect(self.getTableColumnNames)
        #self.comboBox_table_name.currentIndexChanged.connect(self.loadAllQueryText)
        self.comboBox_scriptedQueries.currentIndexChanged.connect(self.updateCannedQuery)

        # Update detector selection query
        self.checkBox_0.stateChanged.connect(self.selectDetectors)
        self.checkBox_1.stateChanged.connect(self.selectDetectors)
        self.checkBox_2.stateChanged.connect(self.selectDetectors)
        self.checkBox_3.stateChanged.connect(self.selectDetectors)
        self.checkBox_4.stateChanged.connect(self.selectDetectors)
        self.checkBox_5.stateChanged.connect(self.selectDetectors)
        self.checkBox_6.stateChanged.connect(self.selectDetectors)
        self.checkBox_7.stateChanged.connect(self.selectDetectors)
        self.checkBox_8.stateChanged.connect(self.selectDetectors)
        self.checkBox_9.stateChanged.connect(self.selectDetectors)
        self.checkBox_all_eng.stateChanged.connect(self.selectBulkDetectors)
        self.checkBox_all_flight.stateChanged.connect(self.selectBulkDetectors)


    def updateServer(self):

        comboBoxTextIn = self.comboBox_Server_Location.currentText()
        if 'local' in comboBoxTextIn:
            print('using local')
            ssh_host = None
            ssh_username = None
            ssh_password = None
            database_username = 'root'
            database_password = '$PHEREx_B111'
            database_name = 'spherex_lab'
            localhost = '127.0.0.1'

        elif 'green' in comboBoxTextIn:
            print('using green')
            ssh_host = 'green.pyhk.net'
            ssh_username = 'spherex-green'
            ssh_password = 'spherex_lab'
            database_username = 'root'
            database_password = '$PHEREx_B111'
            database_name = 'spherex_lab'
            localhost = '127.0.0.1'

        elif 'ragnarok' in comboBoxTextIn:
            print('using ragnarok')
            ssh_host = 'ragnarok.caltech.edu'
            ssh_username = 'spherex_lab'
            ssh_password = 'r@gP4$ph!'
            database_username = 'root'
            database_password = '$PHEREx_B111'
            database_name = 'spherexlab'
            localhost = '127.0.0.1'

        ret = {'ssh_host': ssh_host, 'ssh_username': ssh_username, 'ssh_password': ssh_password,
               'database_username': database_username, 'database_password': database_password,
               'database_name': database_name, 'localhost': localhost}

        self._server = ret

    def open_ssh_tunnel(self, verbose=False):
        """Open an SSH tunnel and connect using a username and password.

        :param verbose: Set to True to show logging
        :return tunnel: Global SSH tunnel connection
        """

        if verbose:
            sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG

        global tunnel
        tunnel = SSHTunnelForwarder(
            (self._server['ssh_host'], 22),
            ssh_username=self._server['ssh_username'],
            ssh_password=self._server['ssh_password'],
            remote_bind_address=('127.0.0.1', 3306)
        )

        tunnel.start()

    def mysql_connect(self, db_name=None):
        """Connect to a MySQL server using the SSH tunnel connection

        :return connection: Global MySQL database connection
        """
        if db_name is None:
            db_name = self._server['database_name']
        global connection
        connection = pymysql.connect(
            host='127.0.0.1',
            user=self._server['database_username'],
            passwd=self._server['database_password'],
            db=db_name,
            port=tunnel.local_bind_port
        )
        self._cursor = connection.cursor()

    def read_query(self, sql):
        """Runs a given SQL query via the global database connection.

        :param sql: MySQL query
        :return: Pandas dataframe containing results
        """
        return pd.read_sql_query(sql, connection)

    def mysql_disconnect(self):
        """Closes the MySQL database connection.
        """
        connection.close()

    def close_ssh_tunnel(self):
        """Closes the SSH tunnel connection.
        """
        tunnel.close()

    def populateSchemaNameComboBox(self):
        schemaName_sc = 'spherexlab'

        self.comboBox_database_name.blockSignals(True)
        self.comboBox_database_name.clear()
        schemaNames = self.getSchemaNames()
        # Put schemaName_sc at top of list
        if schemaName_sc in schemaNames:
            idx_sc = schemaNames.index(schemaName_sc)
            schemaNames.pop(idx_sc)
            schemaNames = [schemaName_sc]+schemaNames
        self.comboBox_database_name.addItems(schemaNames)
        self.comboBox_database_name.blockSignals(False)

    def populateTableNameComboBox(self):
        tableName_sc = 'spectral_cal'

        self.comboBox_table_name.blockSignals(True)
        self.comboBox_table_name.clear()
        tableNames = self.getTableNames()
        # Put tableName_sc at top of list
        if tableName_sc in tableNames:
            idx_sc = tableNames.index(tableName_sc)
            tableNames.pop(idx_sc)
            tableNames = [tableName_sc]+tableNames
        self.comboBox_table_name.addItems(tableNames)
        self.comboBox_table_name.blockSignals(False)

    def getSchemaNames(self):
        sql_statement = """ select schema_name as database_name
        from information_schema.schemata
        order by schema_name;
        """
        exclude = ['information_schema', 'mysql', 'performance_schema', 'sys']
        if 'local' in self.comboBox_Server_Location.currentText():

            db = pymysql.connect(user=SCHEMA_USER, password=SCHEMA_PSWD)
            self.cursor = db.cursor()
            self.cursor.execute(sql_statement)

            indexList = self.cursor.fetchall()
            schemaNames = [i[0] for i in indexList]

            self.cursor.close()
            for ex in exclude:
                if ex in schemaNames: schemaNames.remove(ex)
            print("New Schema Names ", schemaNames)
            return schemaNames

        else:

            self.open_ssh_tunnel()
            self.mysql_connect()

            self._cursor.execute(sql_statement)
            indexList = self._cursor.fetchall()
            schemaNames = [i[0] for i in indexList]

            self.mysql_disconnect()
            self.close_ssh_tunnel()
            for ex in exclude:
                if ex in schemaNames: schemaNames.remove(ex)
            print("New Schema Names ",schemaNames)
            return schemaNames

    def getTableNames(self):
        DB_NAME = self.comboBox_database_name.currentText()
        sql_statement = '''
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = "{}";'''.format(DB_NAME)

        if 'local' in self.comboBox_Server_Location.currentText():

            db = pymysql.connect(user=SCHEMA_USER, password=SCHEMA_PSWD, database=DB_NAME)
            self.cursor = db.cursor()

            try:
                self.cursor.execute(sql_statement)
                indexList = self.cursor.fetchall()
                tableNames = [i[0] for i in indexList]
                print("New Table Names ", tableNames)
            except:
                tableNames = []

            self.cursor.close()
            return tableNames

        else:

            self.open_ssh_tunnel()
            self.mysql_connect()

            try:
                self._cursor.execute(sql_statement)
                indexList = self._cursor.fetchall()
                tableNames = [i[0] for i in indexList]
                print("New Table Names ", tableNames)
            except:
                tableNames = []

            self.mysql_disconnect()
            self.close_ssh_tunnel()
            return tableNames

    def getTableColumnNames(self):

        if 'local' in self.comboBox_Server_Location.currentText():
            DB_NAME = self.comboBox_database_name.currentText()
            TABLE_NAME = self.comboBox_table_name.currentText()

            db = pymysql.connect(user=SCHEMA_USER, password=SCHEMA_PSWD, database=DB_NAME)
            self.cursor = db.cursor()

            try:
                self.cursor.execute("DESCRIBE {}".format(TABLE_NAME))
                indexList = self.cursor.fetchall()
                columnNames = [i[0] for i in indexList]
            except:
                columnNames = []

            self.cursor.close()

            self.df_cols = pd.DataFrame(columnNames)
            self.cols_model = TableModel(self.df_cols)
            self.listView_table.setModel(self.cols_model)

            return columnNames

        else:
            DB_NAME = self.comboBox_database_name.currentText()
            TABLE_NAME = self.comboBox_table_name.currentText()

            self.open_ssh_tunnel()
            self.mysql_connect(db_name=DB_NAME)

            try:
                self._cursor.execute("DESCRIBE {}".format(TABLE_NAME))
                indexList = self._cursor.fetchall()
                columnNames = [i[0] for i in indexList]
            except:
                columnNames = []

            self.mysql_disconnect()
            self.close_ssh_tunnel()

            self.df_cols = pd.DataFrame(columnNames)
            self.cols_model = TableModel(self.df_cols)
            self.listView_table.setModel(self.cols_model)

            return columnNames

    def readCannedQueries(self):

        self.scripted_queries = sql_query_commands_dict
        for d_key in sql_query_commands_dict:
            self.comboBox_scriptedQueries.addItem(d_key)

    def updateCannedQuery(self):

        d_key = self.comboBox_scriptedQueries.currentText()
        d_txt = self.scripted_queries[d_key]
        self.clearQueryText()
        self.textEdit_SQL_Query.setText(d_txt)

    def clearTable(self):
        ''' By setting setModel(None) the table is cleared.
        '''

        self.tableView_SQL_Results.setModel(None)

    def loadDataBase(self):

        if self.comboBox_database_name.currentText().lower() == SCHEMA_NAME:
            DB_NAME = SCHEMA_NAME
        else:
            DB_NAME = self.comboBox_database_name.currentText()
        if 'local' in self.comboBox_Server_Location.currentText():
            #columnNames = self.getTableColumnNames()

            db = pymysql.connect(user=SCHEMA_USER, password=SCHEMA_PSWD, database=DB_NAME)
            self.cursor = db.cursor()

            self.populateQueryDict()
            query = self.assembleQueryDict()
            self.textEdit_SQL_Query.setText(query)
            #print(query)

            self.last_query = query
            self.cursor.execute(query)
            cursor = self.cursor.fetchall()

            if len(cursor):
                table_header = [i[0] for i in self.cursor.description]
                self.dataFrame = pd.DataFrame(cursor, columns=table_header)
                self.model = TableModel(self.dataFrame)
                self.tableView_SQL_Results.setModel(self.model)
            else:
                print('No Data in Selection!')

            self.cursor.close()
        else:
            # SSH Tunnel into Remote Server
            self.open_ssh_tunnel()
            self.mysql_connect(db_name=DB_NAME)
            self.populateQueryDict()
            query = self.assembleQueryDict()
            self.textEdit_SQL_Query.setText(query)
            #print(query)
            self.last_query = query
            try:
                self._cursor.execute(query)
                cursor = self._cursor.fetchall()

                if len(cursor):
                    table_header = [i[0] for i in self._cursor.description]
                    self.dataFrame = pd.DataFrame(cursor, columns=table_header)
                    self.model = TableModel(self.dataFrame)
                    self.tableView_SQL_Results.setModel(self.model)
                else:
                    print('No Data in Selection!')
            except Exception as e:
                print(e)

            finally:
                self.mysql_disconnect()
                self.close_ssh_tunnel()

    def clickColumn(self, signalIn):

        self.editQueryBox(signalIn.data())

    def editQueryBox(self, input):

        query = self.textEdit_SQL_Query.toPlainText().lower()
        if 'select' not in query:
            query = ' '.join(['select', query])
        if input in query:
            query_out = query
        elif '*' in query:
            query_out = query.replace('*', input)
        else:
            query_out = '''select {}, {}'''.format(input, query.split('select')[1])

        self.textEdit_SQL_Query.setText(query_out)

    def updateBulkDetectorDict(self):

        setChecked_flight=0
        setChecked_eng=0
        self.detector_dict['flight'] = self.checkBox_all_flight.checkState()
        self.detector_dict['engineering'] = self.checkBox_all_eng.checkState()
        if self.detector_dict['flight']:
            setChecked_flight=2
        if self.detector_dict['engineering']:
            setChecked_eng = 2

        #for idflight in self.flight_detectors:
        #    self.detector_dict[idflight] = self.checkBox_1.setChecked(setChecked_flight)
        #for ideng in self.engineering_detectors:
        #    self.detector_dict[ideng] = self.checkBox_1.setChecked(setChecked_eng)
        self.detector_dict['ID01-XXXXX'] = self.checkBox_1.setChecked(setChecked_flight)
        self.detector_dict['ID02-XXXXX'] = self.checkBox_2.setChecked(setChecked_flight)
        self.detector_dict['ID03-XXXXX'] = self.checkBox_3.setChecked(setChecked_flight)
        self.detector_dict['ID04-XXXXX'] = self.checkBox_4.setChecked(setChecked_flight)
        self.detector_dict['ID05-XXXXX'] = self.checkBox_5.setChecked(setChecked_flight)
        self.detector_dict['ID06-XXXXX'] = self.checkBox_6.setChecked(setChecked_flight)
        self.detector_dict['ID00_18831'] = self.checkBox_0.setChecked(setChecked_eng)
        self.detector_dict['ID07-XXXXX'] = self.checkBox_7.setChecked(setChecked_eng)
        self.detector_dict['ID08_22145'] = self.checkBox_8.setChecked(setChecked_eng)
        self.detector_dict['ID09-21708'] = self.checkBox_9.setChecked(setChecked_eng)

    def updateDetectorDict(self):

        self.detector_dict['flight'] = self.checkBox_all_flight.checkState()
        self.detector_dict['engineering'] = self.checkBox_all_eng.checkState()
        self.detector_dict['ID00_18831'] = self.checkBox_0.checkState()
        self.detector_dict['ID01-XXXXX'] = self.checkBox_1.checkState()
        self.detector_dict['ID02-XXXXX'] = self.checkBox_2.checkState()
        self.detector_dict['ID03-XXXXX'] = self.checkBox_3.checkState()
        self.detector_dict['ID04-XXXXX'] = self.checkBox_4.checkState()
        self.detector_dict['ID05-XXXXX'] = self.checkBox_5.checkState()
        self.detector_dict['ID06-XXXXX'] = self.checkBox_6.checkState()
        self.detector_dict['ID07-XXXXX'] = self.checkBox_7.checkState()
        self.detector_dict['ID08_22145'] = self.checkBox_8.checkState()
        self.detector_dict['ID09-21708'] = self.checkBox_9.checkState()

    def selectBulkDetectors(self):
        self.updateBulkDetectorDict()
        self.selectDetectors()

    def selectDetectors(self):

        self.updateDetectorDict()
        live_detectors = []
        if self.detector_dict['flight'] and self.detector_dict['engineering']:
            pass
        else:
            if self.detector_dict['flight']:
                live_detectors = self.flight_detectors
            elif self.detector_dict['engineering']:
                live_detectors = self.engineering_detectors
            else:
                live_detectors = [i for i in self.detector_dict if self.detector_dict[i]]
        detector_list = ' OR '.join(["FILEID='"+i+"'" for i in live_detectors])#+'\n'

        self.populateQueryDict()
        query_in = self.assembleQueryDict()

        if 'where' in query_in.lower():
            where_query = self.query_dict['WHERE']
            if 'and' in where_query:
                and_list = where_query.lower().split('and')
                and_list.append(detector_list)
            else:
                and_list = [detector_list]
            self.query_dict['WHERE'] = ' AND '.join(and_list)
        else:
            self.query_dict['WHERE'] = detector_list
        if 'order by' not in query_in:
            self.query_dict['ORDER BY'] = "{} DESC".format(timestamp_or_datetime)
        query_final = self.assembleQueryDict()
        self.textEdit_SQL_Query.setText(query_final)

    def updateDownloadDict(self):
        print('changing downloaded files')

        self.download_dict['FRAME_DATA'] = {}
        self.download_dict['FRAME_DATA']['RST'] = self.checkBox_include_frame_data_RST.checkState()
        self.download_dict['FRAME_DATA']['SUR'] = self.checkBox_include_frame_data_SUR.checkState()
        self.download_dict['FRAME_DATA']['PIX'] = {}
        self.download_dict['FRAME_DATA']['PIX']['ANY'] = False
        self.download_dict['FRAME_DATA']['PIX']['ALL'] = self.checkBox_PIX_all_frames.checkState()
        self.download_dict['FRAME_DATA']['PIX']['RANGE'] = [self.spinBox_PIX_frames_lo.value(),
                                                            self.spinBox_PIX_frames_hi.value()]
        # SET ANY to True if ALL is checked or range difference is non-zero
        if self.download_dict['FRAME_DATA']['PIX']['ALL'] or np.diff(self.download_dict['FRAME_DATA']['PIX']['RANGE']):
            self.download_dict['FRAME_DATA']['PIX']['ANY'] = True

        self.download_dict['LAB_OUTPUT'] = {}
        self.download_dict['LAB_OUTPUT']['unCorr'] = self.checkBox_lab_output_unCorr.checkState()
        self.download_dict['LAB_OUTPUT']['phantom'] = self.checkBox_lab_output_phantom.checkState()
        self.download_dict['LAB_OUTPUT']['refCorr'] = self.checkBox_lab_output_refCorr.checkState()
        self.download_dict['LAB_OUTPUT']['phanCorr'] = self.checkBox_lab_output_phanCorr.checkState()

    def prepareDownload(self):
        ''' Make a list of files to download from ragnarok given GUI settings
        sql_rows = [exp_id,ndf_position,mono_shutter,mono_osf,mono_grating,mono_wavelength,
                    lockin_sr510_time_constant,lockin_sr830_time_constant,lockin_sr510_sensitivity,
                    lockin_sr830_sensitivity,detid,detsn,start,exposure,comment,
                    nofits,donesig,
                    fileid,timestamp,filename,
                    dio,fits,lockin_mod_mean,lockin_mod_std,
                    lockin_samples,proc_exposure_comment,proc_exposure_time,proc_generate_fits,
                    proc_lockin_sample_rate,proc_lockin_sr510_sensitivity,proc_lockin_sr510_time_constant,
                    proc_lockin_sr830_sensitivity,proc_lockin_sr830_time_constant,proc_log_lockin,
                    proc_mono_grating,proc_mono_osf,proc_mono_shutter,proc_mono_wavelength,proc_ndf_position,
                    storage_path]
        '''
        # example_frames_path = "/H2RG-tests/FRAME_DATA/fileid/timestamp/filename"
        # example_frames_path = "/H2RG-tests/FRAME_DATA/ID00_18831/20220722/SPX_ID00_18831_20220722_181710"
        # example_lab_output_path = /H2RG-tests/LAB_OUTPUT/ID00_18831/phanCorr
        base_path = "/H2RG-tests/"
        base_lab_output = ["unCorr", "phanCorr", "refCorr", "phantom"]
        lab_output_names = {}
        for ilab in base_lab_output:
            lab_output_names[ilab] = []
        frame_names = []
        downloads_list = []
        if not len(self.dataFrame):
            print('NO DATA TO DOWNLOAD')
            return None

        fileids = self.dataFrame['fileid']
        for fileid in np.unique(fileids):
            idx = self.dataFrame.index[self.dataFrame['fileid'] == fileid].tolist()
            timestamps = self.dataFrame['timestamp'].iloc[idx]
            lab_output_path = os.path.join(base_path, "LAB_OUTPUT", fileid)

            # LAB VALUES
            self.open_sftp_connection()
            try:
                for ilab in base_lab_output:
                    lab_output_names[ilab].extend(
                        sftp_client.listdir(Path(os.path.join(lab_output_path, ilab)).as_posix()))
            except Exception as e:
                print(e)

            # FRAMES
            if self.download_dict['FRAME_DATA']['RST'] + self.download_dict['FRAME_DATA']['SUR']+self.download_dict['FRAME_DATA']['PIX']['ANY']:
                for timestamp in timestamps:
                    print(timestamp)
                    dirname = "_".join(["SPX", fileid, timestamp])
                    frames_path = os.path.join(base_path, "FRAME_DATA", fileid, timestamp.split('_')[0], dirname)

                    try:
                        frame_names.extend(sftp_client.listdir(Path(frames_path).as_posix()))
                    except Exception as e:
                        print(e)

            self.close_sftp_connection()

            ## GET LIST OF DOWNLOADS
            # FRAMES
            for i in self.download_dict['FRAME_DATA']:
                files_list = [Path(os.path.join(frames_path, s)).as_posix() for s in frame_names if i in s]
                if len(files_list):
                    if i in ['RST', 'SUR']:
                        if self.download_dict['FRAME_DATA'][i]:
                            downloads_list.extend(files_list)
                    elif self.download_dict['FRAME_DATA'][i]['ANY']:
                        if self.download_dict['FRAME_DATA'][i]['ALL']:
                            downloads_list.extend(files_list)
                        else:
                            lo = self.download_dict['FRAME_DATA'][i]['RANGE'][0]
                            hi = self.download_dict['FRAME_DATA'][i]['RANGE'][1]
                            for ipix in np.arange(lo,hi):
                                iname = "_".join([dirname, 'PIX', str(ipix).zfill(4)])+'.FITS'
                                if iname in files_list:
                                    downloads_list.append(iname)
            # LAB OUTPUT
            for ilab in lab_output_names:
                # Only if boxes are checked
                if self.download_dict['LAB_OUTPUT'][ilab]:
                    for timestamp in timestamps:
                        ilab_files = [Path(os.path.join(lab_output_path, ilab, s)).as_posix() for s in lab_output_names[ilab] if timestamp in s]
                        downloads_list.extend(ilab_files)

        #pdb.set_trace()
        return downloads_list

    def downloadData(self):
        try:
            downloads_list = self.prepareDownload()
        except Exception as e:
            print(e)

        Hostname = "skellig.caltech.edu"
        Username = "eng"
        Password = os.environ['SKELLIG_PWD']

        # Get path to download data from GUI
        export_path = self.lineEdit_ExportFITS.text()
        #export_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        #export_path = os.path.join(export_basepath, export_timestamp)
        if not os.path.exists(export_path):
            os.makedirs(export_path)

        if downloads_list is not None:
            try:
                with pysftp.Connection(host=Hostname, username=Username, password=Password) as sftp:
                    print("Connection successfully established ... ")

                    for i, ipath in enumerate(downloads_list):
                        if not os.path.isfile(Path(os.path.join(export_path, os.path.basename(ipath))).as_posix()):
                            print('downloading {}'.format(ipath))
                            sftp.get(ipath, Path(os.path.join(export_path, os.path.basename(ipath))).as_posix())
                        else:
                            print("{} Exists!".format(os.path.basename(ipath)))
            except Exception as e:
                print(e)
            finally:
                print("FIND DOWNLOADED FILES IN {}".format(export_path))
                sftp.close()
        else:
            print("NO FILES TO DOWNLOAD")

    def open_sftp_connection(self):
        Hostname = "skellig.caltech.edu"
        Username = "eng"
        Password = os.environ['SKELLIG_PWD']  # "$PHEREx_2024!"

        global sftp_client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=Hostname,
                           username=Username,
                           password=Password)
        sftp_client = ssh_client.open_sftp()

    def close_sftp_connection(self):
        sftp_client.close()

    def exportCSV(self):
        df = self.dataFrame
        if len(df):
            export_basepath_list = self.lineEdit_ExportCSV.text().split('.csv')
            export_basepath = export_basepath_list[0]
            if len(export_basepath_list) == 1:
                if not os.path.isdir(export_basepath):
                    os.makedirs(export_basepath)
                export_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                df.to_csv(os.path.join(os.path.dirname(export_basepath), "sql_export_"+export_timestamp+".csv"))
            else:
                while os.path.isfile(export_basepath+".csv"):
                    export_basepath += '_'
                pdb.set_trace()
                print("Exporting {}".format(export_basepath+".csv"))
                df.to_csv(export_basepath+".csv")
        else:
            print("Nothing to export!")

    def loadCSV(self):

        import_basepath = self.lineEdit_ExportCSV.text()
        if os.path.isfile(import_basepath):
            self.dataFrame = pd.read_csv(import_basepath)
            self.model = TableModel(self.dataFrame)
            self.tableView_SQL_Results.setModel(self.model)
        else:
            print("File {} does not exist".format(import_basepath))

    def assembleQueryDict(self):
        for key in self.query_dict:
            self.query_dict[key] = self.query_dict[key].replace('\n', '')
        query_final = '\n'.join([' '.join([i, self.query_dict[i]]) for i in self.query_dict if self.query_dict[i] != ""])
        query_final = query_final.replace('hours', 'hour').replace('days', 'day').replace('  ', ' ').replace('   ', ' ').replace('    ', ' ')
        print(query_final)
        return query_final

    def populateQueryDict(self):

        query_in = self.textEdit_SQL_Query.toPlainText().lower()
        self.query_dict['SELECT'] = query_in.split('select')[1].split('from')[0]
        self.query_dict['FROM'] = \
        query_in.split('from')[1].split('inner')[0].split('join')[0].split('where')[0].split('group by')[0].split('order by')[0]
        if 'join' in query_in:
            #pdb.set_trace()
            #self.query_dict['INNER JOIN'] = \
            #query_in.split('join')[1].split('where')[0].split('group by')[0].split('order by')[0]
            join_list = query_in.split('join')[1:]
            join_string = [i.split('where')[0].split('group by')[0].split('order by')[0] for i in join_list]
            self.query_dict['INNER JOIN'] = \
                '\n join '.join(join_string)
        else:
            self.query_dict['INNER JOIN'] = ""
        if 'where' in query_in:
            self.query_dict['WHERE'] = query_in.split('where')[1].split('group by')[0].split('order by')[0]
        else:
            self.query_dict['WHERE'] = ""
        if 'group' in query_in:
            self.query_dict['GROUP BY'] = query_in.split('group by')[1].split('order by')[0]
        else:
            self.query_dict['GROUP BY'] = ""
        if 'order' in query_in:
            self.query_dict['ORDER BY'] = query_in.split('order by')[1]
        else:
            self.query_dict['ORDER BY'] = ""

    def clearQueryText(self):
        self.query_dict = {"SELECT": "*",
                      "FROM": "",
                      "INNER JOIN": "",
                      "WHERE": "",
                      "GROUP BY": "",
                      "ORDER BY": ""
                      }
        self.textEdit_SQL_Query.setText("")

    def loadLastQueryText(self):

        self.textEdit_SQL_Query.setText(self.last_query)

    def saveQueryText(self):

        self.saved_query = self.textEdit_SQL_Query.toPlainText()
        save_key = self.lineEdit_SQL_Save_Query.text()
        self.scripted_queries[save_key] = self.saved_query
        self.comboBox_scriptedQueries.addItem(save_key)

    def loadQueryText(self):

        self.textEdit_SQL_Query.setText(self.saved_query)

    def loadAllQueryText(self):
        self.clearQueryText()
        TABLE_NAME = self.comboBox_table_name.currentText()
        SCHEMA_NAME=self.comboBox_database_name.currentText()
        self.query_dict['SELECT'] = TABLE_NAME[:3]+'.*'
        self.query_dict['FROM'] = "{0}.{1}".format(SCHEMA_NAME, TABLE_NAME) + ' AS '+TABLE_NAME[:3]#+'\n'
        query_final = self.assembleQueryDict()
        self.textEdit_SQL_Query.setText(query_final)

    def loadWhereStatement(self, new_condition):

        self.populateQueryDict()
        query_in = self.assembleQueryDict()
        for new_condition_key, new_condition_query in new_condition.items():
            if 'where' in query_in.lower():
                where_query = self.query_dict['WHERE']
                and_list = where_query.lower().split('and')
                if 'between' in where_query.lower():
                    between_list = ['AND'.join([and_list[i], and_list[i + 1]]) for i in range(len(and_list)) if 'between' in and_list[i]]
                    and_list = [i for i in and_list if i.lower() not in ' and '.join(between_list).lower()]
                    and_list.extend(between_list)
                elif 'and' in where_query.lower():
                    and_list = where_query.split('and')
                else:
                    and_list = [where_query]

                and_list = [i for i in and_list if new_condition_key.lower() not in i]
                and_list.append(new_condition_query)
                self.query_dict['WHERE'] = ' AND '.join(and_list)
            else:
                self.query_dict['WHERE'] = new_condition_query

    def loadLastDayQueryText(self):

        last_day_query = "DATETIME > NOW() - INTERVAL 1 DAY"
        self.loadWhereStatement({timestamp_or_datetime: last_day_query})
        if self.query_dict['ORDER BY'] == "":
            self.query_dict['ORDER BY'] = "{} DESC".format(timestamp_or_datetime)
        query_final = self.assembleQueryDict()
        self.textEdit_SQL_Query.setText(query_final)

    def loadLastHourQueryText(self):

        last_hour_query = "DATETIME > NOW() - INTERVAL 1 HOUR"
        self.loadWhereStatement({timestamp_or_datetime: last_hour_query})
        if self.query_dict['ORDER BY'] == "":
            self.query_dict['ORDER BY'] = "{} DESC".format(timestamp_or_datetime)
        query_final = self.assembleQueryDict()
        self.textEdit_SQL_Query.setText(query_final)

    def loadBetweenDateTime(self):
        if timestamp_or_datetime == 'TIMESTAMP':
            dS = self.dateTimeEdit_start.dateTime().toString('yyyyMMdd_hhmmss')
            dE = self.dateTimeEdit_end.dateTime().toString('yyyyMMdd_hhmmss')
        else:
            dS = self.dateTimeEdit_start.dateTime().toString('yyyy-MM-dd hh:mm:ss')
            dE = self.dateTimeEdit_end.dateTime().toString('yyyy-MM-dd hh:mm:ss')

        in_between_query = ''' {0} BETWEEN '{1}' and '{2}' '''.format(timestamp_or_datetime, dS, dE)
        self.loadWhereStatement({timestamp_or_datetime: in_between_query})
        if self.query_dict['ORDER BY'] == "":
            self.query_dict['ORDER BY'] = "{} DESC".format(timestamp_or_datetime)
        query_final = self.assembleQueryDict()
        self.textEdit_SQL_Query.setText(query_final)

    def loadBetweenWavelengths(self):
        wS = self.doubleSpinBox_lower.value()
        wE = self.doubleSpinBox_upper.value()
        wavelength_label = 'proc_mono_wavelength'
        in_between_query = ''' {0} BETWEEN {1:0.3f} and {2:0.3f}'''.format(wavelength_label, wS, wE)
        self.loadWhereStatement({wavelength_label: in_between_query})
        if self.query_dict['ORDER BY'] == "":
            self.query_dict['ORDER BY'] = "{} DESC".format(timestamp_or_datetime)
        query_final = self.assembleQueryDict()
        self.textEdit_SQL_Query.setText(query_final)

    def addLockin(self):

        self.populateQueryDict()
        TABLE_NAME = self.comboBox_table_name.currentText()
        REF_TABLE_NAME = 'reference_detector'
        LOCKIN_QUERY = 'SQRT(POW(AVG({0}.lockin_x), 2) + POW(AVG({0}.lockin_y), 2)) as lockin_out'.format(REF_TABLE_NAME[0:3])
        if self.query_dict['SELECT'] == "":
            self.query_dict['SELECT'] = '{0}.*, {1}'.format(TABLE_NAME[:3], LOCKIN_QUERY)
        else:
            select_list = self.query_dict['SELECT'].split(',')
            select_query = ', '.join(['{0}.{1}'.format(TABLE_NAME[0:3],i.split('.')[-1]) for i in select_list])
            select_query = ', '.join([select_query, LOCKIN_QUERY])
            self.query_dict['SELECT'] = select_query
        self.query_dict['FROM'] = 'spectral_cal {0}'.format(TABLE_NAME[:3])
        self.query_dict['INNER JOIN'] = '{1} {2} ON {0}.RecordGroup = {2}.RecordGroup AND {0}.RecordGroupInd = {2}.RecordGroupInd '.format(TABLE_NAME[:3], REF_TABLE_NAME, REF_TABLE_NAME[0:3])
        self.query_dict['GROUP BY'] = '{2}.RecordGroupInd'.format(TABLE_NAME[:3], REF_TABLE_NAME, REF_TABLE_NAME[0:3])
        self.query_dict['ORDER BY'] = '{0}.meta_mono_wavelength asc '.format(TABLE_NAME[:3], REF_TABLE_NAME, REF_TABLE_NAME[0:3])

        query_final = self.assembleQueryDict()
        #print(query_final)
        self.textEdit_SQL_Query.setText(query_final)

    def addBlue(self):
        self.addPyhk('green')

    def addGreen(self):
        self.addPyhk('green')

    def addPyhk(self, DB_NAME_PYHK):
        self.populateQueryDict()
        #DB_NAME = self.comboBox_database_name.currentText()
        TABLE_NAME = self.comboBox_table_name.currentText()
        #REF_TABLE_NAME_1 = 'temperature'

        # Get list of tables in Blue/Green
        sql_statement = '''
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = "{}";'''.format(DB_NAME_PYHK)
        self.open_ssh_tunnel()
        self.mysql_connect()
        self._cursor.execute(sql_statement)
        indexList = self._cursor.fetchall()
        tableNames = [i[0] for i in indexList]
        self.mysql_disconnect()
        self.close_ssh_tunnel()

        select_list = self.query_dict['SELECT'].split(',')
        self.query_dict['SELECT'] = ""
        select_query = ', '.join(
            ['{0}.{1}'.format(TABLE_NAME[0:3], i.split('.')[-1]) for i in select_list if '(' not in i])

        LEAD_TXT = ""
        LEAD_PRE = TABLE_NAME[:3]
        for REF_TABLE_NAME in tableNames:
            print(REF_TABLE_NAME)
            # Get list of columns in pressure, etc.
            self.open_ssh_tunnel()
            self.mysql_connect(db_name=DB_NAME_PYHK)
            self._cursor.execute("DESCRIBE {}".format(REF_TABLE_NAME))
            indexList = self._cursor.fetchall()
            columnNames = [i[0] for i in indexList]
            self.mysql_disconnect()
            self.close_ssh_tunnel()

            PYHK_QUERY = ', '.join(['avg({0}.{1}) as avg_{1}\n'.format(REF_TABLE_NAME[:3], i) for i in columnNames[3:]])
            if select_list == "":
                self.query_dict['SELECT'] = '{0}.*'.format(TABLE_NAME[:3], PYHK_QUERY)
            else:
                self.query_dict['SELECT'] = ', '.join([self.query_dict['SELECT'], PYHK_QUERY])

            TRAIL_PRE = REF_TABLE_NAME[0:3]
            #self.query_dict['INNER JOIN'] += '{4}{3}.{1} {2} ON {0}.RecordGroup = {2}.RecordGroup AND {0}.RecordGroupInd = {2}.RecordGroupInd\n ' \
            #    .format(LEAD_PRE, REF_TABLE_NAME, TRAIL_PRE, DB_NAME_PYHK, LEAD_TXT)
            self.query_dict[
                'INNER JOIN'] += '{0}{1}.{2} {3} ON {4}.RecordGroup = {3}.RecordGroup AND {4}.RecordGroupInd = {3}.RecordGroupInd\n ' \
                .format(LEAD_TXT, DB_NAME_PYHK, REF_TABLE_NAME, TRAIL_PRE, LEAD_PRE)
            LEAD_TXT = "INNER JOIN "
            LEAD_PRE = REF_TABLE_NAME[0:3]
            #pdb.set_trace()

        self.query_dict['SELECT'] = ' '.join([select_query, self.query_dict['SELECT']])
        self.query_dict['FROM'] = 'spectral_cal {0}'.format(TABLE_NAME[:3])
        #self.query_dict['INNER JOIN'] = '{3}.{1} {2} ON {0}.RecordGroup = {2}.RecordGroup AND {0}.RecordGroupInd = {2}.RecordGroupInd '\
        #    .format(TABLE_NAME[:3], REF_TABLE_NAME, REF_TABLE_NAME[0:3], DB_NAME_PYHK)
        self.query_dict['GROUP BY'] = '{2}.RecordGroupInd'.format(TABLE_NAME[:3], REF_TABLE_NAME, REF_TABLE_NAME[0:3])
        self.query_dict['ORDER BY'] = '{0}.meta_mono_wavelength asc '.format(TABLE_NAME[:3], REF_TABLE_NAME, REF_TABLE_NAME[0:3])

        query_final = self.assembleQueryDict()
        #print(query_final)
        self.textEdit_SQL_Query.setText(query_final)


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = SQLQueryWindow()
    window.mainwindow.show()
    sys.exit(app.exec_())
