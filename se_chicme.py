from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.touch_actions import TouchActions
import random
import time
import math
import traceback

# web = 'https://www.shop-test-1.elasticbeanstalk.com'


web = 'https://chicme.com'


class Se_chicme():
    wd = None
    wait = None
    longwait = None
    msite = False
    headless = False
    web = web

    def __init__(self, headless=False, msite=False, driver=None):
        if driver:
            self.wd = driver
            self.wait = WebDriverWait(self.wd, 10)
            self.longwait = WebDriverWait(self.wd, 30)
            self.msite = msite
            return
        option = webdriver.ChromeOptions()
        self.msite = msite
        self.headless = headless
        if self.headless:
            option.add_argument('--headless')
        if self.msite:
            # mobileEmulation = {'deviceName': 'iPhone X'}
            mobileEmulation = {
            "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},  # 定义设备高宽，像素比
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) "  # 通过UA来模拟
            "AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
            option.add_experimental_option('mobileEmulation', mobileEmulation)

        option.add_argument('--ignore-ssl-errors=yes')
        option.add_argument('--ignore-certificate-errors')
        option.add_argument("-lang=en-us")

        self.wd = webdriver.Chrome(options=option, executable_path=ChromeDriverManager().install())
        self.wait = WebDriverWait(self.wd, 10)
        self.longwait = WebDriverWait(self.wd, 30)

        # self.wd.get('https://www.chicme.xyz')
        self.wd.maximize_window()
        self.enterIndex()

    def login(self, email, password):
        locator = (By.XPATH, '//input[@id="email"]')
        cls_xpath = '//div[@class="cls"]/i'

        self.wd.find_element_by_xpath('//input[@id="email"]').send_keys(email)
        self.wd.find_element_by_xpath('//input[@id="password"]').send_keys(password)
        self.wd.find_element_by_xpath('//button[@id="btns"]').click()

        self.__pop_up0()
        # se_chicme_static.login(self.wd,self.wait,self.longwait,email,password)

    def regist(self):
        xpath_email = '//form[@id="register-former"]/div/input[@id="email"]'
        xpath_password = '//form[@id="register-former"]/div/input[@id="password"]'
        xpath_firstname = '//input[@id="firstName"]'
        xpath_lastname = '//input[@id="lastName"]'
        xpath_read = '//span[@id="read"]'
        xpath_button = '//button[@id="submit-register"]'

        (email, password) = gen_email_password()
        firstname = 'a'
        lastname = 'b'

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
    def __add_chart(self, haveCache=False):
        print("add_chart:商品加入购物车")

        # cs_items = 'span[class="__btn addtocart"]'
        # cs_colors = 'ul.p-colors li'
        # cs_sizes = 'ul.p-sizes li'
        # cs_qty = 'div#xproductbuyerqty span'
        # cs_buy = 'span#xproductbuyerbuy'
        # cs_carti = 'a[class="i-cart v-m relative"]'
        # cs_cart = 'a[class="minicart-btn block"]'
        # xp_checkout = '//div[text()="Proceed to Checkout"]'
        #
        # xp_items_ms = '//span[contains(text(),"buy now")]'
        # xp_checkout_ms = '//div[contains(text(),"Check Out")]'

        cs_items = '.carousel.slide.__slider_body > div.carousel-inner > div.row.item.active > div:nth-child(1) > a'
        xp_items = '//*[@id="carousel-1G50t7w8J6e5T0y8q82L2Z4Z"]/div/div[1]/div[1]/a'
        cs_colors = 'ul.xp-colors li'
        cs_sizes = 'ul#sizes > li'
        cs_qty = 'div#qtycontainer span'
        cs_buy = 'button.xp-add-to-cart'
        cs_carti = 'button[class="xp-add-to-cart"]'
        cs_cart = 'a[class="minicart-btn block"]'
        xp_checkout = '//div[text()="Proceed to Checkout"]'

        xp_items_ms = '//span[contains(text(),"buy now")]'
        xp_checkout_ms = '//div[contains(text(),"Check Out")]'

        if not self.msite:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_items)))
            self.wd.find_element_by_css_selector(cs_items).click()

            self.longwait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_colors)))
            colors = self.wd.find_elements_by_css_selector(cs_colors)
            if len(colors) > 1:
                colors[1].click()
            else:
                colors[0].click()
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_sizes)))
            sizes = self.wd.find_elements_by_css_selector(cs_sizes)
            if len(sizes) > 1:
                sizes[1].click()
            else:
                sizes[0].click()
            # self.wd.find_elements_by_css_selector(cs_qty)[1].click()
            # self.wd.find_element_by_css_selector(cs_buy).click()

            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_carti)))
            self.wd.find_element_by_css_selector(cs_carti).click()
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

    def __pay_paypal(self, wd=wd, wait=wait, longwait=longwait):
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
            # self.wd.find_element_by_xpath(xp_confirm).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_edit)))

            time.sleep(3)
            cs_iframe = 'iframe[class="zoid-component-frame zoid-visible"]'
            iframe = self.wd.find_element_by_css_selector(cs_iframe)
            self.wd.switch_to.frame(iframe)

            # ActionChains(self.wd).move_to_element(self.wd.find_element_by_xpath(xp_paywith)).perform()
            time.sleep(1)
            self.wd.find_element_by_xpath(xp_paywith).click()
            time.sleep(3)
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
            self.screen_shot('paypal')
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
            self.screen_shot('paypal_msite')

    def __pay_creditcard(self, cardname, haveCache=False):
        """

        :param cardname:
        :param haveCache: 该浏览器是否支付过
        """
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

            self.screen_shot('creditcard')
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

            self.screen_shot('creditcard_msite')

    def fillAddress(self):
        """
        填写购物车页下的地址具体信息
        无跳转
        """
        print("fill_address:填写个人信息")
        (email, password) = gen_email_password()
        # xp_checkout = '//div[text()="Proceed to Checkout"]'
        xp_checkout = '//div[contains(text(),"Check")]'

        xp_email = '//input[@name="email"]'
        xp_name = '//input[@name="name"]'
        xp_streetaddress = '//input[@name="streetAddress1"]'
        xp_city = '//input[@name="city"]'
        xp_zipCode = '//input[@name="zipCode"]'
        xp_phoneNumber = '//input[@name="phoneNumber"]'
        xp_state = '//select[@name="state"]'
        xp_submit_ms = '//button[text()="Submit"]'
        xp_confirm = '//button[text()="Confirm"]'

        self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_checkout)))
        self.wd.find_element_by_xpath(xp_checkout).click()

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
        else:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_confirm)))
            self.wd.find_element_by_xpath(xp_confirm).click()

    def __select_coupon(self, coupon_index=0):
        coupons_num = [3, 5]
        xp_select = '//div[@class="__select"]'
        xp_use = '//div[@class="__use"]'
        xp_coupons = '/html/body/div[2]/div/div[2]/div[2]/div[2]/div[2]/ul/li'
        xp_usenow = './div/div[2]/span'
        xp_input = '//*[@id="root"]/div/div[2]/div/div/div[1]/div/div[4]/div[2]/div[3]/div/div/div/li/div/div[2]/div/div[4]/div/input'
        xp_input_ms = '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[3]/div/div/li/div/div[3]/div/div[3]/div[1]/input'

        item_nums = 1

        xp_select_ms = '//a[@href="/cart/coupons"]'
        xp_coupons_ms = '/html/body/div[2]/div/div[6]/div/div/div[2]/ul/li'

        if not self.msite:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_select)))
            item_nums = self.wd.find_element_by_xpath(xp_input).get_attribute('value')
            self.qty_items(coupons_num[coupon_index] - int(item_nums))

            # self.wd.find_element_by_xpath(xp_select).click()
            # self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_use)))

            # coupons = self.wd.find_elements_by_xpath(xp_coupons)
            # coupons[coupon_index].find_element_by_xpath(xp_usenow).click()
            self.screen_shot('coupon' + str(coupon_index))

        else:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_select_ms)))
            item_nums = self.wd.find_element_by_xpath(xp_input_ms).get_attribute('value')
            self.qty_items(coupons_num[coupon_index] - int(item_nums))

            # self.wd.execute_script("arguments[0].click();", self.wd.find_element_by_xpath(xp_select_ms))
            # self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_use)))

            # coupons = self.wd.find_elements_by_xpath(xp_coupons_ms)
            # self.wd.execute_script("arguments[0].click();", coupons[coupon_index].find_element_by_xpath(xp_usenow))
            self.screen_shot('coupon' + str(coupon_index) + '_ms')

        if coupon_index < len(coupons_num) - 1:
            self.select_coupon(coupon_index + 1)

    def qty_items(self, times):
        xp_add = '//*[@id="root"]/div/div[2]/div/div/div[1]/div/div[4]/div[2]/div[2]/div/div/div/li/div/div[2]/div/div[4]/div/span[2]'
        xp_minus = '//*[@id="root"]/div/div[2]/div/div/div[1]/div/div[4]/div[2]/div[2]/div/div/div/li/div/div[2]/div/div[4]/div/span[1]'
        xp_add_ms = '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[3]/div/div/li/div/div[3]/div/div[3]/div[1]/span[2]'
        xp_minus_ms = '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[3]/div/div/li/div/div[3]/div/div[3]/div[1]/span[1]'

        if not self.msite:
            xp_op = xp_add
            if times < 0:
                xp_op = xp_minus
                times = -times

        else:
            xp_op = xp_add_ms
            if times < 0:
                xp_op = xp_minus_ms
                times = -times

        self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_op)))

        for i in range(times):
            self.wd.find_element_by_xpath(xp_op).click()
            time.sleep(0.5)

    def screen_shot(self, name, element=None):
        # width = self.wd.execute_script("return document.documentElement.scrollWidth")
        # height = self.wd.execute_script("return document.documentElement.scrollHeight")
        # self.wd.maximize_window()
        time.sleep(1)
        if self.msite:
            name += '_ms'
        if element is None:
            self.wd.save_screenshot(name + '.png')
        else:
            element.screenshot(name + '.png')
        print('图片已保存：' + name + '.png')

    def enterLogin(self):
        print('enter_login:跳转登录界面')
        cs_login = 'span[class="iconfont"]'
        cs_login_email = 'input#email'
        try:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_login)))
            self.wd.find_element_by_css_selector(cs_login).click()

            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_login_email)))
        except:
            self.wd.get(self.web + '/i/login')
            print('跳转成功')

    def enterIndex(self):
        xp_banner = '//*[@id="i-collection-events"]/li[2]/a/img'
        self.wd.get(self.web)
        self.__pop_up_index()

        # if self.msite:
        #     self.longwait.until(EC.element_to_be_clickable((By.XPATH, xp_banner)))

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

    def __afterpay(self):
        cs_cls = 'a.stjr-review-checkout-widget-body__close'
        try:
            self.longwait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_cls)))
            self.wd.find_element_by_css_selector(cs_cls).click()
        except:
            print('未完成支付')

    def enterDetail_swORindex2itemDetail_pcms(self):
        xp_trending = '//a[@data-type="Trending Now"]'
        xp_item = '//*[@id="filter-products"]/div[1]/figure/a/div/img'

        xp_item_ms = '//div[@class="xi-list-product"]'

        if not self.msite:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_trending)))
            self.wd.find_element_by_xpath(xp_trending).click()

            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_item)))
            self.wd.find_element_by_xpath(xp_item).click()
        else:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_item_ms)))
            element = self.wd.find_element_by_xpath(xp_item_ms)
            self.wd.execute_script("arguments[0].scrollIntoView(true);", element)
            element.click()

    def enterItemPop_trendingORindex2itemPop_pcms(self):
        xp_trending = '//a[@data-type="Trending Now"]'
        xp_item = '//*[@id="filter-products"]/div[1]/figure/a/div/img'
        xp_addchart = '//*[@id="filter-products"]/div[1]/figure/a/div/div[2]'

        xp_addcart_ms = '//*[@id="ninimour-black-friday"]/div[3]/div[1]/ul/li[1]/div/a/figure/figcaption/div/div[2]/span'

        if not self.msite:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_trending)))
            self.wd.find_element_by_xpath(xp_trending).click()

            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_item)))
            self.wd.execute_script("window.scrollTo(0,100)")
            item = self.wd.find_element_by_xpath(xp_item)
            ActionChains(self.wd).move_to_element(item).perform()

            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_addchart)))
            self.wd.find_element_by_xpath(xp_addchart).click()
        else:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_addcart_ms)))
            element = self.wd.find_element_by_xpath(xp_addcart_ms)
            # self.wd.execute_script("arguments[0].scrollIntoView(true);", element)
            self.wd.execute_script("window.scrollTo(0,400)")

            element.click()

    def selectItemAttrPopAndAddCart(self):
        cs_colors = 'ul.p-colors li'
        cs_sizes = 'ul.p-sizes > li'
        cs_addchart = 'span.x-product-buy'

        self.longwait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_colors)))
        colors = self.wd.find_elements_by_css_selector(cs_colors)
        if len(colors) > 1:
            colors[1].click()
        else:
            colors[0].click()
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_sizes)))
        sizes = self.wd.find_elements_by_css_selector(cs_sizes)
        if len(sizes) > 1:
            sizes[1].click()
        else:
            sizes[0].click()

        self.screen_shot("item")

        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_addchart)))
        self.wd.find_element_by_css_selector(cs_addchart).click()

    def selectAttrDetail(self):
        cs_colors = 'ul.xp-colors li'
        cs_sizes = 'ul#sizes > li'

        self.longwait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_colors)))
        colors = self.wd.find_elements_by_css_selector(cs_colors)
        if len(colors) > 1:
            colors[1].click()
        else:
            colors[0].click()
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cs_sizes)))
        sizes = self.wd.find_elements_by_css_selector(cs_sizes)
        if len(sizes) > 1:
            sizes[1].click()
        else:
            sizes[0].click()

    def enterCart(self):
        self.wd.get(web + '/cart')

    def long_screen_shot(self, window, element, name):
        print(window.size['height'])
        print(element.size['height'])

        ws = window.size['height']
        es = element.size['height']

        if es < ws * 2:
            element.screenshot(name + '0.png')
            js = "var q=document.documentElement.scrollTop=10000"
            self.wd.execute_script(js)
            element.screenshot(name + '1.png')

    def shotsSelectDescribe(self):
        '''详情页信息截图'''

        if not self.msite:
            xp_ship_button = '//*[@id="view-more-shipping"]/div/div[2]'
            iframe_ship = '//iframe[@src="/fs/return-policy"]'
            xp_return_button = '//*[@id="view-more-return"]/div/div[2]'

            xp_size_button = '//*[@id="view-more-size"]/div/div[2]'
            xp_detail_button = '//*[@id="description-open"]/div[2]'


        else:
            xp_ship_iframe = '//iframe[@src="/fs/shipping-policy"]'
            xp_ship_button='//*[@id="view-more-shipping"]/div/div[2]'
            xp_ship='/html/body'
            xp_return_iframe='//iframe[@src="/fs/return-policy"]'
            xp_return_button='//*[@id="view-more-return"]/div/div[2]'
            xp_return='/html/body'
            # xp_iframe_size = '//iframe[@src="/f/mobile/size?productId=7ecc313b-0d9f-456e-ab21-000a12c73ffb"]'
            # xp_size_button='//*[@id="view-more-size"]/div/div[2]'
            xp_detail_button='//*[@id="description-open"]/div[2]'
            xp_detail='//*[@id="description-fixed"]'

            self.wd.find_element_by_xpath(xp_ship_button).click()
            frame = self.wd.find_element_by_xpath(xp_ship_iframe)
            self.wd.switch_to.frame(frame)
            self.screen_shot(self.wd.find_element_by_xpath(xp_ship),'ship')
            self.wd.switch_to.default_content()

            self.wd.find_element_by_xpath(xp_return_button).click()
            frame = self.wd.find_element_by_xpath(xp_return_iframe)
            self.wd.switch_to.frame(frame)
            self.screen_shot(self.wd.find_element_by_xpath(xp_return), 'return')
            self.wd.switch_to.default_content()

            self.wd.find_element_by_xpath(xp_detail_button).click()
            self.screen_shot(self.wd.find_element_by_xpath(xp_detail), 'detail')


    def shotEditAddress(self):
        xp_edit = '//*[@id="root"]/div/div[2]/div/div/div[1]/div/div[1]/div/div[2]/div/div/div/address/div[2]/span[2]/span[2]/span'
        xp_edit_ms = '//a[@href="/cart/address"]/span'
        xp_input = '//input[@name="unit"]'
        xp_save = '//button[text()="Save"]'
        xp_submit_ms = '//Button[text()="Submit"]'

        xp_address = '//*[@id="root"]/div/div[2]/div/div/div[1]/div/div[1]/div/div[2]/div/div/div'

        if not self.msite:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_edit)))
            self.wd.find_element_by_xpath(xp_edit).click()

            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_input)))
            self.wd.find_element_by_xpath(xp_input).send_keys('EEEEEEEEEE')

            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_save)))
            self.wd.find_element_by_xpath(xp_save).click()

            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_edit)))
            self.screen_shot('address',self.wd.find_element_by_xpath(xp_address))
        else:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_edit_ms)))
            self.wd.find_element_by_xpath(xp_edit_ms).click()

            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_input)))
            self.wd.find_element_by_xpath(xp_input).send_keys('EEEEEEEEEE')

            self.wait.until(EC.element_to_be_clickable((By.XPATH, xp_submit_ms)))
            self.wd.find_element_by_xpath(xp_submit_ms).click()

            self.screen_shot('address')

    def shotsQtyForCoupon(self):
        '''所有coupon优惠组合截图'''
        xp_unit_price = '//*[@id="root"]/div/div[2]/div/div/div[1]/div/div[4]/div[2]/div[2]/div/div/div/li/div/div[2]/div/div[5]/div/span/span'
        xp_sum = '//*[@id="root"]/div/div[2]/div/div/div[1]/div/div[4]/div[2]/div[2]/div/div/div/li/div/div[2]/div/div[6]/span'
        coupon_type = 'sum'  # 两种类型，num和sum
        coupons = [79, 129, 199]
        js = "var q=document.documentElement.scrollTop=100000"
        self.wd.execute_script(js)

        if coupon_type is 'sum':
            for coupon in coupons:
                unit_price = float(self.wd.find_element_by_xpath(xp_unit_price).text[1:])
                sum = float(self.wd.find_element_by_xpath(xp_sum).text[1:])
                qty_times = math.ceil((coupon - sum) / unit_price)
                if qty_times <= 0:
                    qty_times -= 1
                self.qty_items(qty_times)
                self.screen_shot('coupon' + str(coupon))

    def find_element_by_xpath(self,xpath):
        try:
            element=self.wd.find_element_by_xpath(xpath)

            element.screenshot('locate.png')
            return element
        except:
            return None


    def t(self):
        self.wd.execute_script("window.scrollTo(0,50)")

        pass


