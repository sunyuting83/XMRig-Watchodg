import time
import requests
from UI.view import UpdateProgress, setLog
from public import gl_thread_lock
def DownloadFile(url, filename):
    start = time.time()  # 开始时间
    headers = {
		'accept': 'application/json, text/javascript, */*; q=0.01',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		"X-Requested-With": "XMLHttpRequest",
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
	}
    res = requests.get(url, headers=headers, stream=True)

    chunk_size = 1024  # 每次下载数据大小
    content_size = int(res.headers["content-length"])  # 文件总字节数
    size = 0
    if res.status_code == 200:
        # print("[文件地址]：", url)
        # print('[文件名称]:', filename)
        # print('[文件大小]: {:.3f} MB'.format(content_size / chunk_size / 1024))
        with open(f"{filename}", 'wb') as f:
            for data in res.iter_content(chunk_size=chunk_size):
                f.write(data)
                size += len(data)  # 已下载文件大小
                gl_thread_lock.acquire()
                UpdateProgress(int(size / content_size * 100))
                gl_thread_lock.release()
                # print('\r[下载进度]: {}{:.2f}%'.format('>' * int(size * 50 / content_size), float(size / content_size * 100)),end='')  # 下载进度条

    end = time.time()  # 结束时间
    gl_thread_lock.acquire()
    setLog('[下载时间]: {:.2f}s'.format(end - start))
    gl_thread_lock.release()
    # print("\n[下载时间]: {:.2f}s".format(end - start))
    # print("".center(100, "*"))

if __name__ == '__main__':
    DownloadFile("https://mirrors.sdu.edu.cn/software/Windows/WePE/WePE_64_V2.3.exe", "temp.exe")