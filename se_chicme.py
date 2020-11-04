from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

        self.wd.get('https://www.chicme.com')

    def login(self,email,password):
        locator=(By.XPATH, '//input[@id="email"]')
        cls_xpath='//div[@class="cls"]/i'

        self.wait.until(EC.element_to_be_clickable((By.XPATH, cls_xpath)))

        self.wd.find_element_by_xpath(cls_xpath).click()
        self.wd.find_element_by_xpath('//span[@class="iconfont"]').click()

        self.wait.until(EC.element_to_be_clickable(locator))

        self.wd.find_element_by_xpath('//input[@id="email"]').send_keys(email)
        self.wd.find_element_by_xpath('//input[@id="password"]').send_keys(password)
        self.wd.find_element_by_xpath('//button[@id="btns"]').click()



if __name__ == '__main__':
    chicme = Se_chicme()
    chicme.login('123@gmail','123')
