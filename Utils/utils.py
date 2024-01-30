# -*- coding: utf-8 -*-
import subprocess
import os
import time
import datetime
import ctypes.wintypes
import inspect
import locale
from win32com.client import Dispatch

import yaml

def get_language():
    local_language = locale.getdefaultlocale()[0]
    language = 'zh_CN'
    if 'zh' in local_language:
        language = 'zh_CN'
    if 'en' in local_language:
        language = 'en'
    return language

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
    desired_caps['Language'] = "en"
    if os.path.exists(config_path) == False:
        SaveConfigFile(config_path, desired_caps)
    yamlData = ReadConfigFile(config_path)
    
    if yamlData == None:
        SaveConfigFile(config_path, desired_caps)
        yamlData = ReadConfigFile(config_path)
    else:
        if 'XmrigPath' not in yamlData:
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
        if 'Language' not in yamlData:
            yamlData["Language"] = "en"
        SaveConfigFile(config_path, yamlData)
        yamlData = ReadConfigFile(config_path)
    return yamlData

def CheckLanguageFile(yaml_path):
    programPath = os.path.dirname(yaml_path)
    CheckPath(programPath)
    
    desired_caps = {}
    desired_caps['zh_CN'] = {}
    desired_caps['zh_CN']['Title'] = 'XMRig监工'
    desired_caps['zh_CN']['BasicSettings'] = '基础设置'
    desired_caps['zh_CN']['XmrigPath'] = 'XMRIG目录:'
    desired_caps['zh_CN']['AutomaticallyAtStartup'] = '开机自启'
    desired_caps['zh_CN']['Language'] = '界面语言:'
    desired_caps['zh_CN']['PoolSettings'] = '矿池设置'
    desired_caps['zh_CN']['PoolUrl'] = '矿池地址:'
    desired_caps['zh_CN']['WalletAddress'] = '钱包地址:'
    desired_caps['zh_CN']['EnableTls'] = '开启TLS'
    desired_caps['zh_CN']['Socks5Url'] = '代理地址:'
    desired_caps['zh_CN']['TlsFingerprint'] = 'TLS秘钥:'
    desired_caps['zh_CN']['Donate'] = '抽水:'
    desired_caps['zh_CN']['FirstRun'] = '首次启动'
    desired_caps['zh_CN']['Save'] = '保存设置'
    desired_caps['zh_CN']['Status'] = '运行状态'
    desired_caps['zh_CN']['Setup'] = '设置'
    desired_caps['zh_CN']['Log'] = '日志'
    desired_caps['zh_CN']['NotYetAcquired'] = '未获取'
    desired_caps['zh_CN']['LastSpeed'] = '最后测速:'
    desired_caps['zh_CN']['HugePages'] = 'HUGE PAGES:'
    desired_caps['zh_CN']['1gbPages'] = '1GB PAGES:'
    desired_caps['zh_CN']['Cpu'] = 'CPU:'
    desired_caps['zh_CN']['Memory'] = '内存'
    desired_caps['zh_CN']['MotherBoard'] = '主板:'
    desired_caps['zh_CN']['Updating'] = '更新中'
    desired_caps['zh_CN']['UpdateSuccess'] = '更新成功'
    desired_caps['zh_CN']['WorkerName'] = '矿工名称'
    desired_caps['zh_CN']['Test01'] = '测试矿工'
    desired_caps['zh_CN']['SelectAFile'] = '请选择文件'
    desired_caps['zh_CN']['Select'] = '选择'
    desired_caps['zh_CN']['DownloadTime'] = '下载用时'
    desired_caps['zh_CN']['SoftwareUpdateCompleted'] = '软件更新已完成,程序将在1秒后自动关闭。'
    desired_caps['zh_CN']['Alert'] = '温馨提示'
    desired_caps['zh_CN']['CantRun'] = '当前windows系统不支持本软件,请使用说明中推荐的系统'
    desired_caps['zh_CN']['PoolUriErr'] = '尚未设置'
    desired_caps['zh_CN']['StartMenuAdd'] = '添加开机启动成功'
    desired_caps['zh_CN']['StartMenuRemove'] = '取消开机启动成功'
    desired_caps['zh_CN']['StartMenuDev'] = '开发版没有本功能'
    desired_caps['zh_CN']['XmrPath'] = 'XMRig位置保存到配置文件'
    desired_caps['zh_CN']['XmrPathErr'] = 'XMRig位置选择错误'
    desired_caps['zh_CN']['CantSaveConfig'] = '钱包地址或矿池地址不能为空'
    desired_caps['zh_CN']['SaveConfig'] = '保存配置成功，请点击首次运行'
    desired_caps['zh_CN']['StartErr'] = '矿池地址或钱包地址尚未设置，请先设置后再点击首次运行'
    desired_caps['zh_CN']['XmrConfig'] = 'XMR配置文件写入成功'
    desired_caps['zh_CN']['XmrStatus1'] = '启动中'
    desired_caps['zh_CN']['XmrStatus2'] = '发生错误'
    desired_caps['zh_CN']['XmrStatus3'] = '运行中'
    desired_caps['zh_CN']['XmrStatus4'] = '矿池验证错误，请检查配置'
    desired_caps['zh_CN']['XmrStatus5'] = '未运行'

    
    desired_caps['en'] = {}
    desired_caps['en']['Title'] = 'XMRig Watchdog'
    desired_caps['en']['BasicSettings'] = 'Basic Settings'
    desired_caps['en']['XmrigPath'] = 'XMRIG Path:'
    desired_caps['en']['AutomaticallyAtStartup'] = 'Automatically at startup'
    desired_caps['en']['Language'] = 'Language:'
    desired_caps['en']['PoolSettings'] = 'Pool Settings'
    desired_caps['en']['PoolUrl'] = 'Pool URL:'
    desired_caps['en']['WalletAddress'] = 'Wallet address:'
    desired_caps['en']['WorkerName'] = 'Worker name:'
    desired_caps['en']['EnableTls'] = 'Enable TLS'
    desired_caps['en']['Socks5Url'] = 'Socks5 URL:'
    desired_caps['en']['TlsFingerprint'] = 'TLS-fingerprint:'
    desired_caps['en']['Donate'] = 'donate:'
    desired_caps['en']['FirstRun'] = 'First Run'
    desired_caps['en']['Save'] = 'Save'
    desired_caps['en']['Status'] = 'Status'
    desired_caps['en']['Setup'] = 'Setup'
    desired_caps['en']['Log'] = 'Log'
    desired_caps['en']['NotYetAcquired'] = 'Not yet acquired'
    desired_caps['en']['LastSpeed'] = 'Last speed:'
    desired_caps['en']['HugePages'] = 'HUGE PAGES:'
    desired_caps['en']['1gbPages'] = '1GB PAGES:'
    desired_caps['en']['Cpu'] = 'CPU:'
    desired_caps['en']['Memory'] = 'MEMORY:'
    desired_caps['en']['MotherBoard'] = 'Mother Board:'
    desired_caps['en']['Updating'] = 'Updating'
    desired_caps['en']['UpdateSuccess'] = 'Update success'
    desired_caps['en']['Test01'] = 'test01'
    desired_caps['en']['SelectAFile'] = 'Select a file'
    desired_caps['en']['Select'] = 'Select'
    desired_caps['en']['DownloadTime'] = 'Download time'
    desired_caps['en']['SoftwareUpdateCompleted'] = 'Software update completed, program will automatically close in 1 second.'
    desired_caps['en']['Alert'] = 'Warm Prompt'
    desired_caps['en']['CantRun'] = 'This software is not supported on the current Windows system, please use the recommended system in the instructions'
    desired_caps['en']['PoolUriErr'] = 'Not yet set'
    desired_caps['en']['StartMenuAdd'] = 'Successfully added to startup'
    desired_caps['en']['StartMenuRemove'] = 'Successfully cancelled startup'
    desired_caps['en']['StartMenuDev'] = 'No such feature in the development version'
    desired_caps['en']['XmrPath'] = 'XMRig location saved to configuration file'
    desired_caps['en']['XmrPathErr'] = 'Error in selecting XMRig location'
    desired_caps['en']['CantSaveConfig'] = 'Wallet address or pool address cannot be empty'
    desired_caps['en']['SaveConfig'] = 'Configuration saved successfully, please click First Run'
    desired_caps['en']['StartErr'] = 'Pool address or wallet address not set, please set them first then click First Run'
    desired_caps['en']['XmrConfig'] = 'XMR configuration file written successfully'
    desired_caps['en']['XmrStatus1'] = 'Starting'
    desired_caps['en']['XmrStatus2'] = 'An error occurred'
    desired_caps['en']['XmrStatus3'] = 'Running'
    desired_caps['en']['XmrStatus4'] = 'Pool verification error, please check the configuration'
    desired_caps['en']['XmrStatus5'] = 'Not already'

    desired_caps['LanguageList'] = []
    desired_caps1 = {}
    desired_caps1['Language'] = '简体中文'
    desired_caps1['Code'] = 'zh_CN'
    desired_caps['LanguageList'].append(desired_caps1)
    desired_caps2 = {}
    desired_caps2['Language'] = 'English'
    desired_caps2['Code'] = 'en'
    desired_caps['LanguageList'].append(desired_caps2)
    
    if os.path.exists(yaml_path) == False:
        SaveConfigFile(yaml_path, desired_caps)
    yamlData = ReadConfigFile(yaml_path)
    
    if yamlData == None:
        SaveConfigFile(yaml_path, desired_caps)
        yamlData = ReadConfigFile(yaml_path)
    return yamlData


