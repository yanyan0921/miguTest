from ui_test.page.BasePage import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class AdminHomeMenu(BasePage):
    # 定位元素
    org_manage = '//*[@id="app"]/section/section/aside/ul/li[1]/span'
    account__manage = '//*[@id="app"]/section/section/aside/ul/li[2]/span'
    app_manage = '//*[@id="app"]/section/section/aside/ul/li[3]/span'
    resource_manage = '//*[@id="app"]/section/section/aside/ul/li[3]/span'

    def init_page(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.org_manage)))

    def choose_org_manage(self):
        org_manage = self.driver.find_element(By.XPATH,self.org_manage)
        org_manage.click()

    def choose_account__manage(self):
        account__manage = self.driver.find_element(By.XPATH,self.account__manage)
        account__manage.click()

    def choose_app_manage(self):
        app_manage = self.driver.find_element(By.XPATH,self.app_manage)
        app_manage.click()

    def choose_resource_manage(self):
        resource_manage = self.driver.find_element(By.XPATH,self.resource_manage)
        resource_manage.click()


