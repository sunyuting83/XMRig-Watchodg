# -*- coding: utf-8 -*-
import os
import re
import subprocess
import json
from Utils.utils import make_even_num, KillPid, checkRunning
from public import gl_thread_lock, gl_thread_event, DEV
from UI.view import setLog, setLabel

class TaskMain:
    def __init__(self, config_data, language_data):
        super().__init__()
        self.config_data = config_data
        self.event = gl_thread_event
        self.language_data = language_data
        xmr_path = os.path.abspath(os.path.dirname(config_data['XmrigPath']))
        self.config_path = os.path.join(xmr_path,'config.json')
        self.run_exec = '%s -c %s'% (config_data['XmrigPath'], self.config_path)
        self.Exec_name = os.path.basename(config_data['XmrigPath'])
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
        json_data = '''{"api":{"id":null,"worker-id":null},"http":{"enabled":false,"host":"127.0.0.1","port":0,"access-token":null,"restricted":true},"autosave":true,"background":false,"colors":true,"title":true,"randomx":{"init":-1,"init-avx2":-1,"mode":"auto","1gb-pages":true,"rdmsr":true,"wrmsr":true,"cache_qos":false,"numa":true,"scratchpad_prefetch_mode":1},"cpu":{"enabled":true,"huge-pages":true,"huge-pages-jit":true,"hw-aes":null,"priority":null,"memory-pool":false,"yield":true,"asm":true,"argon2-impl":null,"rx":[],"cn-lite/0":false,"cn/0":false,"rx/arq":"rx/wow","rx/keva":"rx/wow"},"opencl":{"enabled":false,"cache":true,"loader":null,"platform":"AMD","adl":true,"cn-lite/0":false,"cn/0":false},"cuda":{"enabled":false,"loader":null,"nvml":true,"cn-lite/0":false,"cn/0":false},"log-file":null,"donate-level":0,"donate-over-proxy":1,"pools":[{"algo":"rx/0","coin":null,"url":"","user":"","pass":"","rig-id":null,"nicehash":false,"keepalive":false,"enabled":true,"tls":false,"sni":false,"tls-fingerprint":null,"daemon":false,"socks5":null,"self-select":null,"submit-to-origin":false}],"retries":5,"retry-pause":5,"print-time":60,"health-print-time":60,"dmi":true,"syslog":false,"tls":{"enabled":false,"protocols":null,"cert":null,"cert_key":null,"ciphers":null,"ciphersuites":null,"dhparam":null},"dns":{"ipv6":false,"ttl":30},"user-agent":null,"verbose":0,"watch":true,"pause-on-battery":false,"pause-on-active":false}'''
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
        setLog(self.language_data['XmrConfig'])
    
    def restart(self, message):
        setLog(message)
        setLabel('status', message)
        KillPid(self.Exec_PID, self.Exec_name)
        self.Status = False
        return False
    
    def start(self):
        while True:
            if self.Status == False:
                process = subprocess.Popen(self.run_exec, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, creationflags = subprocess.CREATE_NO_WINDOW)
                self.Exec_PID = process.pid
                self.Status = True
                hasError = True
                while hasError:
                    for line in iter(process.stdout.readline, b''):
                        line_txt = line.decode('utf-8').strip()
                        # print(line_txt)
                        if 'HUGE' in  line_txt:
                            setLog(self.language_data['XmrStatus1'])
                            setLabel('status', self.language_data['XmrStatus1'])
                            setLabel('huge', self.make_value(line_txt))
                        if '1GB PAGES' in  line_txt:
                            setLabel('pages', self.make_value(line_txt))
                        if 'CPU' in  line_txt:
                            setLabel('cpu', self.make_value(line_txt))
                        if 'MEMORY' in  line_txt:
                            setLabel('mem', self.make_value(line_txt))
                        if 'MOTHERBOARD' in  line_txt:
                            setLabel('board', self.make_value(line_txt))
                        if 'DONATE' in  line_txt:
                            setLabel('donate', self.make_value(line_txt))
                        if 'error:' in  line_txt:
                            hasError = self.restart(self.language_data['XmrStatus2'])
                            break
                        if 'verify server' in line_txt:
                            hasError = self.restart(self.language_data['XmrStatus4'])
                            break
                        if 'miner' in line_txt:
                            line_list = line_txt.split(' ')
                            speed_index = line_list.index('speed')
                            speed_num = line_list[speed_index + 2]
                            if 'n/a' in speed_num:
                                hasError = self.restart(self.language_data['XmrStatus2'])
                                break
                            setLabel('status', self.language_data['XmrStatus3'])
                            setLog(self.language_data['LastSpeed'] + speed_num + 'H/s')
                            setLabel('speed', speed_num + 'H/s')
                            if '.' in speed_num:
                                speed_num = speed_num.split('.')[0]
                            if int(speed_num) < 100:
                                hasError = self.restart(self.language_data['XmrStatus2'])
                                break
                            continue
                    
                    self.event.wait(60)
                    PID, _ = checkRunning(self.Exec_name)
                    if PID == 0:
                        self.restart(self.language_data['XmrStatus2'])
                        break

                process.wait()
            self.event.wait(60)
    
    def make_value(self, data):
        # use re
        match = re.match(r'\* ([\w\s]+)\s{2,}(.+)', data)
        if match:
            value = match.group(2).strip()
        return value