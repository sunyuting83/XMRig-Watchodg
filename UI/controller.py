# -*- coding: utf-8 -*-
import os

from threading import Thread
from PyQt5.QtWidgets import  QMessageBox, QFileDialog
from .main import MainView
from Utils.utils import CurrentTimeStr, getDocPath, CheckPath, checkXMR, SaveConfigFile, create_shortcut, stop_thread, KillExecNameDontCheck
from UI.SignalUnit import signal
from public import gl_info, error_value, gl_thread_event
from task import TaskMain
from CheckUpdate import CheckUpdate

class MainController:
    def __init__(self, program_path, program_name, yaml_data):
        super().__init__()
        self.mainView = MainView()
        self.program_path = program_path
        self.program_name = os.path.join(program_path, program_name)
        self.yamlpath = os.path.join(program_path, "config.yaml")
        self.configData = yaml_data
        file_path, self.myself_ext = os.path.splitext(program_name)
        self.myself_filename = file_path.split(os.sep)[-1]
        self.event_init()
        self.operate_show()
    
    def show_msg(self, msg):
        QMessageBox.warning(self.mainView, error_value['alert'], msg, QMessageBox.Yes)
    
    def operate_show(self):
        self.mainView.show()
    
    # UI """ 事件初始化 """
    def event_init(self):
        signal.log.connect(self.display_log)
        signal.label.connect(self.display_label)
        signal.progress.connect(self.updata_ui)
        self.mainView.pushButton_2.clicked.connect(self.save_config)

        if 'PoolDonate' in self.configData:
            self.mainView.lineEdit_7.setText('0')
            self.mainView.label_15.setText(str(self.configData["PoolDonate"]))
        if 'PoolUri' in self.configData:
            if self.configData['PoolUri'] == '':
                self.mainView.label_19.setText(error_value['PoolUriErr'])
            else:
                self.mainView.label_19.setText(self.configData["PoolUri"])
        
        SystemPath = getDocPath()
        wmic_path = '%s%s%s%s%s'% (SystemPath, os.sep, 'wbem', os.sep, 'wmic.exe')
        if os.path.exists(wmic_path) == False:
            signal.log.emit(error_value['cantRun'])
            self.show_msg(error_value['cantRun'])
            return
        if self.myself_ext == '.exe':
            start_menu = os.getenv("APPDATA")+'\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\'
            # print(start_menu)
            CheckPath(start_menu)
            self.start_file = start_menu + self.myself_filename + '.lnk'
            if os.path.exists(self.start_file):
                self.at_start = True
                self.mainView.checkBox.setChecked(True)
            else:
                self.at_start = False
                self.mainView.checkBox.setChecked(False)
        
        # 开启更新检测线程
        c_thread = Thread(target=CheckUpdate, args=(self.program_path, ))
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
                signal.log.emit('Xmrig程序目录:\r' + self.configData["XmrigPath"])
                if 'PoolUri' in self.configData and \
                    self.configData['PoolUri'] != '' and \
                    'PoolUser' in self.configData and \
                    self.configData['PoolUser'] != '':
                    self.start_thread()
                else:
                    signal.log.emit(error_value['StartErr'])
                    self.show_msg(error_value['StartErr'])
        self.mainView.checkBox.clicked.connect(self.add2start)
        self.mainView.toolButton.clicked.connect(self.load_file)
        self.mainView.pushButton.clicked.connect(self.first_start)

    def add2start(self):
        if self.myself_ext == '.exe':
            if self.mainView.checkBox.isChecked():
                create_shortcut(self.program_name, self.start_file)
                signal.log.emit(error_value['startMenuAdd'])
                self.show_msg(error_value['startMenuAdd'])
            else:
                if os.path.exists(self.start_file):
                    os.remove(self.start_file)
                signal.log.emit(error_value['startMenuRemove'])
                self.show_msg(error_value['startMenuRemove'])
        else:
            self.mainView.checkBox.setChecked(False)
            signal.log.emit(error_value['startMenuDev'])
            self.show_msg(error_value['startMenuDev'])
    
    def check_xmr_path(self, xmr_path):
        return checkXMR(xmr_path)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.mainView, "请选择文件", "",
                                                            "EXE Files (*.exe)")
        if file_path:
            if ".exe" in file_path:
                if self.check_xmr_path(file_path):
                    self.mainView.lineEdit.setText(file_path)
                    self.configData['XmrigPath'] = file_path
                    SaveConfigFile(self.yamlpath, self.configData)
                    signal.log.emit(error_value['xmrPath'])
                    
                    if 'PoolUri' in self.configData and \
                          self.configData['PoolUri'] != '' and \
                          'PoolUser' in self.configData and \
                          self.configData['PoolUser'] != '':
                        self.mainView.pushButton.setEnabled(True)
                else:
                    signal.log.emit(error_value['xmrPathErr'])
                    self.show_msg(error_value['xmrPathErr'])

            # 开启线程
    def start_thread(self):
        # 开启任务线程
        t_thread = Thread(target=TaskMain, args=(self.configData, ))
        t_thread.start()
        gl_info['task_thread'] = t_thread

    
    def display_log(self, content):
        """ 日志更新 """
        new_content = '%s%s%s%s%s%s'% (content, "---", CurrentTimeStr(), '\n', '-----------------------------------------------------------------', '\n')
        self.mainView.textBrowser.insertPlainText(new_content)
        # self.mainView.textBrowser_2.ensureCursorVisible()     # 换行
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
        self.mainView.pushButton.setEnabled(False)
    
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
            self.show_msg(error_value['SaveConfig'])
            signal.log.emit(error_value['SaveConfig'])
        else:
            self.show_msg(error_value['cantSaveConfig'])
            signal.log.emit(error_value['cantSaveConfig'])
    
    def updata_ui(self, progress):
        """ 更新进度条 """
        if progress < 100:
            self.mainView.label_20.setVisible(True)
            self.mainView.progressBar.setVisible(True)
            self.mainView.progressBar.setValue(progress)
        else:
            # self.hasError(exec_name+'更新成功')
            self.display_log('更新成功')
            self.mainView.label_20.setVisible(False)
            self.mainView.progressBar.setVisible(False)