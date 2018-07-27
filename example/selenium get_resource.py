from selenium import webdriver
 
browser = webdriver.PhantomJS()
browser.get('https://www.baidu.com')
browser.implicitly_wait(10)
data = browser.find_element_by_xpath('/*')
print browser.title
print data.text
with open('2.html', 'w') as fp:
    fp.write(browser.page_source.encode('utf8'))
browser.quit()