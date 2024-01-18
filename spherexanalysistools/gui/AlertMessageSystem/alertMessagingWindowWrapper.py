import pdb
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
#from queue import Empty, Queue
from threading import Thread, Lock
import paramiko
import numpy as np
import pandas as pd
import mmap
import logging
from pathlib import Path
import time, datetime
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from alertMessagingWindow import Ui_MainWindow

rec_lock = Lock()

# For text messages
sms_gateway = {}
sms_gateway['verizon'] = 'vtext.com'
sms_gateway['tmobile'] = 'tmomail.net'
sms_gateway['sprint'] = 'messaging.sprintpcs.com'
sms_gateway['att'] = 'txt.att.net'

# For text messages including images
mms_gateway = {}
mms_gateway['verizon'] = 'vzwpix.com'
mms_gateway['tmobile'] = 'tmomail.net'
mms_gateway['sprint'] = 'pm.sprint.com'
mms_gateway['att'] = 'mms.att.net'

phone_numbers = {}
phone_numbers["Marco"] = {'tmobile': '6263790255'}
phone_numbers["Howard"] = {'att': '9712750526'}
phone_numbers["Sam"] = {'verizon': '3604636805'}
phone_numbers["Chi"] = {'tmobile': '5208226335'}
phone_numbers["Phil"] = {'verizon': '3477420215'}
phone_numbers["Hien"] = {'verizon': '8186348054'}
phone_numbers["Steve"] = {'verizon': '3477420215'}

email_addresses = {}
email_addresses["Marco"] = "mviero@caltech.edu"
email_addresses["Howard"] = "hhui@caltech.edu"
email_addresses["Sam"] = "scondon@caltech.edu"
email_addresses["Chi"] = "chnguyen@caltech.edu"
email_addresses["Phil"] = "pkorngut@caltech.edu"
email_addresses["Hien"] = "hitnguyen@gmail.com"
email_addresses["Steve"] = "spadin@caltech.edu"


hardcoded_list = {'Marco': {'sms': True, 'email': True},
                  'Howard': {'sms': True, 'email': True},
                  'Sam': {'sms': True, 'email': True},
                  'Chi': {'sms': True, 'email': True},
                  'Steve': {'sms': False, 'email': False},
                  'Hien': {'sms': False, 'email': False},
                  'Phil': {'sms': False, 'email': False}
                  }
hardcoded_list_test = {'Marco': {'sms': True, 'email': True},
                  'Howard': {'sms': False, 'email': False},
                  'Sam': {'sms': False, 'email': False},
                  'Chi': {'sms': False, 'email': False},
                  'Steve': {'sms': False, 'email': False},
                  'Hien': {'sms': False, 'email': False},
                  'Phil': {'sms': False, 'email': False}
                  }

auto_load = {'local': [{'temperature': '20k%20plate'}],
             'green': [{'pressure': 'pt%20avg%20delta'},
                      {'temperature': '20k%20plate'},
                      {'temperature': '80k%20plate'}
                      ],
             'blue': [{'pressure': 'pt%20avg%20delta'},
                      {'temperature': '20k%20plate'},
                      {'temperature': '80k%20plate'}
                      ]
             }

limit_dict = {'80k': {('<', '>'): [40, 150]},
              '20k': {('<', '>'): [20, 150]},
              'ts': {('=', '>'): [0, 10]},
              'delta': {('<', '>'): [150, 300]}
              }

sent_start_end_alerts = True
send_alerts = True
crashTrigger = 5 * 60  # Send Alarm when reading has stopped for this number of seconds.
readDelay = 0.5  # time to wait between readings.  Made larger to prevent crashing.

