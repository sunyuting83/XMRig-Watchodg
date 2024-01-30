import time
import requests
from UI.view import UpdateProgress, setLog
from public import gl_thread_lock
def DownloadFile(url, filename, language_data):
    start = time.time()
    headers = {
		'accept': 'application/json, text/javascript, */*; q=0.01',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		"X-Requested-With": "XMLHttpRequest",
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
	}
    res = requests.get(url, headers=headers, stream=True)

    chunk_size = 1024
    content_size = int(res.headers["content-length"]) 
    size = 0
    if res.status_code == 200:
        with open(f"{filename}", 'wb') as f:
            percen:int = 0
            for data in res.iter_content(chunk_size=chunk_size):
                f.write(data)
                size += len(data)
                percentage:int = int(size / content_size * 100)
                if percentage > percen:
                    gl_thread_lock.acquire()
                    UpdateProgress(percentage)
                    gl_thread_lock.release()
                percen = percentage

    end = time.time()
    gl_thread_lock.acquire()
    setLog("["+language_data['DownloadTime']+"]: {:.2f}s".format(end - start))
    gl_thread_lock.release()

if __name__ == '__main__':
    DownloadFile("https://mirrors.sdu.edu.cn/software/Windows/WePE/WePE_64_V2.3.exe", "temp.exe")