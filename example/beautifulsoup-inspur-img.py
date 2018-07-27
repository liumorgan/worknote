import urllib
import urllib2
from bs4 import BeautifulSoup
import re


url="http://www.inspur.com"
request = urllib2.Request(url)
response = urllib2.urlopen(request) 

body=response.read()
soup = BeautifulSoup(body,"html.parser")
imgs= soup.find_all('img', attrs={"border": "0"})
#soup.find_all(src=re.compile(".*\.png"), attrs={'border':'0'})
#len(soup.find_all(src=re.compile(".*img_pc_site.*\.png"), attrs={'border':'0'}))
#soup.find_all(src=re.compile(".*\.png"), attrs={'border':'0'},limit=10)
for img in imgs:
	print img['src']