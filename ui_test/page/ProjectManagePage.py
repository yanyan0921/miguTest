from ui_test.page.BasePage import BasePage
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ui_test.page.BasePage import BasePage

class ProjectManagePage(BasePage):

    # 定位元素
    project_manage_menu = '//*[@id="app"]/section/section/aside/ul/li[3]/span'
    # 项目相关元素
    project_create_button = '//*[@id="app"]/section/section/main/div[2]/div/h2/div[2]/button'
    project_search_input = '//*[@id="app"]/section/section/main/div[2]/div/div/div/div/div[1]/div/input'
    project_save_button = '//*[@id="app"]/section/section/main/div[2]/div/h2/div[2]/button[1]'
    project_name_div = '//*[@id="app"]/section/section/main/div[2]/div/div/div/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[1]/div'
    project_view_button = '//*[@id="app"]/section/section/main/div[2]/div/div/div/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[5]/div/button[2]'
    project_del_button = '//*[@id="app"]/section/section/main/div[2]/div/div/div/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[5]/div/button[1]'
    project_del_confirm_button = '/html/body/div[3]/div/div/div[3]/button[2]'  
    project_info_tab = '//*[@id="tab-pro3"]'
    project_name_input = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div/div[2]/div[2]/div/div[1]/input'
    project_update_name_input = '//*[@id="pane-pro3"]/div/form/div/div/div[2]/div[2]/div/div/input'
    project_description_input = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div/div[2]/div[3]/div/div/textarea'
    project_info_save_button = '//*[@id="pane-pro3"]/div/form/div/div/div[1]/div/button'
    no_data_div = '//*[@id="app"]/section/section/main/div[2]/div/div/div/div/div[2]/div[1]/div[3]/div/div[1]/div/div/span/div'

    # 初始化项目管理页面
    def init_project_manage_page(self):

        WebDriverWait(self.driver,15).until(EC.visibility_of_element_located((By.XPATH,self.project_manage_menu)))
        project_manage_menu = self.driver.find_element(By.XPATH,self.project_manage_menu)
        project_manage_menu.click()


    # 创建项目
    def create_project(self,project_name, project_description):

        # 点击创建项目按钮
        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,self.project_create_button)))
        project_create_button = self.driver.find_element(By.XPATH, self.project_create_button)
        project_create_button.click()
        # 输入项目名称
        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,self.project_name_input)))
        project_name_input = self.driver.find_element(By.XPATH, self.project_name_input)
        project_name_input.click()
        project_name_input.send_keys(project_name)
        # 输入项目简介
        project_description_input = self.driver.find_element(By.XPATH, self.project_description_input)
        project_description_input.click()
        project_description_input.send_keys(project_description)
        # 点击立即创建按钮
        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,self.project_create_button)))
        project_save_button = self.driver.find_element(By.XPATH, self.project_save_button)
        project_save_button.click()


    # 搜索项目
    def search_project(self, project_name):

        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,self.project_search_input)))
        project_search_input = self.driver.find_element(By.XPATH, self.project_search_input)
        project_search_input.click()
        project_search_input.clear()
        project_search_input.send_keys(project_name, Keys.TAB)
        project_name_div_text = self.driver.find_element(By.XPATH, self.project_name_div).text.strip()
        assert project_name_div_text != ''


    # 进入项目详情页面
    def enter_project_details_page(self):
        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,self.project_view_button)))
        project_view_button = self.driver.find_element(By.XPATH, self.project_view_button)
        project_view_button.click()


    # 编辑项目信息
    def edit_project_info(self,update_project_name):

        # 切换到项目信息tab
        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,self.project_info_tab)))
        project_info_tab = self.driver.find_element(By.XPATH, self.project_info_tab)
        project_info_tab.click()
        # 输入项目名称
        project_update_name_input = self.driver.find_element(By.XPATH, self.project_update_name_input)
        project_update_name_input.click()
        project_update_name_input.clear()
        sleep(2)
        project_update_name_input.send_keys(update_project_name)
        # 点击保存修改
        project_info_save_button = self.driver.find_element(By.XPATH, self.project_info_save_button)
        project_info_save_button.click()


    # 删除项目
    def del_project(self):
        
        project_del_button = self.driver.find_element(By.XPATH, self.project_del_button)
        project_del_button.click()
        project_del_confirm_button = self.driver.find_element(By.XPATH, self.project_del_confirm_button)
        project_del_confirm_button.click()
        


    # 搜索项目是否删除成功
    def search_deleted_project(self, update_project_name):

        project_search_input = self.driver.find_element(By.XPATH, self.project_search_input)
        project_search_input.click()
        project_search_input.clear()
        project_search_input.send_keys(update_project_name, Keys.TAB)
        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,self.no_data_div)))
        no_data_div_text = self.driver.find_element(By.XPATH, self.no_data_div).text.strip()
        assert no_data_div_text == '暂无数据'