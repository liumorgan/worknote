'''
    requests,bs4
'''
 
import os
import requests
from bs4 import BeautifulSoup
import time
 
def getHtmlCode(url):  # 该方法传入url，返回url的html的源码
    headers = {
        'User-Agent': 'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
    }
 
    r= requests.get(url,headers=headers)
    r.encoding='UTF-8'
    page = r.text
    return page
 
def getImg(page,localPath):  # 该方法传入html的源码，经过截取其中的img标签，将图片保存到本机
    if not os.path.exists(localPath): # 新建文件夹
        os.mkdir(localPath)
    soup = BeautifulSoup(page,'html.parser') # 按照html格式解析页面
    imgList = soup.find_all('img')  # 返回包含所有img标签的列表
    x = 0
    for imgUrl in imgList:  # 列表循环
        print('正在下载：%s'%imgUrl.get('src'))
        ir = requests.get(imgUrl.get('src'))

        # open().write()方法原始且有效
        open(localPath+'%d.jpg'%x, 'wb').write(ir.content)
        x+=1
 
 
if __name__ == '__main__':
    url = 'http://www.zhangzishi.cc/20160712mz.html'
    localPath = 'e:/pythonSpiderFile/img8/'
    page = getHtmlCode(url)
    getImg(page,localPath)