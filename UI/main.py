# -*- coding: utf-8 -*-
import time
from .MainWin import Ui_MainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from public import gl_info, gl_thread_event
from Utils.utils import stop_thread, KillExecNameDontCheck

class MainView(Ui_MainWindow,QWidget):
    def __init__(self):
        super(MainView,self).__init__()
        self.setupUi(self)
        # self.retranslateUi(self)
        self.ui_init()

    # 界面窗口关闭信号
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        # self.StopThread()
        gl_thread_event.set()
        if gl_info['check_thread'] != None:
            stop_thread(gl_info['check_thread'])
        if gl_info['task_thread'] != None:
            stop_thread(gl_info['task_thread'])
        KillExecNameDontCheck('xmrig.exe')
        a0.accept()
        

    def ui_init(self):
        self.pushButton.setEnabled(False)
        self.label_20.setVisible(False)
        self.progressBar.setVisible(False)