class alertMessagingWindow(Ui_MainWindow):
    ''' Choose readings to monitor.  Send alert email/sms if goes out of range.

    '''

    #lock = threading.Lock()
    #lock_initialized = True

    #startup_signal = QtCore.pyqtSignal()
    #update_signal = QtCore.pyqtSignal(object)
    #shutdown_signal = QtCore.pyqtSignal()

    #queue = Queue()

    cdict = {}

    global pdict
    pdict = {}

    def __init__(self, wait=readDelay):
        super().__init__()
        self._wait = wait
        self.mainwindow = QtWidgets.QMainWindow()
        self.setupUi(self.mainwindow)

        self._server = {}
        self.updateServer()
        self.tableCurrentFiles()
        self.autoLoadFields()

        self.comboBox_Server_Location.currentIndexChanged.connect(self.clearFields)
        self.comboBox_Server_Location.currentIndexChanged.connect(self.updateServer)
        self.comboBox_Server_Location.currentIndexChanged.connect(self.tableCurrentFiles)
        self.comboBox_Server_Location.currentIndexChanged.connect(self.autoLoadFields)

        self.populatePeople()

        try:
            self.pushButton_Refresh.clicked.connect(self.tableCurrentFiles)
        except Exception as e:
            print(e)

        self.pushButton_Start.clicked.connect(self.startMonitors)
        self.pushButton_Stop.clicked.connect(self.stopMonitors)
        self.listView_table.doubleClicked.connect(self.addToSettingsDict)
        self.pushButton_clearFields.clicked.connect(self.clearFields)

        #self.stopMonitors()

    def autoLoadFields(self):

        comboBoxTextIn = self.comboBox_Server_Location.currentText()
        if comboBoxTextIn in list(auto_load.keys()):
            print('auto loading '+comboBoxTextIn)
            for i in auto_load[comboBoxTextIn]:
                self.addToSettingsDict(i)

    def populatePeople(self):

        for person in hardcoded_list:

            if person not in pdict:
                dictIn = {'name': person,
                          'sms': hardcoded_list[person]['sms'],
                          'email': hardcoded_list[person]['email']
                          }
                try:
                    horizWidget = peopleHorizonatalLine(dictIn)
                    self.addToVerticalLayout_4(horizWidget)
                    pdict[person] = horizWidget
                    print(person)
                except Exception as e:
                    print(e)
                    raise e

        self.textEdit_Log = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.textEdit_Log.setMaximumSize(QtCore.QSize(16777215, 900))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textEdit_Log.setFont(font)
        self.textEdit_Log.setObjectName("textEdit_Log")
        self.verticalLayout_4.addWidget(self.textEdit_Log)
        self.verticalLayout_4.setAlignment(self.textEdit_Log, Qt.AlignBottom)

    def loopThrough(self):

        print('loopthrough started')
        try:
            self.open_sftp_connection()
            while np.sum([self.cdict[i].running for i in self.cdict]):
                for field in self.cdict:
                    if self.cdict[field].running:
                        self.cdict[field].run()
            else:
                print('thread no longer running')
                self.comboBox_Running.setCurrentIndex(0)
            self.close_sftp_connection()

        except Exception as e:
            print(e)
            print('threads shut down')

    def addToSettingsDict(self, signalIn):

        # Use field name as key to self.cdict
        try:
            key = os.path.basename(signalIn.data()).split('.txt')[0]
            mea = signalIn.data().split('/')[0]
        except:
            key = list(signalIn.values())[0]
            mea = list(signalIn.keys())[0]

        print('key is {}'.format(key))

        # If not present, add key and dict to self.cdict and verticalLayout
        if key not in self.cdict:
            dictIn = {'field_name': key, 'type_name': mea}
            #dictIn['condition'] = list([val0.keys() for key0, val0 in limit_dict.items() if key0 in key][0])[0]
            #dictIn['limit_val'] = list([val0.values() for key0, val0 in limit_dict0.items() if key0 in key][0])[0]
            dictIn['condition_lo'] = [list(val0.keys())[0][0] for key0, val0 in limit_dict.items() if key0 in key][0]
            dictIn['condition_hi'] = [list(val0.keys())[0][1] for key0, val0 in limit_dict.items() if key0 in key][0]
            dictIn['limit_val_lo'] = [list(val0.values())[0][0] for key0, val0 in limit_dict.items() if key0 in key][0]
            dictIn['limit_val_hi'] = [list(val0.values())[0][1] for key0, val0 in limit_dict.items() if key0 in key][0]
            dictIn['check_box'] = True
            dictIn['server'] = self._server
            dictIn['alert_sent'] = False
            dictIn['alert_type'] = 'email_and_text'

            try:
                #pdb.set_trace()
                horizWidget = conditionHorizontalLine(dictIn)
                self.addToVerticalLayout(horizWidget)
                self.cdict[key] = horizWidget
                #horizWidget.start()
                #self.queue.append(horizWidget)
                loggingBox_text = "{} - Field {} ADDED.".format(datetime.now().strftime("%Y/%m/%d at %M:%H:%S"), key)
                self.textEdit_loggingBox.append(loggingBox_text)
            except Exception as e:
                print(e)
                raise e

    def startMonitors(self):
        alert_text = '''At {0} the SLT Alert System was INITIATED at {1}'''\
            .format(datetime.now().strftime("%H:%M:%S on %Y/%m/%d"), self.comboBox_Server_Location.currentText())
        if sent_start_end_alerts:
            alertMessagingWindow.sendAlertMessage(subject='SpherexLabTools GUI Started', text=alert_text)

        self.comboBox_Running.setCurrentIndex(1)
        for key in self.cdict:
            print("starting {}".format(key))
            self.cdict[key].start()
            loggingBox_text = "{} - Field {} STARTED.".format(datetime.now().strftime("%Y/%m/%d at %M:%H:%S"), key)
            self.textEdit_loggingBox.append(loggingBox_text)
        self.loopThrough()

    def stopMonitors(self):
        alert_text = '''At {0} the SLT Alert System was TERMINATED at {1}'''\
            .format(datetime.now().strftime("%H:%M:%S on %Y/%m/%d"), self.comboBox_Server_Location.currentText())
        alertMessagingWindow.sendAlertMessage(subject='SpherexLabTools GUI Stopped', text=alert_text)

        self.comboBox_Running.setCurrentIndex(0)
        for key in self.cdict:
            print("stopping {}".format(key))
            self.cdict[key].stop()
            loggingBox_text = "{} - Field {} STOPPED.".format(datetime.now().strftime("%Y/%m/%d at %M:%H:%S"), key)
            self.textEdit_loggingBox.append(loggingBox_text)

    def addToVerticalLayout(self, horizWidget):

        self.verticalLayout.addWidget(horizWidget)
        self.verticalLayout.setAlignment(horizWidget, Qt.AlignTop)

    def addToVerticalLayout_4(self, horizWidget):

        self.verticalLayout_4.addWidget(horizWidget)
        self.verticalLayout_4.setAlignment(horizWidget, Qt.AlignTop)

    def clearFields(self):

        if len(self.cdict):
            # Delete widgets from https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt
            for i in reversed(range(self.verticalLayout.count())):
                self.cdict[self.verticalLayout.itemAt(i).widget().objectName()].stop()
                self.verticalLayout.itemAt(i).widget().setParent(None)
        self.cdict = {}
        self.comboBox_Running.setCurrentIndex(0)
        loggingBox_text = "{} - Fields CLEARED.".format(datetime.now().strftime("%Y/%m/%d at %M:%H:%S"))
        self.textEdit_loggingBox.append(loggingBox_text)

    def readLastLine(self, path_file, local=True):

        if local:
            with open(path_file, 'r') as f:
                lines = f.read().splitlines()
                last_line = lines[-1]
                return [float(i) for i in last_line.split('\t')]
        else:
            with sftp_client.open(path_file) as remote_file:
                last_line = str(remote_file.read().splitlines()[-1]).split("b")[1][1:-1]
                return [float(i) for i in last_line.split('\\t')]

    def tableCurrentFiles(self):

        include = ['temperature', 'pressure']
        d = datetime.now()
        t = time.mktime(d.timetuple())
        fp = self.getFilePathNow(self._server['path_pyhk'])

        fields = []
        if 'local' in self.comboBox_Server_Location.currentText():
            fp = os.path.join(self._server['path_pyhk'], "2022\\07\\13\\")
            for root0, dirs0, files0 in os.walk(fp):
                for dirf in dirs0:
                    if dirf in include:
                        for root, dirs, files in os.walk(os.path.join(fp, dirf)):
                            for filename in files:
                                print(filename)
                                lastLine=self.readLastLine(os.path.join(fp, dirf, filename))
                                deltaTime = t - lastLine[0]
                                #print(deltaTime)
                                if deltaTime < 5:
                                    fields.append(Path(os.path.join(dirf, filename.lower())).as_posix())
                                else:
                                    fields.append(Path(os.path.join(dirf, filename.lower())).as_posix() + ' INACTIVE')

        elif self.comboBox_Server_Location.currentText() in ['green', 'blue']:
            self.open_sftp_connection()
            for dirf in sftp_client.listdir_attr(Path(fp).as_posix()):
                if dirf.filename in include:
                    for f in sftp_client.listdir_attr(Path(os.path.join(fp, dirf.filename)).as_posix()):
                        filename = Path(os.path.join(fp, dirf.filename, f.filename)).as_posix()
                        #pdb.set_trace()
                        try:
                            lastLine = self.readLastLine(filename, local=False)
                            deltaTime = t - lastLine[0]
                            if deltaTime < 5:
                                fields.append(Path(os.path.join(dirf.filename, f.filename.lower())).as_posix())
                            else:
                                fields.append(
                                    Path(os.path.join(dirf.filename, f.filename.lower())).as_posix() + ' INACTIVE')
                        except Exception as e:
                            print(e)
                            fields.append(Path(os.path.join(dirf.filename, f.filename.lower())).as_posix() + ' INACTIVE')

            self.close_sftp_connection()

        # Display Fields in Table
        self.df_cols = pd.DataFrame(fields)
        self.cols_model = TableModel(self.df_cols)
        self.listView_table.setModel(self.cols_model)

    @staticmethod
    def getFilePathNow(path_hk):
        d = datetime.now()
        Yn = d.strftime("%Y")
        Mn = d.strftime("%m")
        Dn = d.strftime("%d")
        return os.path.join(path_hk, Yn, Mn, Dn)

    def updateServer(self):

        comboBoxTextIn = self.comboBox_Server_Location.currentText()
        if 'local' in comboBoxTextIn:
            print('using local')
            server_name = 'local'
            ssh_host = '127.0.0.1'
            ssh_username = 'spherex'
            ssh_password = 'spherex_lab'
            path_pyhk = 'D:\\spherex\\hk'

        elif 'blue' in comboBoxTextIn:
            print('using blue')
            server_name = 'blue'
            ssh_host = 'blue.pyhk.net'
            ssh_username = 'spherex'
            ssh_password = 'spherex_lab'
            path_pyhk = '/data/hk'

        elif 'green' in comboBoxTextIn:
            print('using green')
            server_name = 'green'
            ssh_host = 'green.pyhk.net'
            ssh_username = 'spherex-green'
            ssh_password = 'spherex_lab'
            path_pyhk = '/data/hk'

        elif 'skellig' in comboBoxTextIn:
            print('using skellig')
            server_name = 'skellig'
            ssh_host = 'skellig.caltech.edu'
            ssh_username = 'eng'
            ssh_password = os.environ['SKELLIG_PWD']
            path_pyhk = '/H2RG-tests/hk'

        ret = {'ssh_host': ssh_host, 'ssh_username': ssh_username, 'ssh_password': ssh_password,
               'path_pyhk': path_pyhk, 'server_name': server_name}

        self._server = ret

    @staticmethod
    def getRecipiantAddresses(people, sms=True, email=True):

        numbers = []
        emails = []
        numbers_and_emails = []
        for name in people:
            sm = sms_gateway[list(phone_numbers[name].keys())[0]]
            num = list(phone_numbers[name].values())[0]
            numbers.append('@'.join([num, sm]))
            numbers_and_emails.append('@'.join([num, sm]))
            emails.append(email_addresses[name])
        numbers_and_emails.extend(emails)

        if sms and email:
            return numbers_and_emails
        elif sms:
            return numbers
        elif email:
            return email
        else:
            return None

    def sendTestMessage(self):

        self.sendAlertMessage(text='Party on Garth!')

    @classmethod
    def sendAlertMessage(cls, subject='SPHERExLabTools GUI Alert', text='Party On Garth!'):

        base_text = 'You are getting this email from the SPHEREx Lab Alert system. '

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg.attach(MIMEText(base_text+text))

        people = list(pdict.keys())
        for person in people:
            email = pdict[person].checkBox_email.checkState()
            sms = pdict[person].checkBox_sms.checkState()
            numbers_and_emails = cls.getRecipiantAddresses([person], sms=sms, email=email)
            if numbers_and_emails is not None:
                if send_alerts:
                    try:
                        cls.open_smpt_connection()
                        cls.send_smpt_message(msg, numbers_and_emails)
                        cls.close_smpt_connection()
                    except Exception as e:
                        print(e)
                        pdb.set_trace()

    def open_sftp_connection(self):

        global sftp_client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=self._server['ssh_host'],
                           username=self._server['ssh_username'],
                           password=self._server['ssh_password'])
        sftp_client = ssh_client.open_sftp()
        loggingBox_text = "{} - SFTP Connection Opened".format(datetime.now().strftime("%Y/%m/%d at %M:%H:%S"))
        self.textEdit_loggingBox.append(loggingBox_text)

    def close_sftp_connection(self):
        sftp_client.close()
        loggingBox_text = "{} - SFTP Connection Closed".format(datetime.now().strftime("%Y/%m/%d at %M:%H:%S"))
        self.textEdit_loggingBox.append(loggingBox_text)

    @staticmethod
    def open_smpt_connection(verbose=False):
        '''Open a connection to Gmail
        '''

        global smtp
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()
        pwd = os.environ['SLT_GMAIL_PWD']
        smtp.login('spherexlabalerts@gmail.com', pwd)  # 'feavmjsgefzfkinw')

    @staticmethod
    def close_smpt_connection(verbose=False):

        smtp.quit()

    @staticmethod
    def send_smpt_message(msg, to, verbose=False):

        smtp.sendmail(from_addr="spherexlabalerts@gmail.com",
                      to_addrs=to, msg=msg.as_string())

