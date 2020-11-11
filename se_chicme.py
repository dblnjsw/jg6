from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import random


class Se_chicme():
    wd = None
    wait = None

    def __init__(self, headless=False):
        option = webdriver.ChromeOptions()
        if headless:
            option.add_argument('--headless')

        option.add_argument("-lang=en-us")

        self.wd = webdriver.Chrome(options=option, executable_path=ChromeDriverManager().install())
        self.wait = WebDriverWait(self.wd, 5)

        self.wd.get('https://www.chicme.xyz')

    def login(self,email,password):
        # locator=(By.XPATH, '//input[@id="email"]')
        # cls_xpath='//div[@class="cls"]/i'

        self.wd.find_element_by_xpath('//input[@id="email"]').send_keys(email)
        self.wd.find_element_by_xpath('//input[@id="password"]').send_keys(password)
        self.wd.find_element_by_xpath('//button[@id="btns"]').click()

        self.__pop_up0()


    def regist(self,email,password,firstname,lastname):
        xpath_email='//form[@id="register-former"]/div/input[@id="email"]'
        xpath_password = '//form[@id="register-former"]/div/input[@id="password"]'
        xpath_firstname='//input[@id="firstName"]'
        xpath_lastname = '//input[@id="lastName"]'
        xpath_read='//span[@id="read"]'
        xpath_button='//button[@id="submit-register"]'

        self.wd.find_element_by_xpath(xpath=xpath_email).send_keys(email)
        self.wd.find_element_by_xpath(xpath=xpath_password).send_keys(password)
        self.wd.find_element_by_xpath(xpath=xpath_firstname).send_keys(firstname)
        self.wd.find_element_by_xpath(xpath=xpath_lastname).send_keys(lastname)
        self.wd.find_element_by_xpath(xpath=xpath_read).click()
        self.wd.find_element_by_xpath(xpath=xpath_button).click()

        self.__pop_up0()

    def logout(self):
        cs_account='a[href="/me/m"]'
        cs_logout='li[class="fc-g sign-out"]'

        ActionChains(self.wd).move_to_element(self.wd.find_element_by_css_selector(cs_account)).perform()
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,cs_logout)))
        self.wd.find_element_by_css_selector(cs_logout).click()

    def add_chart(self):
        cs_items='div.xi-list-products'
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,cs_items)))
        print(self.wd.find_element_by_css_selector(cs_items))

    def enter_login(self):
        print('开始跳转登录页')
        self.__pop_up_index()
        cs_login='span[class="iconfont"]'
        cs_login_email='input#email'
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,cs_login)))
        self.wd.find_element_by_css_selector(cs_login).click()

        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,cs_login_email)))
        print('跳转成功')




    def __pop_up0(self):
        cs_continue='div[class="msclose __continue"]'
        try:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,cs_continue)))
            self.wd.find_element_by_css_selector(cs_continue).click()
        except:
            print('未找到弹窗0')

    def __pop_up_index(self):
        css_cls = 'div.cls i'

        try:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,css_cls)))
            self.wd.find_element_by_css_selector(css_cls).click()
        except:
            print('未找到首页弹窗')




def gen_email_password():
    email='1'
    password=''
    for i in range(8):
        email+=str(random.randint(0,10))
        password+=str(random.randint(0,10))
    email+='@gmail12.com'

    return (email,password)


def test_regist_login(email,password):
    chicme = Se_chicme()
    chicme.enter_login()
    chicme.regist(email,password,'a','b')
    chicme.logout()
    chicme.enter_login()
    chicme.login(email,password)

if __name__ == '__main__':
    # email='123456'
    # chicme = Se_chicme()
    # chicme
    # chicme.login('123@gmail','123')
    email,password=gen_email_password()
    test_regist_login(email,password)
