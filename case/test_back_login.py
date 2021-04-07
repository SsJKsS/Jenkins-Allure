from selenium import webdriver
import pytest
import time
import allure
from selenium.webdriver.support.wait import WebDriverWait


driver = webdriver.Chrome()
driver.get('https://staging.teaches.cc/admin/login')
driver.maximize_window()

# 定位帳號欄位
account_blank = driver.find_element_by_name('email')
account_blank_text = account_blank.get_attribute('placeholder')
# 定位密碼欄位
password_blank = driver.find_element_by_name('password')
password_blank_text = password_blank.get_attribute('placeholder')
# 定位登入按鈕
login_btn = driver.find_element_by_class_name('ant-btn')


def err():
    # 定位登入錯誤訊息
    login_err_text = login_btn.get_attribute('ant-click-animating-without-extra-node')
    assert login_err_text == 'true'


# 【後台】登入頁面欄位、邏輯
@allure.feature('【後台】登入')
@allure.story('欄位文案驗證')
def blank_placeholder_check():
    print('\n=======欄位驗證=======')
    assert account_blank_text == '電子郵件'  # 判斷帳號欄位placeholder
    print('登入帳號欄位 placeholder 為 : ' + account_blank_text)
    assert password_blank_text == '密碼'  # 判斷密碼欄位placeholder
    print('登入密碼欄位 placeholder 為 : ' + password_blank_text)


@allure.story('欄位邏輯驗證')
@allure.step("不輸入帳號、密碼登入")
def no_account_password():
    # 不輸入帳號、密碼登入
    print('\n=======不輸入帳號、密碼登入=======')
    login_btn.click()
    err()
    print('不輸入帳號、密碼登入有跳出 Toast')


@allure.step("只輸入不合格式帳號登入")
def only_incorrect_format_account():
    # 只輸入不合格式帳號登入
    print('\n=======只輸入不合格式帳號登入=======')
    account_blank.send_keys('teaches')
    login_btn.click()
    err()
    print('只輸入不合格式帳號登入有跳出 Toast')


@allure.step("只輸入符合格式帳號(未註冊)登入")
def only_correct_format_unregistered_account():
    # 只輸入符合格式帳號(未註冊)登入
    print('\n=======只輸入符合格式帳號登入(未註冊)=======')
    account_blank.clear()
    account_blank.send_keys('teaches@gmail.com')
    login_btn.click()
    err()
    print('不輸入密碼登入有跳出 Toast')


@allure.step("只輸入密碼登入")
def only_password():
    # 只輸入密碼登入
    print('\n=======只輸入密碼登入=======')
    account_blank.clear()
    password_blank.send_keys('teaches')
    login_btn.click()
    err()
    print('不輸入帳號登入有跳出 Toast')


@allure.step("輸入符合格式帳號(未註冊)、密碼")
def correct_format_unregistered_account_password():
    # 輸入符合格式帳號(未註冊)、密碼
    print('\n=======輸入符合格式帳號(未註冊)、密碼登入=======')
    password_blank.clear()
    account_blank.send_keys('teaches@gmail.com')
    password_blank.send_keys('00000000')
    login_btn.click()
    WebDriverWait(driver, 20).until(lambda x: x.find_element_by_class_name(
        'src-styles-ErrorMessage-module__container--2MSYJ').text)
    error_message = driver.find_element_by_class_name(
        'src-styles-ErrorMessage-module__container--2MSYJ').text
    assert error_message == '帳號或密碼錯誤'
    print('輸入符合格式帳號(未註冊)、密碼跳出 wording : ' + error_message)


@allure.step("輸入符合格式帳號(已註冊)、錯誤密碼登入")
def correct_format_registered_account_wrong_password():
    # 輸入符合格式帳號(已註冊)、錯誤密碼
    print('\n=======輸入符合格式帳號(已註冊)、錯誤密碼登入=======')
    account_blank.clear()
    password_blank.clear()
    account_blank.send_keys('jack@teaches.cc')
    password_blank.send_keys('00000001')
    login_btn.click()
    WebDriverWait(driver, 20).until(lambda x: x.find_element_by_class_name(
        'src-styles-ErrorMessage-module__container--2MSYJ').text)
    error_message = driver.find_element_by_class_name(
        'src-styles-ErrorMessage-module__container--2MSYJ').text
    assert error_message == '帳號或密碼錯誤'
    print('輸入符合格式帳號(已註冊)、錯誤密碼跳出 wording : ' + error_message)


@allure.feature('登入')
@allure.story('正常登入情境')
@allure.step("驗證登入過程")
def test_back_login():
    blank_placeholder_check()
    no_account_password()
    only_incorrect_format_account()
    only_correct_format_unregistered_account()
    only_password()
    correct_format_unregistered_account_password()
    correct_format_registered_account_wrong_password()
