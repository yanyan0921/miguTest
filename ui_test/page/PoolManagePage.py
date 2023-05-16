from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ui_test.page.BasePage import BasePage

class PoolManagePage(BasePage):

    # 定位元素
    pool_manage_menu = '//*[@id="app"]/section/section/aside/ul/li[2]/span'
    create_pool_button = '//*[@id="app"]/section/section/main/div[2]/div/div/div/div/div[1]/button'
    pool_name_input = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div/div[2]/div[2]/div/div/input'
    pool_type_input = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div/div[2]/div[3]/div/div/div/div/div/input'
    pool_type = "//span[contains(text(),'弹性')]"
    pool_configuration_input = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div/div[2]/div[4]/div[1]/div/div/div/div/input'
    pool_configuration = "//span[contains(text(),'PUB_3060_弹性')]"
    pool_configuration_number = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div/div[2]/div[4]/div[2]/div/div/div/input'
    pool_description = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div/div[2]/div[5]/div/div/textarea'
    create_button = '//*[@id="app"]/section/section/main/div[2]/div/h2/div[2]/button[1]'
    search_input = '//*[@id="app"]/section/section/main/div[2]/div/div/div/div/div[1]/div/input'
    pool_name_div = '//*[@id="app"]/section/section/main/div[2]/div/div/div/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div'
    del_button = '//*[@id="app"]/section/section/main/div[2]/div/div/div/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[7]/div/button[1]'  
    confirm_del_button = '/html/body/div[3]/div/div/div[3]/button[2]'
    no_data_div = '//*[@id="app"]/section/section/main/div[2]/div/div/div/div/div[2]/div[1]/div[3]/div/div[1]/div/div/span/div'  
    edit_info_button = '//*[@id="app"]/section/section/main/div[2]/div/div/div/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[7]/div/button[2]'
    save_update_button = '//*[@id="app"]/section/section/main/div[2]/div/h2/div[2]/button[1]'
    
    # 初始化资源池列表
    def init_page(self):

        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,self.pool_manage_menu)))
        pool_manage_menu = self.driver.find_element(By.XPATH,self.pool_manage_menu)
        pool_manage_menu.click()
        


    # 创建资源池
    def create_pool(self):
        WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.XPATH,self.create_pool_button)))
        create_pool_button = self.driver.find_element(By.XPATH,self.create_pool_button)
        create_pool_button.click()


    # 输入资源池信息
    def input_pool_info(self, pool_name, pool_type_value, configuration, configuration_number, descriptions):

        WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.XPATH,self.pool_name_input)))
        # 输入资源池名称
        pool_name_input = self.driver.find_element(By.XPATH, self.pool_name_input)
        pool_name_input.click()
        pool_name_input.send_keys(pool_name)

        # 输入资源池类型
        pool_type_input = self.driver.find_element(By.XPATH,self.pool_type_input)
        pool_type_input.click()
        pool_type_input.send_keys(pool_type_value)

        # 点击下拉框选择资源池类型
        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH, self.pool_type)))
        pool_type1 = self.driver.find_element(By.XPATH,self.pool_type)
        pool_type1.click()

        # 输入资源配置
        pool_configuration_input = self.driver.find_element(By.XPATH,self.pool_configuration_input)
        pool_configuration_input.click()
        pool_configuration_input.send_keys(configuration)

        # 点击下拉框选择资源配置
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.pool_configuration)))
        pool_configuration = self.driver.find_element(By.XPATH,self.pool_configuration)
        pool_configuration.click()

        # 输入资源配置数量
        pool_configuration_number = self.driver.find_element(By.XPATH,self.pool_configuration_number)
        pool_configuration_number.click()
        pool_configuration_number.clear()
        pool_configuration_number.send_keys(configuration_number)
        

        # 输入资源池描述
        description = self.driver.find_element(By.XPATH,self.pool_description)
        description.send_keys(descriptions)

        # 点击 立即创建 按钮
        create_button = self.driver.find_element(By.XPATH,self.create_button)
        create_button.click()

    # 搜索创建的资源池是否存在
    def search_pool(self, pool_name):

        WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.XPATH,self.search_input)))
        search_input = self.driver.find_element(By.XPATH, self.search_input)
        search_input.send_keys(pool_name,Keys.TAB)
        pool_name_div_text = self.driver.find_element(By.XPATH, self.pool_name_div).text.strip()
        assert pool_name_div_text != ''

    # 删除创建的资源池
    def del_searched_pool(self):

        WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.XPATH,self.del_button)))
        del_button = self.driver.find_element(By.XPATH, self.del_button)
        del_button.click()
        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,self.confirm_del_button)))
        confirm_del_button = self.driver.find_element(By.XPATH, self.confirm_del_button)
        confirm_del_button.click()

    # 搜索删除的资源池是否已经不存在
    def search_deleted_pool(self, pool_name):

        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,self.search_input)))
        search_input = self.driver.find_element(By.XPATH, self.search_input)
        search_input.clear()
        search_input.send_keys(pool_name,Keys.TAB)
        no_data_div_text = self.driver.find_element(By.XPATH, self.no_data_div).text.strip()
        assert no_data_div_text in '暂无数据'


    # 编辑资源池信息
    def edit_pool_info(self, update_pool_name):

        WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.XPATH,self.edit_info_button)))
        edit_info_button = self.driver.find_element(By.XPATH, self.edit_info_button)
        edit_info_button.click()
        sleep(2)
        # 修改资源池名称
        pool_name_input = self.driver.find_element(By.XPATH, self.pool_name_input)
        pool_name_input.click()
        pool_name_input.clear()
        pool_name_input.send_keys(update_pool_name)
        save_update_button = self.driver.find_element(By.XPATH, self.save_update_button)
        save_update_button.click()






