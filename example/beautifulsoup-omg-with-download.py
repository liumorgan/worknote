#coding=utf-8
import io
import os
import time
import sys
import urllib
import urllib2
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from xml.etree.ElementTree import parse
from xml.etree.ElementTree import fromstring
import re
import requests
import traceback

import pycurl,StringIO
from multiprocessing import Process, Queue,Lock


def buildcurl():
	c = pycurl.Curl()	#通过curl方法构造一个对象
	c.setopt(pycurl.FOLLOWLOCATION, True)	#自动进行跳转抓取
	c.setopt(pycurl.MAXREDIRS,5)			#设置最多跳转多少次
	c.setopt(pycurl.CONNECTTIMEOUT, 60)		#设置链接超时
	c.setopt(pycurl.TIMEOUT,260)			#下载超时
	return c

def download_curl(url,path):
	try:
		c=buildcurl()
		c.fp = StringIO.StringIO()	
		print("curl %s"%(url))
		c.setopt(pycurl.URL, str(url))	#设置要访问的URL
		c.setopt(c.WRITEFUNCTION, c.fp.write)	#回调写入字符串缓存
		c.perform()		
		code = c.getinfo(c.HTTP_CODE)	#返回状态码
		body = c.fp.getvalue()	#返回源代码
		f = open("%s" % (path,), 'wb')
		f.write(body)
		f.close()
	except Exception, e:
		print 'str(Exception):\t', str(Exception)
		print 'str(e):\t\t', str(e)
		print 'repr(e):\t', repr(e)
		print 'e.message:\t', e.message
		print 'traceback.print_exc():'; traceback.print_exc()
		print 'traceback.format_exc():\n%s' % traceback.format_exc()	
		print("exception pid=%d"%(os.getpid()))		

def download_fun(que,lock):
	while True:
		try:
			lock.acquire()
			if que.empty():
				print("pid=%d sleep 1 second "%(os.getpid()))
				lock.release()
				time.sleep( 1 )				
				continue
			pair=que.get()	
			lock.release()
			url = pair[0]
			path = pair[1]
			
			print("pid=%d download %s to %s"%(os.getpid(),url,path))
			download_curl(url,path)
		except Exception, e:
			print 'str(Exception):\t', str(Exception)
			print 'str(e):\t\t', str(e)
			print 'repr(e):\t', repr(e)
			print 'e.message:\t', e.message
			print 'traceback.print_exc():'; traceback.print_exc()
			print 'traceback.format_exc():\n%s' % traceback.format_exc()	
			print("exception pid=%d"%(os.getpid()))
			break			
			
def realdownload(path,ref):
	print(ref)
	ir = requests.get(ref)
	open(path, 'wb').write(ir.content)

def download_omg(name,url,que,lock):
	req=urllib2.Request(url)
	html=urllib2.urlopen(req)
	soup=BeautifulSoup(html.read(),"html.parser")
	for a in soup.find_all('a',attrs={'class':'download-document'}):
		if type(a) == NavigableString:
			continue
		ref = a.get("href")
		if ref.endswith("PDF"):
			path="./omg/"+ name.replace("/","-") +".pdf"
			#realdownload(path,ref)
			print("put " + ref + " -O " + path )
			pair=(ref,path)
			lock.acquire()
			que.put(pair)
			lock.release()
			break

def parsespecf(que,lock):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
	req=urllib2.Request("https://www.omg.org/spec/",headers=headers)
	html=urllib2.urlopen(req)
	soup=BeautifulSoup(html.read(),"html.parser")
	idx=0
	for tb in soup.find_all('tbody'):
		for tr in tb.children:
			if type(tr) == NavigableString:
				continue
			i = 0
			name=""
			url=""
			
			for td in tr.children:
				if type(td) == NavigableString:
					continue
				if i == 0:
					name=td.string
				elif i == 1:
					url=td.a.get("href")
				i = i+1
			print(idx)
			idx=idx+1
			#print(name)
			#print(url)
			download_omg(name,url,que,lock)
			

if __name__ == '__main__':
	#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')	
	que = Queue()
	lock = Lock()

	procs = []
	for i in range(6):
		p = Process(target=download_fun, args=(que,lock,))
		p.daemon = True
		procs.append(p)
		p.start()
		
	parsespecf(que,lock)
	
	for i in range(len(procs)):
		procs[i].join()