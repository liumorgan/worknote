
from selenium import webdriver
 
browser = webdriver.PhantomJS()
browser.get('https://www.baidu.com')
browser.implicitly_wait(5)
print(browser.page_source)