def gen_email_password():
    email = '1'
    password = ''
    for i in range(8):
        email += str(random.randint(0, 10))
        password += str(random.randint(0, 10))
    email += '@gmail12.com'

    return (email, password)

# def test_main(email, password):
#     # try:
#     #     test_main_1(ms=False)
#     # except Exception:
#     #     print('test_main_1 fail')
#     #     traceback.print_exc()
#
#     try:
#         test_main_2(email, password, ms=False)
#     except Exception:
#         print('test_main_2 fail')
#         traceback.print_exc()
#
#
# def test_main_1(ms=False):
#     chicme = Se_chicme(msite=ms)
#     chicme.add_chart()
#     chicme.fill_address()
#     chicme.select_coupon()
#     chicme.pay_paypal()
#     chicme.wd.save_screenshot('test1.1.png')
#
#     # 1.2
#     chicme.enter_index()
#     chicme.add_chart(haveCache=True)
#     # chicme.fill_address()
#     chicme.pay_creditcard('4000020951595032', haveCache=True)
#     chicme.wd.save_screenshot('test1.2.png')
#
#     # 1.3
#     chicme2 = Se_chicme(msite=ms)
#     chicme2.add_chart()
#     chicme2.fill_address()
#     chicme2.pay_creditcard('4002812166761203')
#     chicme2.wd.save_screenshot('test1.3.png')
#
#
# def test_main_2(email, password, ms):
#     chicme = Se_chicme(msite=ms)
#     chicme.enter_login()
#     chicme.regist(email, password, 'a', 'b')
#     # chicme.logout()
#     # chicme.enter_login()
#     # chicme.login(email, password)
#     chicme.add_chart()
#     chicme.fill_address()
#     chicme.pay_paypal()
#     chicme.wd.get(web + '/cart/checkout')
#     chicme.pay_creditcard('4000020951595032')
#     chicme.wd.get(web + '/cart/checkout')
#     chicme.pay_creditcard('4002812166761203', haveCache=True)
#
#
# if __name__ == '__main__':
#     email, password = gen_email_password()
#     test_main(email, password)