class peopleHorizonatalLine(QtWidgets.QWidget):

    settingsDict = {}
    def __init__(self, dictIn):
        super().__init__()

        self.settingsDict = dictIn

        self.setGeometry(QtCore.QRect(330, 290, 651, 45))
        self.setObjectName(self.settingsDict['name'])
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plainTextEdit_name = QtWidgets.QPlainTextEdit(self)
        self.plainTextEdit_name.setMinimumSize(QtCore.QSize(100, 40))
        self.plainTextEdit_name.setMaximumSize(QtCore.QSize(120, 40))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.plainTextEdit_name.setFont(font)
        self.plainTextEdit_name.setObjectName(self.settingsDict['name'])
        self.plainTextEdit_name.setPlainText(self.settingsDict['name'])
        self.horizontalLayout.addWidget(self.plainTextEdit_name)
        self.checkBox_sms = QtWidgets.QCheckBox(self)
        self.checkBox_sms.setMinimumSize(QtCore.QSize(140, 40))
        self.checkBox_sms.setMaximumSize(QtCore.QSize(80, 40))
        self.checkBox_sms.setText("")
        self.checkBox_sms.setChecked(self.settingsDict['sms'])
        self.checkBox_sms.setObjectName("checkBox_sms")
        self.horizontalLayout.addWidget(self.checkBox_sms)
        self.checkBox_email = QtWidgets.QCheckBox(self)
        self.checkBox_email.setMinimumSize(QtCore.QSize(140, 40))
        self.checkBox_email.setMaximumSize(QtCore.QSize(80, 40))
        self.checkBox_email.setText("")
        self.checkBox_email.setChecked(self.settingsDict['email'])
        self.checkBox_email.setObjectName("checkBox_email")
        self.horizontalLayout.addWidget(self.checkBox_email)