def _async_raise(tid, exctype):
    # print(tid)
    """raises the exception, performs cleanup if needed"""
    try:
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            pass
        elif res != 1:
        # """if it returns a number greater than one, you're in trouble, 
        # and you should call it again with exc=NULL to revert the effect""" 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            # raise SystemError("PyThreadState_SetAsyncExc failed")
    except:
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

def checkFirst(appName, dev = False):
    pid_number = 1
    SystemPath = getDocPath()
    wbem_path = '%s\\wbem\\'% (SystemPath)
    hasWmic = os.path.exists(wbem_path)
    pidList = []
    command = "tasklist /fo csv /nh"
    if hasWmic:
        command = wbem_path+'''wmic process where "name like '%%'''+appName+'''%%'" get ProcessId'''   
        child = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, encoding="GBK")
        child.wait()
        pidList = child.stdout.readlines()
    else:
        child = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, encoding="GBK")
        output, _ = child.communicate()
        pidList = output.split('\n')
    
    PID = []
    for item in pidList:
        www = item.strip()
        if len(www) != 0:
            if hasWmic:
                if "ProcessId" not in www:
                    PID.append(www)
            else:
                if appName in www:
                    PID.append(www)
    if dev:
        pid_number = 4
    # print(len(PID))
    # time.sleep(15)
    # print(PID)
    if len(PID) <= pid_number:
        return True
    else:
        return False

def checkRunning(appName):
    SystemPath = getDocPath()
    wbem_path = '%s\\wbem\\'% (SystemPath)
    hasWmic = os.path.exists(wbem_path)
    pidList = []
    command = "tasklist /fo csv /nh"
    if hasWmic:
        command = wbem_path+'''wmic process where "name like '%%'''+appName+'''%%'" get ProcessId'''   
        child = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, encoding="GBK")
        child.wait()
        pidList = child.stdout.readlines()
    else:
        child = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, encoding="GBK")
        output, _ = child.communicate()
        pidList = output.split('\n')
    PID = []
    for item in pidList:
        www = item.strip()
        if len(www) != 0:
            if hasWmic:
                if "ProcessId" not in www:
                    PID.append(int(www))
            else:
                if appName in www:
                    pid = int(www.split(',')[1].replace('"', ''))
                    PID.append(pid)
    # time.sleep(15)
    if len(PID) >= 1:
        return PID[0], PID
    else:
        return 0, PID

def CheckPath(p):
    if os.path.exists(p) == False:
        os.mkdir(p)

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
            else:
                KillExecNameDontCheck(exec_name)
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

# if __name__ == '__main__':
# 	print(compareVersion('v1.0.1', 'v1.0.1'))

