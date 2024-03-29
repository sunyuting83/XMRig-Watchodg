import os
import subprocess
from public import version, gl_thread_lock, gl_thread_event
from Utils.httpServer import HttpGet
from Utils.utils import compareVersion, CheckPath, stop_thread, KillExecNameDontCheck
from Utils.download import DownloadFile
from UI.view import setLog
from public import gl_info

class CheckUpdate:
    def __init__(self, program_path, my_self_name, xmrigName, language_data):
        super().__init__()
        self.program_path = program_path
        self.language_data = language_data
        self.my_self_name = my_self_name
        self.xmrig_name = xmrigName
        if self.xmrig_name == '':
            self.xmrig_name = 'xmrig.exe'
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
        setLog(self.language_data['Updating'])
        TemPath = os.path.join(self.program_path, 'tmp')
        CheckPath(TemPath)
        TemFilePath = os.path.join(TemPath, 'XMRigWatchdog.zip')
        DownloadFile(DownUri, TemFilePath, self.language_data)
        setLog(self.language_data['SoftwareUpdateCompleted'])
        command = os.path.join(self.program_path, 'update.exe')
        command = '%s --appname %s --xmrname %s'% (command, self.my_self_name, self.xmrig_name)
        subprocess.run(f'start {command}', shell=True)
        
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