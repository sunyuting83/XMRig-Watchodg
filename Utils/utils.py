# -*- coding: utf-8 -*-
import subprocess
import os
import time
import datetime
import ctypes.wintypes
import inspect
from win32com.client import Dispatch

import yaml

def SaveConfigFile(config_path, desired_caps):
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(desired_caps, f)

def ReadConfigFile(config_path):
    yamlFile = open(config_path,'r',encoding='utf-8')
    # 解析yaml文件
    yamlData = yaml.load(yamlFile, Loader=yaml.FullLoader)
    return yamlData

def CheckConfigFile(config_path):
    desired_caps = {}
    desired_caps["XmrigPath"] = ""
    desired_caps['PoolUri'] = ""
    desired_caps['PoolUser'] = ""
    desired_caps['PoolPass'] = ""
    desired_caps['PoolTLS'] = True
    desired_caps['PoolTLSFingerprint'] = ""
    desired_caps['PoolSocks5'] = ""
    desired_caps['PoolDonate'] = 0
    if os.path.exists(config_path) == False:
        print("yamlfile none")
        SaveConfigFile(config_path, desired_caps)
    yamlData = ReadConfigFile(config_path)
    
    if yamlData == None:
        print("yamlData none")
        SaveConfigFile(config_path, desired_caps)
        yamlData = ReadConfigFile(config_path)
    else:
        if 'XmrigPath' not in yamlData:
            print("XmrigPath none")
            yamlData["XmrigPath"] = ""
        if 'PoolUri' not in yamlData:
            yamlData["PoolUri"] = ""
        if 'PoolUser' not in yamlData:
            yamlData["PoolUser"] = ""
        if 'PoolPass' not in yamlData:
            yamlData["PoolPass"] = ""
        if 'PoolTLS' not in yamlData:
            yamlData["PoolTLS"] = True
        if 'PoolTLSFingerprint' not in yamlData:
            yamlData["PoolTLSFingerprint"] = ""
        if 'PoolSocks5' not in yamlData:
            yamlData["PoolSocks5"] = ""
        if 'PoolDonate' not in yamlData:
            yamlData["PoolDonate"] = 0
        SaveConfigFile(config_path, yamlData)
        yamlData = ReadConfigFile(config_path)
    return yamlData


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    try:
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
        # """if it returns a number greater than one, you're in trouble, 
        # and you should call it again with exc=NULL to revert the effect""" 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    except WindowsError:
        # print("错误信息")
        # print(e)
        raise

def stop_thread(tid):
    # print(tid)
    # print('开始停止')
    if tid != None:
        # print('线程存在')
        if tid.is_alive():
            # print('线程运行中')
            _async_raise(tid.ident, SystemExit)

def getDocPath(pathID=37):
    '''path=5: My Documents'''
    buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, pathID, None, 0, buf)
    return buf.value

def RunCommand(command):
    try:
        child = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, encoding="GBK")
        code = child.wait()
        return code
    except:
        time.sleep(0.5)
        RunCommand(command)


def BuckupCommand(command):
    try:
        child = subprocess.check_output(command, universal_newlines=True, shell=True, encoding="GBK", timeout= 60 * 10)
        return child
    except:
        return None


def checkFirst(appName, dev = False):
    pid_number = 1
    SystemPath = getDocPath()
    command = SystemPath+'''\\wbem\\wmic process where "name like '%%'''+appName+'''%%'" get ProcessId'''
    # print(command)
    # print(pid_number)
    child = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, encoding="GBK")
    child.wait()
    pidList = child.stdout.readlines()
    PID = []
    for item in pidList:
        www = item.strip()
        if len(www) != 0:
            if "ProcessId" not in www:
                PID.append(www)
    if dev:
        pid_number = 4
    # print(len(PID))
    # time.sleep(15)
    if len(PID) <= pid_number:
        return True
    else:
        return False

def checkRunning(appName):
    SystemPath = getDocPath()
    command = SystemPath+'''\\wbem\\wmic process where "name like '%%'''+appName+'''%%'" get ProcessId'''
    # print(command)
    # print(pid_number)
    child = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, encoding="GBK")
    child.wait()
    pidList = child.stdout.readlines()
    PID = []
    for item in pidList:
        www = item.strip()
        if len(www) != 0:
            if "ProcessId" not in www:
                # print(www)
                PID.append(www)
    # time.sleep(15)
    if len(PID) >= 1:
        return PID[0], PID
    else:
        return 0, PID

