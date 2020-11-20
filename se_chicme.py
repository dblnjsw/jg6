from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import random
import time
import traceback

web = 'https://www.shop-test-1.elasticbeanstalk.com'


class Se_chicme():
    wd = None
    wait = None
    longwait = None
    msite = False
    web = web

    def __init__(self, headless=False, msite=False, init=True):
        if not init:
            return
        option = webdriver.ChromeOptions()
        self.msite = msite
        if headless:
            option.add_argument('--headless')
        if self.msite:
            mobileEmulation = {'deviceName': 'iPhone X'}
            option.add_experimental_option('mobileEmulation', mobileEmulation)

        option.add_argument('--ignore-ssl-errors=yes')
        option.add_argument('--ignore-certificate-errors')
        option.add_argument("-lang=en-us")

        self.wd = webdriver.Chrome(options=option, executable_path=ChromeDriverManager().install())
        self.wait = WebDriverWait(self.wd, 10)
        self.longwait = WebDriverWait(self.wd, 30)

        # self.wd.get('https://www.chicme.xyz')
        self.enter_index()

    def login(self, email, password):
        locator = (By.XPATH, '//input[@id="email"]')
        cls_xpath = '//div[@class="cls"]/i'

        self.wd.find_element_by_xpath('//input[@id="email"]').send_keys(email)
        self.wd.find_element_by_xpath('//input[@id="password"]').send_keys(password)
        self.wd.find_element_by_xpath('//button[@id="btns"]').click()

        self.__pop_up0()
        # se_chicme_static.login(self.wd,self.wait,self.longwait,email,password)

    def regist(self, email, password, firstname, lastname):
        xpath_email = '//form[@id="register-former"]/div/input[@id="email"]'
        xpath_password = '//form[@id="register-former"]/div/input[@id="password"]'
        xpath_firstname = '//input[@id="firstName"]'
        xpath_lastname = '//input[@id="lastName"]'
        xpath_read = '//span[@id="read"]'
        xpath_button = '//button[@id="submit-register"]'

        self.wd.find_element_by_xpath(xpath=xpath_email).send_keys(email)
        self.wd.find_element_by_xpath(xpath=xpath_password).send_keys(password)
        self.wd.find_element_by_xpath(xpath=xpath_firstname).send_keys(firstname)
        self.wd.find_element_by_xpath(xpath=xpath_lastname).send_keys(lastname)
        self.wd.find_element_by_xpath(xpath=xpath_read).click()
        self.wd.find_element_by_xpath(xpath=xpath_button).click()

        self.__pop_up0()

    def logout(self):
        cs_account = 'a[href="/me/m"]'
        cs_logout = 'li[class="fc-g sign-out"]'

        ActionChains(self.wd).move_to_element(self.wd.find_element_by_css_selector(cs_account)).perform()
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_logout)))
        self.wd.find_element_by_css_selector(cs_logout).click()

    # @staticmethod
    def add_chart(self, haveCache=False):
        print("add_chart:商品加入购物车")

        cs_items = 'span[class="__btn addtocart"]'
        cs_colors = 'ul.p-colors li'
        cs_sizes = 'ul.p-sizes li'
        cs_qty = 'div#xproductbuyerqty span'
        cs_buy = 'span#xproductbuyerbuy'
        cs_carti = 'a[class="i-cart v-m relative"]'
        cs_cart = 'a[class="minicart-btn block"]'
        xp_checkout = '//div[text()="Proceed to Checkout"]'

        xp_items_ms = '//span[contains(text(),"buy now")]'
        xp_checkout_ms = '//div[contains(text(),"Check Out")]'
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_items_ms)))
        if not self.msite:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_items)))
            self.wd.find_element_by_css_selector(cs_items).click()

            self.longwait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_colors)))
            colors = self.wd.find_elements_by_css_selector(cs_colors)
            colors[1].click()
            sizes = self.wd.find_elements_by_css_selector(cs_sizes)
            sizes[1].click()
            self.wd.find_elements_by_css_selector(cs_qty)[1].click()
            self.wd.find_element_by_css_selector(cs_buy).click()

            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_carti)))

            self.wd.get(self.web + '/cart')
            if not haveCache:
                self.longwait.until(EC.element_to_be_clickable((By.XPATH, xp_checkout)))
                self.wd.find_element_by_xpath(xp_checkout).click()
        else:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_items_ms)))
            # self.wd.find_element_by_xpath(xp_items_ms).click()
            element_xp_items_ms = self.wd.find_element_by_xpath(xp_items_ms)
            self.wd.execute_script("arguments[0].click();", element_xp_items_ms)

            self.longwait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_colors)))
            colors = self.wd.find_elements_by_css_selector(cs_colors)
            self.wd.execute_script("arguments[0].click();", colors[1])
            sizes = self.wd.find_elements_by_css_selector(cs_sizes)
            self.wd.execute_script("arguments[0].click();", sizes[1])
            qtys = self.wd.find_elements_by_css_selector(cs_qty)
            self.wd.execute_script("arguments[0].click();", qtys[1])
            self.wd.execute_script("arguments[0].click();", self.wd.find_element_by_css_selector(cs_buy))

            # self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_carti)))
            time.sleep(3)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_checkout_ms)))
            self.wd.execute_script("arguments[0].click();", self.wd.find_element_by_xpath(xp_checkout_ms))

            # self.wd.get('https://www.chicme.xyz/cart')
            # if not haveCache:
            #     self.longwait.until(EC.element_to_be_clickable((By.XPATH, xp_checkout_ms)))
            #     self.wd.find_element_by_xpath(xp_checkout_ms).click()

    def pay_paypal(self, wd=wd, wait=wait, longwait=longwait):
        print("pay_paypal:paypal支付")
        xp_confirm = '//button[text()="Confirm"]'
        xp_paywith = '//div[@aria-label="Pay with PayPal"]'
        xp_select_paypal = '//*[@id="root"]/div/div[2]/div/div/div[1]/div/div[2]/div/div[2]/div/ul/li[1]/div/div/div[1]/span'
        xp_edit = '//span[text()="Edit"]'
        cs_next = 'button[class="button actionContinue scTrack:unifiedlogin-login-click-next"]'
        cs_login = 'button[class="button actionContinue scTrack:unifiedlogin-login-submit"]'
        cs_pay_b = 'button#payment-submit-btn'
        xp_yanqi = '//h2[text()="延期付款"]'

        cs_email_pay = 'input#email'
        cs_password_pay = 'input#password'

        xp_select_paypal_ms = '//*[@id="root"]/div/div[1]/div/div[5]/div[2]/ul/li[1]/div/div/div/div[2]/span'
        xp_checkout_ms = '//div[contains(text(),"Check Out")]'

        if not self.msite:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_select_paypal)))
            self.wd.find_element_by_xpath(xp_select_paypal).click()
            self.wd.find_element_by_xpath(xp_confirm).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_edit)))

            time.sleep(5)
            cs_iframe = 'iframe[class="zoid-component-frame zoid-visible"]'
            iframe = self.wd.find_element_by_css_selector(cs_iframe)
            self.wd.switch_to.frame(iframe)

            # ActionChains(self.wd).move_to_element(self.wd.find_element_by_xpath(xp_paywith)).perform()
            time.sleep(1)
            self.wd.find_element_by_xpath(xp_paywith).click()
            self.wd.find_element_by_xpath(xp_paywith).click()
            time.sleep(1)
            handles = self.wd.window_handles
            self.wd.switch_to.window(handles[1])
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_email_pay)))
            self.wd.find_element_by_css_selector(cs_email_pay).send_keys('amour01@163.com')
            self.wd.find_element_by_css_selector(cs_next).click()

            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_password_pay)))
            self.wd.find_element_by_css_selector(cs_password_pay).send_keys('12345678')
            self.wd.find_element_by_css_selector(cs_login).click()

            pay_b = self.wd.find_element_by_css_selector(cs_pay_b)
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_pay_b)))
            self.wd.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            self.longwait.until(EC.element_to_be_clickable((By.XPATH, xp_yanqi)))
            self.wd.find_element_by_css_selector(cs_pay_b).send_keys(Keys.ENTER)
            # self.wd.find_element_by_css_selector(cs_pay_b).click()

            self.wd.switch_to.window(handles[0])
            self.afterpay()
            # self.wd.save_screenshot('a1.jpg')
        else:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_select_paypal_ms)))
            self.wd.execute_script("arguments[0].click();", self.wd.find_element_by_xpath(xp_select_paypal_ms))
            time.sleep(1)
            self.wd.execute_script("arguments[0].click();", self.wd.find_element_by_xpath(xp_checkout_ms))

            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_email_pay)))
            self.wd.find_element_by_css_selector(cs_email_pay).send_keys('amour01@163.com')
            self.wd.execute_script("arguments[0].click();", self.wd.find_element_by_css_selector(cs_next))

            # ok

            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_password_pay)))
            self.wd.find_element_by_css_selector(cs_password_pay).send_keys('12345678')
            self.wd.execute_script("arguments[0].click();", self.wd.find_element_by_css_selector(cs_login))

            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_pay_b)))
            self.wd.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            self.longwait.until(EC.element_to_be_clickable((By.XPATH, xp_yanqi)))
            self.wd.execute_script("arguments[0].click();", self.wd.find_element_by_css_selector(cs_pay_b))

            self.afterpay()

    def pay_creditcard(self, cardname, haveCache=False):
        print("pay_creditcard:信用卡支付")
        xp_submit = '//button[contains(text(),"Submit")]'
        xp_confirm = '//button[text()="Confirm"]'
        xp_paywith = '//div[text()="Check Out"]'
        xp_select_cc = '//*[@id="root"]/div/div[2]/div/div/div[1]/div/div[2]/div/div[2]/div/ul/li[3]/div/div/div[1]/span'
        xp_edit = '//span[text()="Edit"]'
        cs_cardname = 'input#cc_card_number'
        cs_date = 'input#cc-exp-date'
        cs_ccv2 = 'input#cc_cvv2'
        cs_continue = 'button#continueButton'

        xp_select_cc_ms = '//*[@id="root"]/div/div[1]/div/div[5]/div[2]/ul/li[3]/div/div/div/div[2]/span'
        xp_checkout_ms = '//div[contains(text(),"Check Out")]'

        if not self.msite:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_select_cc)))
            self.wd.find_element_by_xpath(xp_select_cc).click()

            if not haveCache:
                self.wd.find_element_by_xpath(xp_confirm).click()
            # es = self.wd.find_elements_by_xpath(xp_edit)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_edit)))

            time.sleep(3)
            self.wd.find_element_by_xpath(xp_paywith).click()
            self.longwait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_cardname)))
            self.wd.find_element_by_css_selector(cs_cardname).send_keys(cardname)
            self.wd.find_element_by_css_selector(cs_date).send_keys('12/20')
            self.wd.find_element_by_css_selector(cs_ccv2).send_keys('123')

            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_continue)))
            self.wd.find_element_by_css_selector(cs_continue).click()
            self.afterpay()
        else:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_select_cc_ms)))
            self.wd.execute_script("arguments[0].click();", self.wd.find_element_by_xpath(xp_select_cc_ms))
            time.sleep(1)
            self.wd.execute_script("arguments[0].click();", self.wd.find_element_by_xpath(xp_checkout_ms))

            self.longwait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_cardname)))
            self.wd.find_element_by_css_selector(cs_cardname).send_keys(cardname)
            self.wd.find_element_by_css_selector(cs_date).send_keys('12/20')
            self.wd.find_element_by_css_selector(cs_ccv2).send_keys('123')

            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_continue)))
            self.wd.find_element_by_css_selector(cs_continue).click()
            self.afterpay()

    def fill_address(self):
        print("fill_address:填写个人信息")
        (email, password) = gen_email_password()
        xp_email = '//input[@name="email"]'
        xp_name = '//input[@name="name"]'
        xp_streetaddress = '//input[@name="streetAddress1"]'
        xp_city = '//input[@name="city"]'
        xp_zipCode = '//input[@name="zipCode"]'
        xp_phoneNumber = '//input[@name="phoneNumber"]'
        xp_state = '//select[@name="state"]'
        xp_submit_ms = '//button[text()="Submit"]'

        self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_email)))

        self.wd.find_element_by_xpath(xp_email).send_keys(email)
        self.wd.find_element_by_xpath(xp_name).send_keys('a b')
        self.wd.find_element_by_xpath(xp_streetaddress).send_keys('a')
        self.wd.find_element_by_xpath(xp_city).send_keys('a')
        self.wd.find_element_by_xpath(xp_zipCode).send_keys('11111')
        self.wd.find_element_by_xpath(xp_phoneNumber).send_keys('1300888899')

        selector = Select(self.wd.find_element_by_xpath(xp_state))
        selector.select_by_index('2')

        if self.msite:
            self.wd.execute_script("arguments[0].click();", self.wd.find_element_by_xpath(xp_submit_ms))

    def enter_login(self):
        print('enter_login:跳转登录界面')
        self.__pop_up_index()
        cs_login = 'span[class="iconfont"]'
        cs_login_email = 'input#email'
        try:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_login)))
            self.wd.find_element_by_css_selector(cs_login).click()

            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_login_email)))
        except:
            self.wd.get(self.web + '/i/login')
            print('跳转成功')

    def enter_index(self):
        xp_banner = '//*[@id="i-collection-events"]/li[2]/a/img'
        self.wd.get(self.web)
        self.__pop_up_index()

        self.longwait.until(EC.element_to_be_clickable((By.XPATH, xp_banner)))

    def __pop_up0(self):
        cs_continue = 'div[class="msclose __continue"]'
        try:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_continue)))
            self.wd.find_element_by_css_selector(cs_continue).click()
        except:
            print('未找到弹窗0')

    def __pop_up_index(self):
        css_cls = 'div.cls i'
        css_cls_ms = '#ninimour-alert-sub-window > div.iconfont.cls'
        if not self.msite:
            try:
                self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_cls)))
                self.wd.find_element_by_css_selector(css_cls).click()
            except:
                print('未找到首页弹窗')
        else:
            try:
                # self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_cls_ms)))
                time.sleep(1)
                element_css_cls = self.wd.find_element_by_css_selector(css_cls_ms)
                self.wd.execute_script("arguments[0].click();", element_css_cls)
            except:
                print('未找到首页弹窗')

    def afterpay(self):
        cs_cls = 'a.stjr-review-checkout-widget-body__close'
        try:
            self.longwait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_cls)))
            self.wd.find_element_by_css_selector(cs_cls).click()
        except:
            print('未完成支付')


