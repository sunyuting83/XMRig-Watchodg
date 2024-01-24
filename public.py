# -*- coding: utf-8 -*-
import threading

gl_info = {
    'task_thread': None,
    'check_thread': None
}

gl_thread_lock = threading.Lock()       # 全局锁
gl_thread_event = threading.Event()

version:str = 'v0.0.5'

DEV = False

error_value = {
    'alert': '温馨提示',
    'cantRun': '当前windows系统不支持本软件，请使用说明中推荐的系统',
    'PoolUriErr': '尚未设置',
    'startMenuAdd': '添加开机启动成功',
    'startMenuRemove': '取消开机启动成功',
    'startMenuDev': '开发版没有本功能',
    'xmrPath': 'XMRig位置保存到配置文件',
    'xmrPathErr': 'XMRig位置选择错误',
    'cantSaveConfig': '钱包地址或矿池地址不能为空',
    'SaveConfig': '保存配置成功，请点击首次运行',
    'StartErr': '矿池地址或钱包地址尚未设置，请先设置后再点击首次运行',
    'XmrConfig': 'XMR配置文件写入成功',
    'XmrStatus1': '启动中',
    'XmrStatus2': '发生错误',
    'XmrStatus3': '运行中',
    'XmrStatus4': '矿池验证错误，请检查配置',
}