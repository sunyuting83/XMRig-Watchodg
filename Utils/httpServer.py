# -*-coding:utf-8 -*-
import requests

def HttpGet(uri):
	send_headers = {
		'accept': 'application/json, text/javascript, */*; q=0.01',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		"X-Requested-With": "XMLHttpRequest",
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
	}

	send_headers['X-Auth-Token'] = 'YzZkMDllYTAtZGRlOS00NGE5LWI0MGItMmU5YzllMDQyMjY4'
	data = {
		'status': 0
    }
	try:
		req = requests.get(uri,headers=send_headers, timeout=15)
		data = req.json()
		return data
	except Exception as e:
		return {
				'status': 1,
				'message': e
			}
# if __name__ == '__main__':
# 	a = HttpGet('http://version.swithc8.top/api/getd', 'a37a5d30')
# 	print(a)