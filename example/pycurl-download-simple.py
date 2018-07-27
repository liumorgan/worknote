#coding:utf-8
import pycurl,StringIO
#传入图片的下载链接
url = 'http://junyiseo.com/wp-content/uploads/2016/10/6.jpg'
c = pycurl.Curl()	#通过curl方法构造一个对象
c.setopt(pycurl.FOLLOWLOCATION, True)	#自动进行跳转抓取
c.setopt(pycurl.MAXREDIRS,5)			#设置最多跳转多少次
c.setopt(pycurl.CONNECTTIMEOUT, 60)		#设置链接超时
c.setopt(pycurl.TIMEOUT,260)			#下载超时
c.fp = StringIO.StringIO()	
c.setopt(pycurl.URL, url)	#设置要访问的URL
c.setopt(c.WRITEFUNCTION, c.fp.write)	#回调写入字符串缓存
c.perform()		
code = c.getinfo(c.HTTP_CODE)	#返回状态码
img = c.fp.getvalue()	#返回源代码
#保存图片
f = open("./%s" % ("img_filename.jpg",), 'wb')
f.write(img)
f.close()