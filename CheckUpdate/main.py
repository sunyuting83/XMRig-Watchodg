import os
import subprocess
from public import version, gl_thread_lock, gl_thread_event
from Utils.httpServer import HttpGet
from Utils.utils import compareVersion, CheckPath, stop_thread, KillExecNameDontCheck
from Utils.download import DownloadFile
from UI.view import setLog
from public import gl_info

class CheckUpdate:
    def __init__(self, program_path, my_self_name, xmrigName):
        super().__init__()
        self.program_path = program_path
        self.my_self_name = my_self_name
        self.xmrig_name = xmrigName
        self.event = gl_thread_event
        self.start_check()
    
    def start_check(self):
        while not self.event.is_set():
            # print("start update")
            if version != None:
                status, downuri = self.check_version(version)
                # print(status, downuri)
                if status:
                    if gl_info['task_thread'] != None:
                        gl_thread_lock.acquire()
                        stop_thread(gl_info['task_thread'])
                        KillExecNameDontCheck('xmrig.exe')
                        gl_thread_lock.release()
                    self.UpdateExec(downuri)
            self.event.wait(3600) #3600
    
    def UpdateExec(self, DownUri):
        # print('辅助更新中')
        setLog("软件更新中……")
        TemPath = os.path.join(self.program_path, 'tmp')
        CheckPath(TemPath)
        TemFilePath = os.path.join(TemPath, 'XMRigWatchdog.zip')
        DownloadFile(DownUri, TemFilePath)
        setLog("软件更新中结束,1秒后程序自动关闭")
        
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        # command = os.path.join(self.program_path, 'update.exe')
        program = os.path.join(self.program_path, 'update.exe')
        args = [program, "--appname=XMRigWatchdog.exe", "--xmrname=xmrig.exe"]
        # command = '%s --appname %s --xmrname %s'% (command, self.my_self_name, self.xmrig_name)
        os.spawnv(os.P_NOWAIT, program, args)
        
        self.event.wait(1)
        KillExecNameDontCheck(self.my_self_name)
        # print('下载完成')
        # 交给update.exe去处理
    
    def check_version(self, version):
        uri = "https://version.switch8.top/GetVersion?project_id=ce3d4cc65628c223b15a23902371c7b7"
        status = False
        downuri = None
        st = 2
        while st >= 0:
            st = st -1
            data = HttpGet(uri)
            # print(data)
            if 'status' in data and data['status'] == 0:
                # print('成功获取')
                web_version = data['version']
                if compareVersion(version, web_version) == -1:
                    downuri = data['download_url']
                    status = True
                break
            else:
                self.event.wait(15)
        return status, downuri