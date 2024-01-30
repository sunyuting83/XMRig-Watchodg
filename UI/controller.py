# -*- coding: utf-8 -*-
import os

from threading import Thread
from PyQt5.QtWidgets import  QMessageBox, QFileDialog
from .main import MainView
from Utils.utils import CurrentTimeStr, getDocPath, CheckPath, checkXMR, SaveConfigFile, create_shortcut, stop_thread, KillExecNameDontCheck, get_language
from UI.SignalUnit import signal
from public import gl_info, gl_thread_event, version
from task import TaskMain
from CheckUpdate import CheckUpdate

class MainController:
    def __init__(self, program_path, program_name, yaml_data, lanaguage_data):
        super().__init__()
        self.mainView = MainView()
        self.program_path = program_path
        self.program_name = os.path.join(program_path, program_name)
        self.my_self_name = program_name
        self.yamlpath = os.path.join(program_path, "config.yaml")
        self.configData = yaml_data
        file_path, self.myself_ext = os.path.splitext(program_name)
        self.myself_filename = file_path.split(os.sep)[-1]
        self.lanaguage_data = lanaguage_data
        self.modify_row = 0
        language = get_language()
        if language not in lanaguage_data:
            self.languageData = lanaguage_data['en']
        elif 'Language' in yaml_data:
            self.languageData = lanaguage_data[yaml_data['Language']]
        else:
            self.languageData = lanaguage_data[language]
        self.retranslateUi()
        self.event_init()
        self.operate_show()
    
    def show_msg(self, msg):
        QMessageBox.warning(self.mainView, self.languageData['Alert'], msg, QMessageBox.Yes)
    
    def operate_show(self):
        self.mainView.show()
        if self.configData['PoolUri'] == '' or self.configData['PoolUser'] == '':
            self.mainView.tabWidget.setCurrentIndex(1)
    
    # UI """ 事件初始化 """
    def event_init(self):
        self.set_comboBox()
        signal.log.connect(self.display_log)
        signal.label.connect(self.display_label)
        signal.progress.connect(self.updata_ui)
        self.mainView.pushButton_2.clicked.connect(self.save_config)
        self.mainView.comboBox.currentIndexChanged.connect(self.change_lanaguagel)

        if 'PoolDonate' in self.configData:
            self.mainView.lineEdit_7.setText('0')
            self.mainView.label_15.setText(str(self.configData["PoolDonate"]))
        if 'PoolUri' in self.configData:
            if self.configData['PoolUri'] == '':
                self.mainView.label_19.setText(self.languageData['NotYetAcquired'])
            else:
                self.mainView.label_19.setText(self.configData["PoolUri"])
        
        SystemPath = getDocPath()
        wmic_path = os.path.join(SystemPath, 'wbem', 'wmic.exe')
        if os.path.exists(wmic_path) == False:
            signal.log.emit(self.languageData['CantRun'])
            self.show_msg(self.languageData['CantRun'])
            return
        if self.myself_ext == '.exe':
            start_menu = os.path.join(os.getenv("APPDATA"), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            CheckPath(start_menu)
            myself_lnk = f'{self.myself_filename}.lnk'
            self.start_file = os.path.join(start_menu, myself_lnk)
            if os.path.exists(self.start_file):
                self.at_start = True
                self.mainView.checkBox.setChecked(True)
            else:
                self.at_start = False
                self.mainView.checkBox.setChecked(False)
        
        # 开启更新检测线程
        _, xmrigName = os.path.split(self.configData["XmrigPath"])
        c_thread = Thread(target=CheckUpdate, args=(self.program_path, self.my_self_name, xmrigName, self.languageData,))
        c_thread.start()
        gl_info['check_thread'] = c_thread
        
        if self.configData["XmrigPath"] != "":
            if 'XmrigPath' in self.configData and checkXMR(self.configData["XmrigPath"]):
                # start
                self.mainView.lineEdit.setText(self.configData["XmrigPath"])
                self.mainView.lineEdit_3.setText(self.configData["PoolUri"])
                self.mainView.textEdit.setPlainText(self.configData["PoolUser"])
                self.mainView.lineEdit_4.setText(self.configData["PoolPass"])
                self.mainView.checkBox_3.setChecked(self.configData["PoolTLS"])
                self.mainView.lineEdit_5.setText(self.configData["PoolSocks5"])
                self.mainView.lineEdit_6.setText(self.configData["PoolTLSFingerprint"])
                self.mainView.lineEdit_7.setText(str(self.configData["PoolDonate"]))
                signal.log.emit(self.languageData['XmrigPath']+'\r' + self.configData["XmrigPath"])
                if 'PoolUri' in self.configData and \
                    self.configData['PoolUri'] != '' and \
                    'PoolUser' in self.configData and \
                    self.configData['PoolUser'] != '':
                    self.start_thread()
                else:
                    signal.log.emit(self.languageData['StartErr'])
                    self.show_msg(self.languageData['StartErr'])
        self.mainView.checkBox.clicked.connect(self.add2start)
        self.mainView.toolButton.clicked.connect(self.load_file)
        self.mainView.pushButton.clicked.connect(self.first_start)

    def add2start(self):
        if self.myself_ext == '.exe':
            if self.mainView.checkBox.isChecked():
                create_shortcut(self.program_name, self.start_file)
                signal.log.emit(self.languageData['StartMenuAdd'])
                self.show_msg(self.languageData['StartMenuAdd'])
            else:
                if os.path.exists(self.start_file):
                    os.remove(self.start_file)
                signal.log.emit(self.languageData['StartMenuRemove'])
                self.show_msg(self.languageData['StartMenuRemove'])
        else:
            self.mainView.checkBox.setChecked(False)
            signal.log.emit(self.languageData['StartMenuDev'])
            self.show_msg(self.languageData['StartMenuDev'])
    
    def check_xmr_path(self, xmr_path):
        return checkXMR(xmr_path)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.mainView, self.languageData['SelectAFile'], "",
                                                            "EXE Files (*.exe)")
        if file_path:
            if ".exe" in file_path:
                if self.check_xmr_path(file_path):
                    self.mainView.lineEdit.setText(file_path)
                    self.configData['XmrigPath'] = file_path
                    SaveConfigFile(self.yamlpath, self.configData)
                    signal.log.emit(self.languageData['XmrPath'])
                    
                    if 'PoolUri' in self.configData and \
                          self.configData['PoolUri'] != '' and \
                          'PoolUser' in self.configData and \
                          self.configData['PoolUser'] != '':
                        self.mainView.pushButton.setEnabled(True)
                else:
                    signal.log.emit(self.languageData['XmrPathErr'])
                    self.show_msg(self.languageData['XmrPathErr'])

    # start_thread
    def start_thread(self):
        t_thread = Thread(target=TaskMain, args=(self.configData, self.languageData))
        t_thread.start()
        gl_info['task_thread'] = t_thread

    
    def display_log(self, content):
        new_content = '%s%s%s%s%s%s'% (content, "---", CurrentTimeStr(), '\n', '-------------------------------------------------------------------------------------------', '\n')
        self.mainView.textBrowser.insertPlainText(new_content)
        self.mainView.textBrowser.moveCursor(self.mainView.textBrowser.textCursor().Start)
    
    def get_label(self, lab):
        if lab == 'status':
            return self.mainView.label_3
        if lab == 'speed':
            return self.mainView.label_5
        if lab == 'huge':
            return self.mainView.label_7
        if lab == 'pages':
            return self.mainView.label_9
        if lab == 'cpu':
            return self.mainView.label_11
        if lab == 'mem':
            return self.mainView.label_13
        if lab == 'board':
            return self.mainView.label_17
        if lab == 'donate':
            return self.mainView.label_15
    
    def display_label(self, lab, content):
        label = self.get_label(lab)
        label.setText(content)
    
    def first_start(self):
        gl_thread_event.set()
        # if gl_info['check_thread'] != None:
        #     stop_thread(gl_info['check_thread'])

        if gl_info['task_thread'] != None:
            stop_thread(gl_info['task_thread'])
            KillExecNameDontCheck('xmrig.exe')
            gl_info['Status'] = False
        gl_thread_event.clear()
        self.start_thread()
        self.mainView.label_19.setText(self.configData['PoolUri'])
        self.mainView.pushButton.setEnabled(False)
        self.mainView.tabWidget.setCurrentIndex(0)
    
    def save_config(self):
        PoolUri = self.mainView.lineEdit_3.text()
        PoolUser = self.mainView.textEdit.toPlainText()
        PoolPass = self.mainView.lineEdit_4.text()
        PoolTLS = self.mainView.checkBox_3.isChecked()
        PoolSocks5 = self.mainView.lineEdit_5.text()
        PoolTLSFingerprint = self.mainView.lineEdit_6.text()
        PoolDonate = self.mainView.lineEdit_7.text()
        # print(PoolUri, PoolUser, PoolPass, PoolTLS, PoolSocks5, PoolTLSFingerprint, PoolDonate)
        if PoolUri != '' and PoolUser != '' :
            self.configData['PoolUri'] = PoolUri
            self.configData['PoolUser'] = PoolUser
            if PoolPass == '':
                PoolPass = '测试矿工'
            self.configData['PoolPass'] = PoolPass
            self.configData['PoolTLS'] = PoolTLS
            self.configData['PoolSocks5'] = PoolSocks5
            self.configData['PoolTLSFingerprint'] = PoolTLSFingerprint
            if PoolDonate == '':
                PoolDonate = '0'
            self.configData['PoolDonate'] = int(PoolDonate)
            SaveConfigFile(self.yamlpath, self.configData)
            self.mainView.lineEdit_3.setText(PoolUri)
            self.mainView.textEdit.setPlainText(PoolUser)
            self.mainView.lineEdit_4.setText(PoolPass)
            self.mainView.checkBox_3.setChecked(PoolTLS)
            self.mainView.lineEdit_5.setText(PoolSocks5)
            self.mainView.lineEdit_6.setText(PoolTLSFingerprint)
            self.mainView.lineEdit_7.setText(PoolDonate)
            if 'XmrigPath' in self.configData and checkXMR(self.configData["XmrigPath"]):
                self.mainView.pushButton.setEnabled(True)
            self.show_msg(self.languageData['SaveConfig'])
            signal.log.emit(self.languageData['SaveConfig'])
        else:
            self.show_msg(self.languageData['CantSaveConfig'])
            signal.log.emit(self.languageData['CantSaveConfig'])
    
    def updata_ui(self, progress):
        if progress < 100:
            self.mainView.label_20.setVisible(True)
            self.mainView.progressBar.setVisible(True)
            self.mainView.progressBar.setValue(progress)
        else:
            self.display_log('更新成功')
            self.mainView.label_20.setVisible(False)
            self.mainView.progressBar.setVisible(False)
    
    def set_comboBox(self):
        if 'LanguageList' in self.lanaguage_data and \
            self.lanaguage_data['LanguageList'] != None:
                Language = self.lanaguage_data['LanguageList']
                for i in range(len(Language)):
                    if 'Code' in Language[i]:
                        self.mainView.comboBox.addItem(Language[i]['Language'])
                        if Language[i]['Code'] == self.configData['Language']:
                            self.mainView.comboBox.setCurrentIndex(i)
    
    def change_lanaguagel(self, i):
        if 'LanguageList' in self.lanaguage_data and \
            self.lanaguage_data['LanguageList'] != None and \
            len(self.lanaguage_data['LanguageList']) != 0:
                self.languageData = self.lanaguage_data[self.lanaguage_data['LanguageList'][i]['Code']]
                self.configData['Language'] = self.lanaguage_data['LanguageList'][i]['Code']
                SaveConfigFile(self.yamlpath, self.configData)
                self.retranslateUi()
    
    def retranslateUi(self):
        self.mainView.setWindowTitle(self.languageData['Title'] + ' ' +version)
        self.mainView.groupBox_3.setTitle(self.languageData['Log'])
        self.mainView.groupBox_2.setTitle(self.languageData['Status'])
        self.mainView.label_2.setText(self.languageData['Status'])
        self.mainView.label_3.setText(self.languageData['XmrStatus5'])
        self.mainView.label_4.setText(self.languageData['LastSpeed'])
        self.mainView.label_5.setText(self.languageData['NotYetAcquired'])
        self.mainView.label_6.setText(self.languageData['HugePages'])
        self.mainView.label_7.setText(self.languageData['NotYetAcquired'])
        self.mainView.label_8.setText(self.languageData['1gbPages'])
        self.mainView.label_9.setText(self.languageData['NotYetAcquired'])
        self.mainView.label_10.setText(self.languageData['Cpu'])
        self.mainView.label_11.setText(self.languageData['NotYetAcquired'])
        self.mainView.label_12.setText(self.languageData['Memory'])
        self.mainView.label_13.setText(self.languageData['NotYetAcquired'])
        self.mainView.label_14.setText(self.languageData['Donate'])
        self.mainView.label_16.setText(self.languageData['MotherBoard'])
        self.mainView.label_17.setText(self.languageData['NotYetAcquired'])
        self.mainView.label_18.setText(self.languageData['PoolUrl'])
        self.mainView.label_19.setText(self.languageData['NotYetAcquired'])
        self.mainView.label_20.setText(self.languageData['Updating'])
        self.mainView.tabWidget.setTabText(0, self.languageData['Status'])
        self.mainView.groupBox.setTitle(self.languageData['BasicSettings'])
        self.mainView.label.setText(self.languageData['XmrigPath'])
        self.mainView.toolButton.setText(self.languageData['Select'])
        self.mainView.checkBox.setText(self.languageData['AutomaticallyAtStartup'])
        self.mainView.label_28.setText(self.languageData['Language'])
        self.mainView.groupBox_4.setTitle(self.languageData['PoolSettings'])
        self.mainView.label_21.setText(self.languageData['PoolUrl'])
        self.mainView.checkBox_3.setText(self.languageData['EnableTls'])
        self.mainView.label_22.setText(self.languageData['WalletAddress'])
        self.mainView.label_23.setText(self.languageData['WorkerName'])
        self.mainView.label_24.setText(self.languageData['Socks5Url'])
        self.mainView.label_25.setText(self.languageData['TlsFingerprint'])
        self.mainView.label_27.setText("%")
        self.mainView.label_26.setText(self.languageData['Donate'])
        self.mainView.pushButton.setText(self.languageData['FirstRun'])
        self.mainView.pushButton_2.setText(self.languageData['Save'])
        self.mainView.tabWidget.setTabText(1, self.languageData['Setup'])