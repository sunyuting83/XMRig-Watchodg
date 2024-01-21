import os
from public import version, gl_thread_lock, gl_thread_event
from Utils.httpServer import HttpGet
from Utils.utils import compareVersion, CheckPath
from Utils.download import DownloadFile
from UI.view import setLog

class CheckUpdate:
    def __init__(self, program_path):
        super().__init__()
        self.program_path = program_path
        self.event = gl_thread_event
        self.start_check()
    
    def start_check(self):
        while not self.event.is_set():
            # print("start update")
            if version != None:
                status, downuri = self.check_version(version)
                # print(status, downuri)
                if status:
                    self.UpdateExec(downuri)
            self.event.wait(3600) #3600
    
    def UpdateExec(self, DownUri):
        # print('辅助更新中')
        setLog("辅助更新中……")
        TemPath = os.path.join(self.program_path, 'tmp')
        CheckPath(TemPath)
        TemFilePath = os.path.join(self.program_path, 'XMRigWatchdog.exe')
        DownloadFile(DownUri, TemFilePath)
        # 交给update.exe去处理
    
    def check_version(self, version):
        uri = "https://version.switch8.top/GetVersion?project_id=ce3d4cc65628c223b15a23902371c7b7"
        status = False
        downuri = None
        st = 2
        while st >= 0:
            st = st -1
            data = HttpGet(uri)
            print(data)
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