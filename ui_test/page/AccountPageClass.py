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

    edit_button = '//*[@id="app"]/section/section/main/div[2]/div/div[1]/div/div/div[3]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[7]/div/button[2]'
    account_name_input = '//*[@id="app"]/section/section/main/div[2]/div/div[1]/div/div[2]/form/div[1]/div/div/input'
    save_button = '//*[@id="app"]/section/section/main/div[2]/div/h2/div[2]/button[2]'
    save_msg = "//p[contains(text(),'恭喜您，更新成功~')]"

    create_org_button = '//*[@id="app"]/section/section/main/div[2]/div/div[2]/div/div[1]/div[1]/button'
    choose_orgs = '//*[@id="app"]/section/section/main/div[2]/div/div[2]/div/div[2]/div/div/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div/div/div/div/div/input'
    choose_roles = '//*[@id="app"]/section/section/main/div[2]/div/div[2]/div/div[2]/div/div/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[3]/div/div/div/div/div/input'
    tag = '//*[@id="app"]/section/section/main/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div[1]/div[2]/table/thead/tr/th[1]/div/div'
    dropdown_li = '//*[@id="el-popper-container-3830"]/div[5]/div/div/div[1]/ul/li'

    remove_connect = '//*[@id="app"]/section/section/main/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[4]/div/div/button/span'

    def init_page(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.new_account_button)))

    def new_account(self):
        new_account_button = self.driver.find_element(By.XPATH, self.new_account_button)
        new_account_button.click()

    def search_account(self, account_info):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.search__txt)))

        search__txt = self.driver.find_element(By.XPATH, self.search__txt)
        search__txt.send_keys(account_info, Keys.TAB)

    def delete_searched_account(self, account_info):
        searched_account_name = self.driver.find_element(By.XPATH, self.searched_account_name)
        account_name = searched_account_name.text.strip()
        logger.info("the delete account's name: " + account_name)
        assert account_name == account_info
        target_account_delete = self.driver.find_element(By.XPATH, self.target_account_delete)
        target_account_delete.click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.confirm_button)))
        confirm_button = self.driver.find_element(By.XPATH, self.confirm_button)
        confirm_button.click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.delete_success_message)))
        delete_success_message = self.driver.find_element(By.XPATH, self.delete_success_message).text.strip()
        logger.info("the delete success's msg: " + delete_success_message)
        assert delete_success_message != ''

    def edit_account_info(self, update_name):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.edit_button)))
        edit_button = self.driver.find_element(By.XPATH, self.edit_button)
        edit_button.click()

        account_name_input = self.driver.find_element(By.XPATH, self.account_name_input)
        account_name_input.clear()
        account_name_input.send_keys(update_name)

        save_button = self.driver.find_element(By.XPATH, self.save_button)
        save_button.click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.save_msg)))
        save_msg = self.driver.find_element(By.XPATH, self.save_msg).text.strip()
        # logger.info("the save success's msg: " + save_succcess_msg)
        # assert save_succcess_msg != ''
        return save_msg

    def org_connect(self, add_org_connect):
        # 验证添加组织关联
        x = 0
        m = True
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.edit_button)))
        edit_button = self.driver.find_element(By.XPATH, self.edit_button)
        edit_button.click()
        create_org_button = self.driver.finf_element(By.XPATH, self.create_org_button)
        for i in range(add_org_connect):
            create_org_button.click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.tag)))
        choose_orgs = self.driver.find_elements(By.XPATH, self.choose_orgs)
        # 组织选择
        for i in choose_orgs:
            x += 1
            i.click()
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, self.dropdown_li)))
            dropdown_li = self.driver.finf_elements(By.XPATH, self.dropdown_li)
            # for x in range(3):
            #     dropdown_li[x].click()
            dropdown_li[x].click()
        choose_roles = self.driver.finf_elements(By.XPATH, self.choose_roles)
        # 角色选择，因为交替选择，故点击新增组织大于6，将提示开发者同时关联最多3个组织
        for h in choose_roles:
            h.click()
            m = not m
            if m:
                choose_roles[1].click()
            else:
                choose_roles[2].click()
            break
        modify_msg = self.driver.switch_to.alert.text
        # 清理数据，移除组织关联
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.remove_connect)))
        remove_connect = self.driver.finf_element(By.XPATH, self.remove_connect)
        for k in range(add_org_connect):
            remove_connect.click()

        return modify_msg