def CheckPath(p):
    if os.path.exists(p) == False:
        os.mkdir(p)

def Str2Time(timestr):
    date01 = datetime.date.today().strftime('%Y-%m-%d')
    tstr = date01+' '+timestr
    dateTime = datetime.datetime.strptime(tstr,'%Y-%m-%d %H:%M:%S')
    return dateTime

def CurrentTime():
    return datetime.datetime.now().replace(microsecond=0)

def CurrentTimeWithoutSecond():
    return datetime.datetime.now().replace(second=0, microsecond=0)
def CurrentNewTimeWithoutSecond():
    current_datetime = datetime.datetime.now()
    newtime = current_datetime + datetime.timedelta(minutes=10)
    return newtime.replace(second=0, microsecond=0)

def CurrentTimeStr():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def KillPid(pid, exec_name):
    try:
        process = 'taskkill /f /pid %s'%pid
        subprocess.Popen(process, universal_newlines=True, shell=True, stdout=subprocess.PIPE, encoding="GBK")
        while True:
            PID, _ = checkRunning(exec_name)
            if PID == 0:
                break
    except WindowsError:
        raise

def KillPidDontCheck(pid):
    try:
        process = 'taskkill /f /pid %s'%pid
        subprocess.Popen(process, universal_newlines=True, shell=True, stdout=subprocess.PIPE, encoding="GBK")
    except WindowsError:
        raise

def KillExecName(exec_name):
    try:
        process = 'taskkill /f /t /im %s'%exec_name
        subprocess.Popen(process, universal_newlines=True, shell=True, stdout=subprocess.PIPE, encoding="GBK")
        time.sleep(0.2)
        while True:
            PID, _ = checkRunning(exec_name)
            if PID == 0:
                break
    except Exception:
        return

def KillExecNameDontCheck(exec_name):
    try:
        process = 'taskkill /f /t /im %s'%exec_name
        subprocess.Popen(process, universal_newlines=True, shell=True, stdout=subprocess.PIPE, encoding="GBK")
    except Exception as e:
        print(e)
        return


def compareVersion(version1, version2):
    """
    用split划分 转换为int 比较即可
    :type version1: str
    :type version2: str
    :rtype: int
    """
    if 'v' in version1.lower():
        version1 = version1.lower().split("v")[1]
    if 'v' in version2.lower():
        version2 = version2.lower().split("v")[1]
    com1 = version1.split(".")
    com2 = version2.split(".")
    if len(com1) != len(com2):
        if len(com1) > len(com2):
            for i in range(len(com2)):
                if int(com1[i]) > int(com2[i]):
                    return 1
                elif int(com1[i]) < int(com2[i]):
                    return -1
            for i in range(len(com2), len(com1)):
                if int(com1[i]) != 0:
                    return 1
            return 0
        else:
            for i in range(len(com1)):
                if int(com1[i]) > int(com2[i]):
                    return 1
                elif int(com1[i]) < int(com2[i]):
                    return -1
            for i in range(len(com1), len(com2)):
                if int(com2[i]) != 0:
                    return -1
            return 0
    for i in range(len(com1)):
        if int(com1[i]) > int(com2[i]):
            return 1
        elif int(com1[i]) < int(com2[i]):
            return -1
        else:
            continue
    return 0

def checkXMR(xmr_path):
    try:
        status = False
        if os.path.exists(xmr_path) == False:
            return status
        command = '%s%s'% (xmr_path, ' --version')
        child = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, encoding="GBK")
        child.wait()
        List = child.stdout.readlines()
        for item in List:
            www = item.strip()
            if len(www) != 0:
                if "XMRig" in www:
                    status = True
        return status
    except:
        return False


def create_shortcut(target_path :str, shortcut_path: str):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target_path
    shortcut.Save()

def make_even_num(num):
    num_list = []
    for i in range(num):
        if i % 2 == 0:
            num_list.append(i)
    return num_list

if __name__ == '__main__':
	print(compareVersion('v1.0.1', 'v1.0.1'))

