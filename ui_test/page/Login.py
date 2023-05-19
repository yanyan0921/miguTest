import sys


sys.path.append("../..")
sys.path.append("../../")
from ui_test.page.BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Login(BasePage):
    # 定位元素
    username = '//*[@id="app"]/div/div[2]/div/form/div[1]/div/div/input'
    password = '//*[@id="app"]/div/div[2]/div/form/div[2]/div/div[1]/input'
    sign_in = '//*[@id="app"]/div/div[2]/div/form/button'
    picture = '#img'

    def init_page(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.username)))

    def sign(self, username, pwd):
        name = self.driver.find_element(By.XPATH, self.username)
        name.send_keys(username)
        password = self.driver.find_element(By.XPATH, self.password)
        password.send_keys(pwd)
        submit = self.driver.find_element(By.XPATH, self.sign_in)
        submit.click()
