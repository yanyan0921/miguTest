from ui_test.page.BasePage import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging

logger = logging.getLogger("main")
logger.setLevel(level=logging.INFO)


class OrgPageClass(BasePage):
    # 定位元素
    new_org_button = '//*[@id="app"]/section/section/main/div[2]/div/h2/div[2]/button'
    search__txt = '//*[@id="pane-orgAccount"]/div/div/div[1]/div/input'
    searched_org_name = '//*[@id="pane-orgAccount"]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[1]/div'
    target_org_delete = '//*[@id="pane-orgAccount"]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[4]/div/button[1]'
    new_org_name_txt = '//*[@id="app"]/section/section/main/div[2]/div/div/div[2]/div/div/div[2]/div/form/div/div/div/input'
    new_button = '//*[@id="app"]/section/section/main/div[2]/div/div/div[2]/div/div/div[3]/span/button[2]'
    details_link = '//*[@id="pane-orgAccount"]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[4]/div/button[2]'
    delete_org_button = '//*[@id="pane-orgAccount"]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[4]/div/button[1]'

    searched_org_name_xpath = '//*[@id="pane-orgAccount"]/div[1]/div/div[2]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[1]/div'
    create_success_message = "//p[contains(text(),'创建组织成功')]"
    delete_confirm_button = '/html/body/div[3]/div/div/div[3]/button[2]'
    delete_success_message = "//p[contains(text(),'删除组织成功！')]"
    search_no_data = '//*[@id="pane-orgAccount"]/div[1]/div/div[2]/div/div[1]/div[3]/div/div[1]/div/div/span/div'

    def init_page(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.new_org_button)))

    def new_org(self, new_org_name):
        new_org_button = self.driver.find_element(By.XPATH, self.new_org_button)
        new_org_button.click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.new_org_name_txt)))
        new_org_name_txt = self.driver.find_element(By.XPATH, self.new_org_name_txt)
        new_button = self.driver.find_element(By.XPATH, self.new_button)

        new_org_name_txt.send_keys(new_org_name)
        new_button.click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.create_success_message)))
        create_success_message = self.driver.find_element(By.XPATH, self.create_success_message).text.strip()
        logger.info("the create org success's msg: " + create_success_message)
        assert create_success_message != ''

    def search_org(self, org_name):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.search__txt)))

        search__txt = self.driver.find_element(By.XPATH, self.search__txt)
        search__txt.send_keys(org_name, Keys.TAB)

    def click_org_detail(self, org_info):
        searched_org_name = self.get_search_org_name()
        logger.info("the searched org's name: " + searched_org_name)
        assert org_info in searched_org_name

        details_link = self.driver.find_element(By.XPATH, self.details_link)
        details_link.click()

    def get_search_org_name(self):
        searched_org_name = self.driver.find_element(By.XPATH, self.searched_org_name_xpath)
        return searched_org_name.text.strip()

    def verify_org_edit_success(self, org_name):
        searched_org_name = self.get_search_org_name()
        assert searched_org_name == org_name

    def delete_org(self, org_info):
        searched_org_name = self.get_search_org_name()
        logger.info("the searched org's name: " + searched_org_name)
        # assert org_info in searched_org_name

        delete_org_button = self.driver.find_element(By.XPATH, self.delete_org_button)
        delete_org_button.click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.delete_confirm_button)))
        delete_confirm_button = self.driver.find_element(By.XPATH, self.delete_confirm_button)
        delete_confirm_button.click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.delete_success_message)))

        delete_success_message = self.driver.find_element(By.XPATH, self.delete_success_message).text.strip()
        logger.info("the delete org success's msg: " + delete_success_message)
        return delete_success_message
        # assert delete_success_message != ''

    def verify_deleted_org(self):
        search_no_data = self.driver.find_element(By.XPATH, self.search_no_data).text.strip()
        return search_no_data
        # assert search_no_data == '暂无数据'
