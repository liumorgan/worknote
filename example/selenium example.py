# coding:utf-8
from time import sleep
from selenium import webdriver  # 从selenium中引入webdriver

username_file = open("G:\\joker_study\\username.txt")  # 打开账号文本路径
username = username_file.read()  # 取出账号

password_file = open("G:\\joker_study\\password.txt")  # 打开密码文本路径
password = password_file.read()  # 取出密码def login_mantis_by_txt():
    driver = webdriver.Firefox()  # 选择打开的浏览器
    driver.maximize_window()  # 浏览器窗口最大化
    driver.implicitly_wait(3)  # 隐式等待
    driver.get("http://192.168.1.201/mantisbt-1.2.19/login_page.php")  # 获取URL，打开页面
    sleep(1)  # 直接等待
    username_input = driver.find_element_by_xpath("html/body/div[3]/form/table/tbody/tr[2]/td[2]/input")  # 获取输入账号框
    username_input.send_keys(username)  # 输入账号
    sleep(1)
    password_input = driver.find_element_by_xpath("html/body/div[3]/form/table/tbody/tr[3]/td[2]/input")  # 获取输入密码框
    password_input.send_keys(password)  # 输入密码
    sleep(1)
    login_button = driver.find_element_by_xpath("html/body/div[3]/form/table/tbody/tr[6]/td/input")  # 获取登录按钮
    login_button.click()  # 点击登录按钮
    sleep(3)
    driver.quit()  # 退出浏览器