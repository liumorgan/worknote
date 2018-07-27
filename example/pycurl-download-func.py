#coding:utf-8
import pycurl,StringIO

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
	
c = buildcurl()	
url = 'http://junyiseo.com/wp-content/uploads/2016/10/6.jpg'
download(c,url,'test.jpg')