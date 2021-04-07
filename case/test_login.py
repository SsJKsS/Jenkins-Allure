from selenium import webdriver
import pytest
import time
import allure
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()
driver.get('https://staging.teaches.cc/admin/login')
driver.maximize_window()


@allure.step("輸入帳號、密碼{arg1}，{arg2}，並點選登入")
def send_and_click_login(arg1, arg2):
    driver.find_element_by_name('email').send_keys(arg1)  # 定位帳號
    driver.find_element_by_name('password').send_keys(arg2)  # 定位密碼
    driver.find_element_by_class_name('ant-btn').click()  # 登入按鈕
    print('成功了')
    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name('logout'))
    driver.close()


@allure.step("輸入帳號、密碼")
def input_username_and_password():
    send_and_click_login('jack@teaches.cc', '00000000')


@allure.feature('登入')
@allure.story('正常登入情境')
@allure.step("驗證登入過程")
def test_login():
    input_username_and_password()