class conditionHorizontalLine(QtWidgets.QWidget, Thread):

    settingsDict = {}
    def __init__(self, dictIn):
        super().__init__()
        #self.thread = None
        self.running = False

        self.settingsDict = dictIn

        self.setGeometry(QtCore.QRect(330, 290, 651, 51))
        self.setObjectName(self.settingsDict['field_name'])
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox_field = QtWidgets.QCheckBox(self)
        self.checkBox_field.setMinimumSize(QtCore.QSize(170, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.checkBox_field.setFont(font)
        self.checkBox_field.setText(self.settingsDict['field_name'])
        self.checkBox_field.setObjectName("checkBox_field")
        self.checkBox_field.setChecked(self.settingsDict['check_box'])
        self.horizontalLayout.addWidget(self.checkBox_field)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textEdit_current = QtWidgets.QTextEdit(self)
        self.textEdit_current.setFont(font)
        self.textEdit_current.setMinimumSize(QtCore.QSize(160, 35))
        self.textEdit_current.setMaximumSize(QtCore.QSize(160, 35))
        self.textEdit_current.setObjectName("textEdit_current")
        self.horizontalLayout.addWidget(self.textEdit_current)

        self.comboBox_Limit = QtWidgets.QComboBox(self)
        self.comboBox_Limit.setMaximumSize(QtCore.QSize(40, 35))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.comboBox_Limit.setFont(font)
        self.comboBox_Limit.setObjectName("comboBox_Limit")
        self.comboBox_Limit.addItem("")
        self.comboBox_Limit.addItem("")
        self.comboBox_Limit.addItem("")
        self.comboBox_Limit.setItemText(0, ">")
        self.comboBox_Limit.setItemText(1, "=")
        self.comboBox_Limit.setItemText(2, "<")
        self.comboBox_Limit.setMinimumSize(QtCore.QSize(45, 35))
        self.comboBox_Limit.setMaximumSize(QtCore.QSize(45, 35))
        self.comboBox_Limit.setCurrentText(self.settingsDict['condition_lo'])
        self.horizontalLayout.addWidget(self.comboBox_Limit)

        font = QtGui.QFont()
        font.setPointSize(14)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox.setFont(font)
        #self.doubleSpinBox.setGeometry(QtCore.QRect(980, 10, 62, 22))
        self.doubleSpinBox.setMinimumSize(QtCore.QSize(160, 35))
        self.doubleSpinBox.setMaximumSize(QtCore.QSize(160, 35))
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.doubleSpinBox.setMaximum(1000.0)
        self.doubleSpinBox.setValue(self.settingsDict['limit_val_lo'])
        self.horizontalLayout.addWidget(self.doubleSpinBox)

        self.comboBox_Limit_Hi = QtWidgets.QComboBox(self)
        self.comboBox_Limit_Hi.setMaximumSize(QtCore.QSize(40, 35))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.comboBox_Limit_Hi.setFont(font)
        self.comboBox_Limit_Hi.setObjectName("comboBox_Limit")
        self.comboBox_Limit_Hi.addItem("")
        self.comboBox_Limit_Hi.addItem("")
        self.comboBox_Limit_Hi.addItem("")
        self.comboBox_Limit_Hi.setItemText(0, ">")
        self.comboBox_Limit_Hi.setItemText(1, "=")
        self.comboBox_Limit_Hi.setItemText(2, "<")
        self.comboBox_Limit_Hi.setMinimumSize(QtCore.QSize(45, 35))
        self.comboBox_Limit_Hi.setMaximumSize(QtCore.QSize(45, 35))
        self.comboBox_Limit_Hi.setCurrentText(self.settingsDict['condition_hi'])
        self.horizontalLayout.addWidget(self.comboBox_Limit_Hi)

        font = QtGui.QFont()
        font.setPointSize(14)
        self.doubleSpinBox_Hi = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_Hi.setFont(font)
        self.doubleSpinBox_Hi.setMinimumSize(QtCore.QSize(160, 35))
        self.doubleSpinBox_Hi.setMaximumSize(QtCore.QSize(160, 35))
        self.doubleSpinBox_Hi.setObjectName("doubleSpinBox")
        self.doubleSpinBox_Hi.setMaximum(1000.0)
        self.doubleSpinBox_Hi.setValue(self.settingsDict['limit_val_hi'])
        self.horizontalLayout.addWidget(self.doubleSpinBox_Hi)

        self.textEdit_status = QtWidgets.QTextEdit(self)
        self.textEdit_status.setFont(font)
        self.textEdit_status.setMinimumSize(QtCore.QSize(150, 35))
        self.textEdit_status.setMaximumSize(QtCore.QSize(150, 35))
        self.textEdit_status.setText('Nominal')
        self.horizontalLayout.addWidget(self.textEdit_status)

        self.doubleSpinBox.valueChanged.connect(self.update_settings_dict)
        self.doubleSpinBox_Hi.valueChanged.connect(self.update_settings_dict)
        self.comboBox_Limit.currentIndexChanged.connect(self.update_settings_dict)
        self.comboBox_Limit_Hi.currentIndexChanged.connect(self.update_settings_dict)

        self.checkBox_field.stateChanged.connect(self.updateState)

    def updateState(self):
        if self.running and not self.checkBox_field.checkState():
            self.stop()
            print('stopping thread')
        elif self.checkBox_field.checkState() and not self.running:
            self.start()
            print('restarting thread')

    def start(self):
        ''' called if checkbox is True'''

        if not self.running:
            print('starting thread')
            self.running = True
            #self.run()
        else:
            raise RuntimeError("Thread already running!")

    #def join(self, timeout=0):
    #    return super().join(0)

    def run(self):
        """ Call the thread execution methods, which should be overridden in subclasses.
        """
        #pdb.set_trace()
        #while self.running:
        #    print('still running')
        self.update_last_value()
        QtWidgets.QApplication.processEvents()
        time.sleep(readDelay)

    def stop(self):
        """ called if checkbox is made False
        """
        self.running = False
        QtWidgets.QApplication.processEvents()
        print('shutting down thread')
        #pdb.set_trace()

    def update_settings_dict(self):
        self.settingsDict['condition_lo'] = self.comboBox_Limit.currentText()
        self.settingsDict['condition_hi'] = self.comboBox_Limit_Hi.currentText()
        self.settingsDict['limit_val_lo'] = self.doubleSpinBox.value()
        self.settingsDict['limit_val_hi'] = self.doubleSpinBox_Hi.value()
        try:
            self.settingsDict['alert_type'] = self.comboBox_action1.currentText()
        except Exception as e:
            print(e)
        #finally:
        #    pdb.set_trace()

    def update_last_value(self):

        with rec_lock:
            if self.settingsDict['limit_val_hi']:
                #print('updating last value')
                multiplier = 1.0
                if 'delta' in self.settingsDict['field_name']:
                    multiplier = 50
                m, t = self.get_last_value()
                m *= 1/multiplier
                #print(m)
                self.textEdit_current.setText("{0:0.4f}".format(m))

                datetime_now = datetime.now()
                t0 = time.mktime(datetime_now.timetuple())
                deltaTime = t0 - t

                if deltaTime < crashTrigger:
                    # Only monitor state if box is checked.
                    if self.checkBox_field.checkState() and not self.settingsDict['alert_sent']:
                        send_alert = False
                        if (self.settingsDict['condition_lo'] == '=') and (self.settingsDict['condition_hi'] == '='):
                            if (m == self.doubleSpinBox.value()) or (m == self.doubleSpinBox_Hi.value()):
                                send_alert = True
                        if (self.settingsDict['condition_lo'] == '=') and (self.settingsDict['condition_hi'] == '>'):
                            if (m == self.doubleSpinBox.value()) or (m > self.doubleSpinBox_Hi.value()):
                                send_alert = True
                        if (self.settingsDict['condition_lo'] == '=') and (self.settingsDict['condition_hi'] == '<'):
                            if (m == self.doubleSpinBox.value()) or (m < self.doubleSpinBox_Hi.value()):
                                send_alert = True
                        if (self.settingsDict['condition_lo'] == '>') and (self.settingsDict['condition_hi'] == '='):
                            if (m > self.doubleSpinBox.value()) or (m == self.doubleSpinBox_Hi.value()):
                                send_alert = True
                        if (self.settingsDict['condition_lo'] == '<') and (self.settingsDict['condition_hi'] == '='):
                            if (m < self.doubleSpinBox.value()) or (m == self.doubleSpinBox_Hi.value()):
                                send_alert = True
                        if (self.settingsDict['condition_lo'] == '>') and (self.settingsDict['condition_hi'] == '<'):
                            if (m > self.doubleSpinBox.value()) or (m < self.doubleSpinBox_Hi.value()):
                                send_alert = True
                        if (self.settingsDict['condition_lo'] == '<') and (self.settingsDict['condition_hi'] == '>'):
                            if (m < self.doubleSpinBox.value()) or (m > self.doubleSpinBox_Hi.value()):
                                send_alert = True
                        if send_alert:
                            alert_text = self.get_alert_message()
                            alertMessagingWindow.sendAlertMessage(text=alert_text)
                            self.settingsDict['alert_sent'] = True
                            self.textEdit_status.setText('ALERT SENT')
                            #loggingBox_text = "{} - Field {} ALERT SENT.".format(datetime.now().strftime("%Y/%m/%d at %M:%H:%S"), self.settingsDict['field_name'])
                            #self.textEdit_loggingBox.append(loggingBox_text)

                elif self.running:
                    alert_text = "{} appears to have crashed at {}".format(self.settingsDict['server']['server_name'], datetime_now.strftime("%H:%M:%S on %Y/%m/%d"))
                    print(alert_text)
                    alertMessagingWindow.sendAlertMessage(text=alert_text)
                else:
                    print('Last {0} data taken {1:0.1f} hours ago'.format(self.settingsDict['field_name'], deltaTime/3600))
                    self.running = False

    def get_alert_message(self):
        field = self.settingsDict['field_name']
        condition = self.settingsDict['condition_lo']
        limit_lo = self.settingsDict['limit_val_lo']
        mess = "At {3}: {0} on {4} is {1} {2}".format(field, condition, limit_lo, datetime.now().strftime("%H:%M:%S on %Y/%m/%d"), self.settingsDict['server']['server_name'])
        return mess

    def get_last_value(self):
        fp = alertMessagingWindow.getFilePathNow(self.settingsDict['server']['path_pyhk'])
        filename = self.settingsDict['field_name']+'.txt'
        dir = self.settingsDict['type_name']

        if '127.0.0.1' in self.settingsDict['server']['ssh_host']:
            try:
                with open(os.path.join(fp, dir, filename), 'r+b') as f:
                    mmlines = mmap.mmap(f.fileno(), 0).read().splitlines()
                    last_line = mmlines[-1].decode('utf-8')
                    t = float(last_line.split('\t')[0])
                    m = float(last_line.split('\t')[1])
                    return m, t
            except Exception as e:
                print('Failed to open', self.settingsDict['server']['ssh_host'], e)

        elif any(x in self.settingsDict['server']['ssh_host'] for x in ['green', 'blue']):
            try:
                #self.open_sftp_connection()
                for f in sftp_client.listdir_attr(Path(os.path.join(fp, dir)).as_posix()):
                    if f.filename.lower() in filename.lower():
                        sftp_filename = Path(os.path.join(fp, dir, f.filename)).as_posix()
                        try:
                            with sftp_client.open(sftp_filename, mode='r+b') as remote_file:
                                last_line = str(remote_file.read().splitlines()[-1]).split("b")[1][1:-1]
                                t = float(last_line.split('\\t')[0])
                                m = float(last_line.split('\\t')[1])
                                return m, t
                        except Exception as e:
                                print(e)

                #self.close_sftp_connection()
            except Exception as e:
                print('Failed to open', self.settingsDict['server']['ssh_host'], e)
'''
    def open_sftp_connection(self):

        global sftp_client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=self.settingsDict['server']['ssh_host'],
                           username=self.settingsDict['server']['ssh_username'],
                           password=self.settingsDict['server']['ssh_password'])
        sftp_client = ssh_client.open_sftp()

    def close_sftp_connection(self):
        sftp_client.close()
'''
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
'''
class UpdateValue(Thread):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.thread = None
        self.running = False

    def start(self):
        ' called if checkbox is True'

        if self.thread is None:
            self.thread.start()
            self.running = True
        else:
            raise RuntimeError("Thread already running!")

    def join(self, timeout=0):
        return super().join(0)

    def run(self):
        """ Call the thread execution methods, which should be overridden in subclasses.
        """

    def stop(self):
        """ called if checkbox is made False
        """
        self.thread.stop()
        #logger.debug("stop")
        #self.shutdown()
        self.running = False
'''
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = alertMessagingWindow()
    window.mainwindow.show()
    sys.exit(app.exec_())
