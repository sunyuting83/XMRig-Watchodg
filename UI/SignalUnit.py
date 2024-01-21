# -*-coding:utf-8 -*-
from PyQt5.QtCore import QObject, pyqtSignal


class SignalUnit(QObject):
    # 调试日志
    log = pyqtSignal(str)
    label = pyqtSignal(str, str)
    progress = pyqtSignal(int)
    UpdateUI = pyqtSignal()


signal = SignalUnit()