#-*- coding:utf-8 -*-

from bs4 import BeautifulSoup

import urllib2
import urllib
import json   #使用json格式存储

def tencent():
    url = "http://hr.tencent.com/"

    request = urllib2.Request(url+"position.php?&start=10#a")
    response = urllib2.urlopen(request)

    resHtml = response.read()

    output = open('tencent.json', 'w')

    html = BeautifulSoup(resHtml, 'lxml')


    #创建CSS选择器
    result = html.select('tr[class="even"]')
    result2 = html.select('tr[class="odd"]')
    result += result2

    print(result)
    items = []
    for site in result:
        item = {}

        name = site.select('td a')[0].get_text()
        dataLink = site.select('td a')[0].attrs['href']
        catalog = site.select('td')[1].get_text()
        recruitNumber = site.select('td')[2].get_text()
        workLocation = site.select('td')[3].get_text()
        publishTime = site.select('td')[4].get_text()

        item['name'] = name
        item['datailLink'] = url + dataLink
        item['catalog'] = catalog
        item['recruitNumber'] = recruitNumber
        item['publishTime'] = publishTime

        items.append(item)
    #禁用ascii编码，按utf-8编码
    line = json.dumps(items, ensure_ascii = False)

    output.write(line.encode('utf-8'))

    output.close()


if __name__ == '__main__':
    tencent()