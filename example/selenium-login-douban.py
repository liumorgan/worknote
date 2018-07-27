#-*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

#如果获取页面时获取不到文本内容，加入下面参数
driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
driver.set_window_size(1366, 768)
driver.get("http://www.douban.com/")

print(driver.page_source)
#输入账号和密码

driver.find_element_by_name("form_email").send_keys("1216938752@qq.com")
driver.find_element_by_name("form_password").send_keys('chenqi1992')

#模拟点击登录
driver.find_element_by_xpath("//input[@class='bn-submit']").click()

#等待3秒
time.sleep(3)

#生成登录后快照

with open('douban.html', 'w') as file:
    file.write(driver.page_source.encode('UTF-8'))

driver.quit()