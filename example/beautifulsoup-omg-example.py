#coding=utf-8
import io
import os
import sys
import urllib
from urllib.request import  urlopen
from urllib  import request
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from xml.etree.ElementTree import parse
from xml.etree.ElementTree import fromstring
import re
import requests

def realdownload(path,ref):
	print(ref)
	ir = requests.get(ref)
	open(path, 'wb').write(ir.content)

def download(name,url):
	req=request.Request(url)
	html=urlopen(req)
	soup=BeautifulSoup(html.read(),"html.parser")
	for a in soup.find_all('a',attrs={'class':'download-document'}):
		if type(a) == NavigableString:
			continue
		ref = a.get("href")
		if ref.endswith("PDF"):
			path="./omg/"+ name.replace("/","-") +".pdf"
			#realdownload(path,ref)
			print("wget " + ref + " -O \"" + path + "\"")
			break

def parsespecf():
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
	req=request.Request("https://www.omg.org/spec/",headers=headers)
	html=urlopen(req)
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
			print(name)
			print(url)
			download(name,url)
			
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
#download("aa","https://www.omg.org/spec/ZIOP/")
parsespecf()