def gen_email_password():
    email = '1'
    password = ''
    for i in range(8):
        email += str(random.randint(0, 10))
        password += str(random.randint(0, 10))
    email += '@gmail12.com'

    return (email, password)


def test_main(email, password):
    try:
        test_main_1(ms=True)
    except Exception:
        print('test_main_1 fail')
        traceback.print_exc()

    # try:
    #     test_main_2(email,password)
    # except Exception:
    #     print('test_main_2 fail')
    #     traceback.print_exc()


def test_main_1(ms=False):
    chicme = Se_chicme(msite=ms)
    chicme.add_chart()
    chicme.fill_address()
    chicme.pay_paypal()
    chicme.wd.save_screenshot('test1.1.png')

    # 1.2
    chicme.enter_index()
    chicme.add_chart(haveCache=True)
    # chicme.fill_address()
    chicme.pay_creditcard('4000020951595032', haveCache=True)
    chicme.wd.save_screenshot('test1.2.png')

    # 1.3
    chicme2 = Se_chicme(msite=ms)
    chicme2.add_chart()
    chicme2.fill_address()
    chicme2.pay_creditcard('4002812166761203')
    chicme2.wd.save_screenshot('test1.3.png')


def test_main_2(email, password):
    chicme = Se_chicme()
    chicme.enter_login()
    chicme.regist(email, password, 'a', 'b')
    chicme.logout()
    chicme.enter_login()
    chicme.login(email, password)
    chicme.add_chart()
    chicme.fill_address()
    chicme.pay_paypal()
    chicme.wd.get(web + '/cart/checkout')
    chicme.pay_creditcard('4000020951595032')
    chicme.wd.get(web + '/cart/checkout')
    chicme.pay_creditcard('4002812166761203', haveCache=True)


if __name__ == '__main__':
    email, password = gen_email_password()
    test_main(email, password)
