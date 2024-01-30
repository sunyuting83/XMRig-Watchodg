# -*- coding: utf-8 -*-
import threading

gl_info = {
    'task_thread': None,
    'check_thread': None
}

gl_thread_lock = threading.Lock()       # 全局锁
gl_thread_event = threading.Event()

version:str = 'v1.0.1'

DEV = False