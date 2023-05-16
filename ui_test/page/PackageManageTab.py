from ui_test.page.BasePage import BasePage
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PackageManageTab(BasePage):

    # 定位元素
    package_manage_tab = '//*[@id="tab-pro1"]'
    upload_game_packege_button = '//*[@id="pane-pro1"]/div/div[1]/div/div/div[1]/button'
    package_version1_num1 = '//*[@id="pane-pro1"]/div/div[2]/div/div/div[2]/div/form/div[1]/div[1]/div/div/div[4]/div/div/div[1]/input'
    package_version1_num2 = '//*[@id="pane-pro1"]/div/div[2]/div/div/div[2]/div/form/div[1]/div[1]/div/div/div[4]/div/div/div[2]/input'
    package_version1_num3 = '//*[@id="pane-pro1"]/div/div[2]/div/div/div[2]/div/form/div[1]/div[1]/div/div/div[4]/div/div/div[3]/input'
    incremental_package_version1_num1 = '//*[@id="pane-pro1"]/div/div[2]/div/div/div[2]/div/form/div[1]/div[1]/div/div/div[5]/div/div/div[1]/input'
    incremental_package_version1_num2 = '//*[@id="pane-pro1"]/div/div[2]/div/div/div[2]/div/form/div[1]/div[1]/div/div/div[5]/div/div/div[2]/input'
    incremental_package_version1_num3 = '//*[@id="pane-pro1"]/div/div[2]/div/div/div[2]/div/form/div[1]/div[1]/div/div/div[5]/div/div/div[3]/input'
    upload_confirm_button = '//*[@id="pane-pro1"]/div/div[2]/div/div/div[3]/span/button'
    search_package_input = '//*[@id="pane-pro1"]/div/div[1]/div/div/div[1]/div/input'
    del_package_button = '//*[@id="pane-pro1"]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[8]/div/button[2]'
    del_confirm_button = '/html/body/div[3]/div/div/div[3]/button[2]'
    package_name_div = '//*[@id="pane-pro1"]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[1]/div'
    no_data_div = '//*[@id="pane-pro1"]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/div[1]/div/div/span/div'
    incremental_radio = '//*[@id="pane-pro1"]/div/div[2]/div/div/div[2]/div/form/div[1]/div[1]/div/div/div[1]/div/label[2]/span[1]'
    original_package_select = '//*[@id="pane-pro1"]/div/div[2]/div/div/div[2]/div/form/div[1]/div[1]/div/div/div[2]/div/div/div/input'
    incremental_package_input = '//*[@id="pane-pro1"]/div/div[2]/div/div/div[2]/div/form/div[1]/div[1]/div/div/div[2]/div[2]/input'
    rename_checkbox = '//*[@id="pane-pro1"]/div/div[2]/div/div/div[2]/div/form/div[1]/div[1]/div/div/div[2]/label/span[1]/span'
    update_package_name_input = '//*[@id="pane-pro1"]/div/div[2]/div/div/div[2]/div/form/div[1]/div[1]/div/div/div[2]/div[2]/input'
    upload_package_input = '//*[@id="pane-pro1"]/div/div[2]/div/div/div[2]/div/form/div[1]/div[1]/div/div/div[2]/div[1]/input'
    incremental_upload_package_input = '//*[@id="pane-pro1"]/div/div[2]/div/div/div[2]/div/form/div[1]/div[1]/div/div/div[3]/div[1]/input'
    upload_success_msg = "//p[contains(text(),'上传成功')]"


    # 初始化游戏包管理tab
    def init_package_manage_tab(self):

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.package_manage_tab)))
        package_manage_tab = self.driver.find_element(By.XPATH, self.package_manage_tab)
        package_manage_tab.click()

    # 普通上传 -- 上传游戏包
    def upload_package(self, package_file_path):

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.upload_game_packege_button)))
        # 点击上传游戏包按钮
        upload_game_packege_button = self.driver.find_element(By.XPATH, self.upload_game_packege_button)
        upload_game_packege_button.click()
        sleep(2)
        upload_package_input = self.driver.find_element(By.XPATH, self.upload_package_input)
        upload_package_input.send_keys(package_file_path)
        sleep(2)
         # 输入游戏包版本号
        package_version1_num1 = self.driver.find_element(By.XPATH, self.package_version1_num1)
        package_version1_num2 = self.driver.find_element(By.XPATH, self.package_version1_num2)
        package_version1_num3 = self.driver.find_element(By.XPATH, self.package_version1_num3)
        package_version1_num1.click()
        package_version1_num1.send_keys('1')
        package_version1_num2.click()
        package_version1_num2.send_keys('1')
        package_version1_num3.click()
        package_version1_num3.send_keys('1')

        upload_confirm_button = self.driver.find_element(By.XPATH, self.upload_confirm_button)
        upload_confirm_button.click()
        
        WebDriverWait(self.driver,60).until(EC.visibility_of_element_located((By.XPATH,self.upload_success_msg)))
        upload_success_msg = self.driver.find_element(By.XPATH, self.upload_success_msg).text.strip()
        assert upload_success_msg != ''



    # 增量上传 -- 上传游戏包
    def upload_incremental_package(self, increment_file_path, orgional_package_name, rename_package):

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.upload_game_packege_button)))
        # 点击上传游戏包按钮
        upload_game_packege_button = self.driver.find_element(By.XPATH, self.upload_game_packege_button)
        upload_game_packege_button.click()
        sleep(2)
        # 勾选增量上传
        incremental_radio = self.driver.find_element(By.XPATH, self.incremental_radio)
        incremental_radio.click()
        # 选择原始包
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.original_package_select)))
        original_package_select = self.driver.find_element(By.XPATH, self.original_package_select)
        original_package_select.click()
        original_package_select.send_keys(orgional_package_name, Keys.DOWN, Keys.ENTER)
        sleep(1)
        # 重命名
        rename_checkbox = self.driver.find_element(By.XPATH, self.rename_checkbox)
        rename_checkbox.click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.incremental_package_input)))
        incremental_package_input = self.driver.find_element(By.XPATH, self.incremental_package_input)
        incremental_package_input.click()
        incremental_package_input.send_keys(rename_package)

        incremental_upload_package_input = self.driver.find_element(By.XPATH, self.incremental_upload_package_input)
        incremental_upload_package_input.send_keys(increment_file_path)
        sleep(2)
        # 输入游戏包版本号
        incremental_package_version1_num1 = self.driver.find_element(By.XPATH, self.incremental_package_version1_num1)
        incremental_package_version1_num2 = self.driver.find_element(By.XPATH, self.incremental_package_version1_num2)
        incremental_package_version1_num3 = self.driver.find_element(By.XPATH, self.incremental_package_version1_num3)
        incremental_package_version1_num1.click()
        incremental_package_version1_num1.send_keys('1')
        incremental_package_version1_num2.click()
        incremental_package_version1_num2.send_keys('1')
        incremental_package_version1_num3.click()
        incremental_package_version1_num3.send_keys('1')

        upload_confirm_button = self.driver.find_element(By.XPATH, self.upload_confirm_button)
        upload_confirm_button.click()
        
        WebDriverWait(self.driver,60).until(EC.visibility_of_element_located((By.XPATH,self.upload_success_msg)))
        upload_success_msg = self.driver.find_element(By.XPATH, self.upload_success_msg).text.strip()
        assert upload_success_msg != ''

    # 搜索游戏包
    def search_package(self, package_name):
        
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.search_package_input)))
        search_package_input = self.driver.find_element(By.XPATH, self.search_package_input)
        search_package_input.click()
        search_package_input.clear()
        search_package_input.send_keys(package_name, Keys.TAB)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.package_name_div)))
        package_name_div_text = self.driver.find_element(By.XPATH, self.package_name_div).text.strip()
        assert package_name_div_text != ''

    # 删除游戏包
    def del_package(self):
        
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.del_package_button)))
        del_package_button = self.driver.find_element(By.XPATH, self.del_package_button)
        del_package_button.click()
        del_confirm_button = self.driver.find_element(By.XPATH, self.del_confirm_button)
        del_confirm_button.click()

    # 搜索游戏包是否删除成功
    def search_deleted_package(self, package_name):

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.search_package_input)))
        search_package_input = self.driver.find_element(By.XPATH, self.search_package_input)
        search_package_input.click()
        search_package_input.clear()
        search_package_input.send_keys(package_name, Keys.TAB)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.no_data_div)))
        no_data_div_text = self.driver.find_element(By.XPATH, self.no_data_div).text.strip()
        assert no_data_div_text != ''
