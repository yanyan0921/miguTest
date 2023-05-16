from ui_test.page.BasePage import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging

logger = logging.getLogger("main")
logger.setLevel(level=logging.INFO)

class AccountPageClass(BasePage):
    # 定位元素
    new_account_button = '//*[@id="app"]/section/section/main/div[2]/div/div[1]/div/div/div[1]/button'
    search__txt = '//*[@id="app"]/section/section/main/div[2]/div/div/div/div/div[1]/div/input'
    searched_account_name = '//*[@id="app"]/section/section/main/div[2]/div/div/div/div/div[3]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[2]/div'
    target_account_delete = '//*[@id="app"]/section/section/main/div[2]/div/div/div/div/div[3]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[7]/div/button[1]'
    confirm_button = '/html/body/div[3]/div/div/div[3]/button[2]'
    delete_success_message = "//p[contains(text(),'删除成功')]"

    # edit_button = '//*[@id="app"]/section/section/main/div[2]/div/div[1]/div/div/div[3]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[7]/div/button[2]'
    # account_name_input = '//*[@id="app"]/section/section/main/div[2]/div/div[1]/div/div[2]/form/div[1]/div/div/input'
    # save_button = '//*[@id="app"]/section/section/main/div[2]/div/h2/div[2]/button[2]'
    # save_succcess_msg = "//p[contains(text(),'恭喜您，更新成功~')]"

    def init_page(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.new_account_button)))

    def new_account(self):
        new_account_button = self.driver.find_element(By.XPATH,self.new_account_button)
        new_account_button.click()

    def search_account(self, account_info):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.search__txt)))

        search__txt = self.driver.find_element(By.XPATH,self.search__txt)
        search__txt.send_keys(account_info, Keys.TAB)

    def delete_searched_account(self, account_info):
        searched_account_name = self.driver.find_element(By.XPATH,self.searched_account_name)
        account_name = searched_account_name.text.strip()
        logger.info("the delete account's name: " + account_name)
        assert account_name == account_info
        target_account_delete = self.driver.find_element(By.XPATH,self.target_account_delete)
        target_account_delete.click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.confirm_button)))
        confirm_button = self.driver.find_element(By.XPATH,self.confirm_button)
        confirm_button.click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.delete_success_message)))
        delete_success_message = self.driver.find_element(By.XPATH,self.delete_success_message).text.strip()
        logger.info("the delete success's msg: " + delete_success_message)
        assert delete_success_message != ''

    # def edit_account_info(self, update_name):
    #     WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
    #         (By.XPATH, self.edit_button)))
    #     edit_button = self.driver.find_element(By.XPATH,self.edit_button)
    #     edit_button.click()
        
    #     account_name_input = self.driver.find_element(By.XPATH,self.account_name_input)
    #     account_name_input.clear()
    #     account_name_input.send_keys(update_name)

    #     save_button = self.driver.find_element(By.XPATH,self.save_button)
    #     save_button.click()

    #     WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
    #         (By.XPATH, self.save_succcess_msg)))
    #     save_succcess_msg = self.driver.find_element(By.XPATH,self.save_succcess_msg).text.strip()
    #     logger.info("the save success's msg: " + save_succcess_msg)
    #     assert save_succcess_msg != ''













