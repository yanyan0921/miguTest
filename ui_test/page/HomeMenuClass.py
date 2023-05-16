from ui_test.page.BasePage import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class HomeMenuClass(BasePage):
    # def __init__(self, driver):
    #     super().__init__(driver)
    #     self.driver = driver
        
    # 定位元素
    account_manage = '//*[@id="app"]/section/section/aside/ul/li[1]/span'
    resource_list = '//*[@id="app"]/section/section/aside/ul/li[2]/span'
    project_manage = '//*[@id="app"]/section/section/aside/ul/li[3]/span'

    def init_page(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                      (By.XPATH, self.account_manage)))

    def choose_account_manage(self):

        account_manage = self.driver.find_element(By.XPATH,self.account_manage)
        account_manage.click()

    def choose_resource_list(self):

        resource_list = self.driver.find_element(By.XPATH,self.resource_list)
        resource_list.click()

    def choose_project_manage(self):

        project_manage = self.driver.find_element(By.XPATH,self.project_manage)
        project_manage.click()

