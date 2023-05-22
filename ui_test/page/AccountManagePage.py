from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ui_test.page.BasePage import BasePage
import time


class AccountManagePage(BasePage):
    # 定位元素
    account_manage_menu = '//*[@id="app"]/section/section/aside/ul/li[1]/span'
    new_account_link_button = '//*[@id="app"]/section/section/main/div[2]/div/div[1]/div/div/div[1]/button'
    dev_account_input = '//*[@id="app"]/section/section/main/div[2]/div/div[2]/div/div/div[2]/div/form/div/div/div[2]/div/div/input'
    link_button = '//*[@id="app"]/section/section/main/div[2]/div/div[2]/div/div/div[3]/span/button[2]'
    account_search = '//*[@id="app"]/section/section/main/div[2]/div/div[1]/div/div/div[1]/div/input'
    cancel_link_button = '//*[@id="app"]/section/section/main/div[2]/div/div[1]/div/div/div[3]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[7]/div/button'
    account_name_div = '//*[@id="app"]/section/section/main/div[2]/div/div[1]/div/div/div[3]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[2]/div'
    nodata_text_div = '//*[@id="app"]/section/section/main/div[2]/div/div[1]/div/div/div[3]/div/div[1]/div[3]/div/div[1]/div/div/span/div'

    dev_account = '//*[@id="el-popper-container-8127"]/div[6]/div/div/div[1]/ul/li[1]'
    # linked_msg = "//p[contains(text(),'用户已在该组织中')]"
    cancel_button = '//*[@id="app"]/section/section/main/div[2]/div/div[2]/div/div/div[3]/span/button[1]'
    confirm_cancel_button = '/html/body/div[3]/div/div/div[3]/button[2]'

    def init_page(self):
        '''
        初始化页面，点击账号管理，进入账号管理页面
        '''
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.account_manage_menu)))
        account_manage_menu = self.driver.find_element(By.XPATH, self.account_manage_menu)
        account_manage_menu.click()

    def link_dev_account(self, dev_account):
        '''
        关联开发者账号的操作
        '''

        # 等待 关联新账号 按钮的出现，并且点击
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.new_account_link_button)))
        new_account_link_button = self.driver.find_element(By.XPATH, self.new_account_link_button)
        new_account_link_button.click()

        # 等待输入开发者账号输入框的出现，点击输入开发者账号，选中目标开发者账号，点击关联按钮
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.dev_account_input)))
        dev_account_input = self.driver.find_element(By.XPATH, self.dev_account_input)
        dev_account_input.click()
        time.sleep(3)
        dev_account_input.send_keys(dev_account)

        # 点击下拉框账号选择关联对象
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.dev_account)))
        dev_account = self.driver.find_element(By.XPATH, self.dev_account)
        dev_account.click()

        link_button = self.driver.find_element(By.XPATH, self.link_button)
        link_button.click()

        # WebDriverWait(self.driver,10).until(EC.visibility_of_element_located(
        #     (By.XPATH, self.linked_msg)))
        # linked_msg = self.driver.find_element(By.XPATH,self.linked_msg).text.strip()
        # if linked_msg == "用户已在该组织中":
        #     cancel_button = self.driver.find_element(By.XPATH,self.cancel_button)
        #     cancel_button.click() 
        # else:
        #     print("执行后续操作")

    def search_linked_dev_accout(self, dev_account):
        '''
        搜索开发者账号是否存在/被关联上
        '''
        account_search = self.driver.find_element(By.XPATH, self.account_search)
        account_search.send_keys(dev_account, Keys.TAB)
        account_name_div_text = self.driver.find_element(By.XPATH, self.account_name_div).text.strip()
        return account_name_div_text
        # assert account_name_div_text != ' '

    def cancel_link_dev_accout(self):
        '''
        取消开发者关联
        '''
        cancel_link_button = self.driver.find_element(By.XPATH, self.cancel_link_button)
        cancel_link_button.click()
        confirm_cancel_button = self.driver.find_element(By.XPATH, self.confirm_cancel_button)
        confirm_cancel_button.click()

    def search_canceled_dev_accout(self, dev_account):
        '''
        搜索开发者账号是否不存在/被取消关联
        '''
        account_search = self.driver.find_element(By.XPATH, self.account_search)
        account_search.click()
        time.sleep(1)
        account_search.clear()
        time.sleep(1)
        account_search.send_keys(dev_account, Keys.TAB)
        time.sleep(3)
        nodata_text = self.driver.find_element(By.XPATH, self.nodata_text_div).text.strip()
        return nodata_text
        # assert nodata_text in '暂无数据'
