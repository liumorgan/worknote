#-*- coding:utf-8 -*-
#本篇将模拟执行javascript语句

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get('https://www.baidu.com/')

#给搜索输入框标红
js = 'var q = document.getElementById(\"kw\"); q.style.border = \"2px solid red\";'

#调用给搜索框输入框标红js脚本
driver.execute_script(js)


#js隐藏元素，将获取到的图片元素隐藏
img = driver.find_element_by_xpath("//*[@id='lg']/img")
driver.execute_script('$(arguments[0]).fadeOut()', img)


#向下滚动到页面底部
driver.execute_script("$('.scroll_top').click(function(){$('html,body').animate({scrollTop: '0px'}, 800);});")


# driver.quit()