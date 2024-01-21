# -*- coding: utf-8 -*-
from UI.SignalUnit import signal

def setLog(content):
    signal.log.emit(str(content))

def setLabel(lab, content):
    signal.label.emit(lab, str(content))

def UpdateProgress(progress):
    signal.progress.emit(int(progress))

def UpdateUI():
    signal.UpdateUI.emit()