# -*- coding: utf-8 -*-
import os
import subprocess
import json
from Utils.utils import make_even_num, KillPid, checkRunning
from public import gl_info, gl_thread_lock, gl_thread_event, DEV, error_value
from UI.view import setLog, setLabel

class TaskMain:
    def __init__(self, config_data):
        super().__init__()
        self.config_data = config_data
        self.event = gl_thread_event
        xmr_path = os.path.abspath(os.path.dirname(config_data['XmrigPath']))
        self.config_path = os.path.join(xmr_path,'config.json')
        self.run_exec = '%s -c %s'% (config_data['XmrigPath'], self.config_path)
        self.Exec_PID = None
        self.Status = False
        
        if DEV:
            self.rx0 = [0, 2]
        else:
            cpu_count = os.cpu_count()
            self.rx0 = make_even_num(cpu_count)
        self.check_config()
        self.start()
    
    def check_config(self):
        json_data = '''{"api":{"id":null,"worker-id":null},"http":{"enabled":false,"host":"127.0.0.1","port":0,"access-token":null,"restricted":true},"autosave":true,"background":false,"colors":true,"title":true,"randomx":{"init":-1,"init-avx2":-1,"mode":"auto","1gb-pages":true,"rdmsr":true,"wrmsr":true,"cache_qos":false,"numa":true,"scratchpad_prefetch_mode":1},"cpu":{"enabled":true,"huge-pages":true,"huge-pages-jit":true,"hw-aes":null,"priority":null,"memory-pool":false,"yield":true,"asm":true,"argon2-impl":null,"argon2":[0,20,1,21,2,22,3,23,4,24,5,25,6,26,7,27,8,28,9,29,10,30,11,31,12,32,13,33,14,34,15,35,16,36,17,37,18,38,19,39],"cn":[[1,0],[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,27],[1,28],[1,29],[1,10],[1,11],[1,12],[1,13],[1,14],[1,15],[1,16],[1,17],[1,18],[1,19],[1,37],[1,38],[1,39]],"cn-heavy":[[1,0],[1,1],[1,2],[1,3],[1,4],[1,5],[1,10],[1,11],[1,12],[1,13],[1,14],[1,15]],"cn-lite":[[1,0],[1,20],[1,1],[1,21],[1,2],[1,22],[1,3],[1,23],[1,4],[1,24],[1,5],[1,25],[1,6],[1,26],[1,7],[1,27],[1,8],[1,28],[1,9],[1,29],[1,10],[1,30],[1,11],[1,31],[1,12],[1,32],[1,13],[1,33],[1,14],[1,34],[1,15],[1,35],[1,16],[1,36],[1,17],[1,37],[1,18],[1,38],[1,19],[1,39]],"cn-pico":[[2,0],[2,20],[2,1],[2,21],[2,2],[2,22],[2,3],[2,23],[2,4],[2,24],[2,5],[2,25],[2,6],[2,26],[2,7],[2,27],[2,8],[2,28],[2,9],[2,29],[2,10],[2,30],[2,11],[2,31],[2,12],[2,32],[2,13],[2,33],[2,14],[2,34],[2,15],[2,35],[2,16],[2,36],[2,17],[2,37],[2,18],[2,38],[2,19],[2,39]],"cn/upx2":[[2,0],[2,20],[2,1],[2,21],[2,2],[2,22],[2,3],[2,23],[2,4],[2,24],[2,5],[2,25],[2,6],[2,26],[2,7],[2,27],[2,8],[2,28],[2,9],[2,29],[2,10],[2,30],[2,11],[2,31],[2,12],[2,32],[2,13],[2,33],[2,14],[2,34],[2,15],[2,35],[2,16],[2,36],[2,17],[2,37],[2,18],[2,38],[2,19],[2,39]],"ghostrider":[[8,0],[8,2],[8,4],[8,6],[8,8],[8,10],[8,12],[8,14],[8,16],[8,18],[8,20],[8,22],[8,24],[8,26],[8,28],[8,30],[8,32],[8,34],[8,36],[8,38]],"rx":[],"rx/wow":[0,20,1,21,2,22,3,23,4,24,5,25,6,26,7,27,8,28,9,29,10,30,11,31,12,32,13,33,14,34,15,35,16,36,17,37,18,38,19,39],"cn-lite/0":false,"cn/0":false,"rx/arq":"rx/wow","rx/keva":"rx/wow"},"opencl":{"enabled":false,"cache":true,"loader":null,"platform":"AMD","adl":true,"cn-lite/0":false,"cn/0":false},"cuda":{"enabled":false,"loader":null,"nvml":true,"cn-lite/0":false,"cn/0":false},"log-file":null,"donate-level":0,"donate-over-proxy":1,"pools":[{"algo":"rx/0","coin":null,"url":"","user":"","pass":"","rig-id":null,"nicehash":false,"keepalive":false,"enabled":true,"tls":false,"sni":false,"tls-fingerprint":null,"daemon":false,"socks5":null,"self-select":null,"submit-to-origin":false}],"retries":5,"retry-pause":5,"print-time":60,"health-print-time":60,"dmi":true,"syslog":false,"tls":{"enabled":false,"protocols":null,"cert":null,"cert_key":null,"ciphers":null,"ciphersuites":null,"dhparam":null},"dns":{"ipv6":false,"ttl":30},"user-agent":null,"verbose":0,"watch":true,"pause-on-battery":false,"pause-on-active":false}'''
        if os.path.exists(self.config_path) == False:
            gl_thread_lock.acquire()
            with open(self.config_path, "w", encoding="utf-8") as json_file:
                json_obj = json.loads(json_data)
                json.dump(json_obj, json_file)
                self.event.wait(0.3)
            gl_thread_lock.release()
        json_file = open(self.config_path,'r',encoding='utf-8')
        json_obj = json.load(json_file)
        if self.config_data['PoolTLSFingerprint'] == '':
            self.config_data['PoolTLSFingerprint'] = None
        if self.config_data['PoolSocks5'] == '':
            self.config_data['PoolSocks5'] = None
        json_obj['cpu']['rx'] = self.rx0
        json_obj['donate-level'] = self.config_data['PoolDonate']
        json_obj['pools'][0]['url'] = self.config_data['PoolUri']
        json_obj['pools'][0]['user'] = self.config_data['PoolUser']
        json_obj['pools'][0]['pass'] = self.config_data['PoolPass']
        json_obj['pools'][0]['tls'] = self.config_data['PoolTLS']
        json_obj['pools'][0]['tls-fingerprint'] = self.config_data['PoolTLSFingerprint']
        json_obj['pools'][0]['socks5'] = self.config_data['PoolSocks5']
        gl_thread_lock.acquire()
        with open(self.config_path, "w", encoding="utf-8") as json_f:
            json.dump(json_obj, json_f)
            self.event.wait(0.3)
        gl_thread_lock.release()
        setLog(error_value['XmrConfig'])
    
    def start(self):
        while True:
            if self.Status == False:
                process = subprocess.Popen(self.run_exec, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, creationflags = subprocess.CREATE_NO_WINDOW)
                pid = process.pid
                gl_thread_lock.acquire()
                self.Status = True
                gl_thread_lock.release()
                hasError = True
                while hasError:
                    for line in iter(process.stdout.readline, b''):
                        line_txt = line.decode('utf-8').strip()
                        # print(line_txt)
                        if 'HUGE' in  line_txt:
                            setLog(error_value['XmrStatus1'])
                            setLabel('status', error_value['XmrStatus1'])
                            setLabel('huge', line_txt.split('   ')[1])
                        if '1GB PAGES' in  line_txt:
                            setLabel('pages', line_txt.split('    ')[1])
                        if 'CPU' in  line_txt:
                            setLabel('cpu', line_txt.split('          ')[1])
                        if 'MEMORY' in  line_txt:
                            setLabel('mem', line_txt.split('       ')[1])
                        if 'MOTHERBOARD' in  line_txt:
                            setLabel('board', line_txt.split('  ')[1])
                        if 'error:' in  line_txt:
                            setLog(error_value['XmrStatus2'])
                            setLabel('status', error_value['XmrStatus2'])
                            KillPid(pid, "xmrig.exe")
                            gl_thread_lock.acquire()
                            self.Status = False
                            gl_thread_lock.release()
                            hasError = False
                            break
                        if 'verify server' in line_txt:
                            setLog(error_value['XmrStatus4'])
                            setLabel('status', error_value['XmrStatus4'])
                            KillPid(pid, "xmrig.exe")
                            gl_thread_lock.acquire()
                            self.Status = False
                            gl_thread_lock.release()
                            hasError = False
                            break
                        if 'miner' in line_txt:
                            line_list = line_txt.split(' ')
                            speed_index = line_list.index('speed')
                            speed_num = line_list[speed_index + 2]
                            setLabel('status', error_value['XmrStatus3'])
                            setLog('最新算力值：' + speed_num + 'H/s')
                            setLabel('speed', speed_num + 'H/s')
                            if '.' in speed_num:
                                speed_num = speed_num.split('.')[0]
                            if int(speed_num) < 100:
                                setLog(error_value['XmrStatus2'])
                                setLabel('status', error_value['XmrStatus2'])
                                KillPid(pid, "xmrig.exe")
                                gl_thread_lock.acquire()
                                self.Status = False
                                gl_thread_lock.release()
                                hasError = False
                                break
                            continue
                    
                    self.event.wait(60)
                    PID, _ = checkRunning('xmrig.exe')
                    if PID == 0:
                        setLog(error_value['XmrStatus2'])
                        setLabel('status', error_value['XmrStatus2'])
                        gl_thread_lock.acquire()
                        self.Status = False
                        gl_thread_lock.release()
                        break

                process.wait()
            self.event.wait(60)