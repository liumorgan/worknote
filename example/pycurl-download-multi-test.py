#coding:utf-8
import pycurl,StringIO
from multiprocessing import Process, Queue,Lock

def buildcurl():
	c = pycurl.Curl()	#通过curl方法构造一个对象
	c.setopt(pycurl.FOLLOWLOCATION, True)	#自动进行跳转抓取
	c.setopt(pycurl.MAXREDIRS,5)			#设置最多跳转多少次
	c.setopt(pycurl.CONNECTTIMEOUT, 60)		#设置链接超时
	c.setopt(pycurl.TIMEOUT,260)			#下载超时
	return c

def download(c,url,path):		
	c.fp = StringIO.StringIO()	
	c.setopt(pycurl.URL, url)	#设置要访问的URL
	c.setopt(c.WRITEFUNCTION, c.fp.write)	#回调写入字符串缓存
	c.perform()		
	code = c.getinfo(c.HTTP_CODE)	#返回状态码
	body = c.fp.getvalue()	#返回源代码
	f = open(path, 'wb')
	f.write(body)
	f.close()
	

def download_fun(que,mutex):
	c = buildcurl()
	while True:
		try:
			pair=que.get(True,20)				
			url = pair[0]
			path = pair[1]
			#download(c,url,path)
			print(url)
			print(path)
		except:
			break
		
def create_test(que):
	for i in range(100):
		url = 'http://junyiseo.com/wp-content/uploads/2016/10/6.jpg'
		path='test%(id)d'%{'id':i}
		pair=(url,path)
		que.put(pair)
		
if __name__ == '__main__':
	que = Queue()
	lock = Lock()
	create_test(que)
	procs = []
	for i in range(5):
		p = Process(target=download_fun, args=(que,lock,))
		p.daemon = True
		procs.append(p)
		p.start()
	for i in range(5):
		procs[i].join()
