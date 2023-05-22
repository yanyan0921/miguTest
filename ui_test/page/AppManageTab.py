from ui_test.page.BasePage import BasePage
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AppManageTab(BasePage):
    # 定位元素
    app_manage_tab = '//*[@id="tab-pro0"]'
    app_name_input = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div[1]/div[2]/div[2]/div/div[1]/input'
    server_package_select = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div[3]/div[2]/div[2]/div/div/div/div/div/input'
    server_packages_li = 'el-select-dropdown__item'
    server_launch_file_path = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div[3]/div[2]/div[3]/div/div/input'
    server_launch_params = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div[3]/div[2]/div[4]/div/div/input'
    server_pool_input = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div[3]/div[2]/div[5]/div/div/div/div/input'
    server_pools_li = 'el-select-dropdown__item'
    merger_package_select = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div[5]/div[2]/div[2]/div/div/div/div/div/input'
    merger_packages_li = 'el-select-dropdown__item'
    merger_launch_file_path = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div[5]/div[2]/div[3]/div/div/input'
    merger_launch_params = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div[5]/div[2]/div[4]/div/div/input'
    merger_pool_input = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div[5]/div[2]/div[5]/div/div/div/div/input'
    merger_pools_li = 'el-select-dropdown__item'
    new_app_button = '//*[@id="pane-pro0"]/div/div[1]/div/div/div[1]/button/span'
    app_create_button = '//*[@id="app"]/section/section/main/div[2]/div/h2/div[2]/button[2]'
    app_search_input = '//*[@id="pane-pro0"]/div/div[1]/div/div/div[1]/div/input'
    app_name_text_div = '//*[@id="pane-pro0"]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[1]/div'
    app_operate_icon = '//*[@id="pane-pro0"]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[7]/div/div/div/span'
    operation_list_ul = '//*[@class="el-dropdown-menu el-dropdown-menu--default"]'
    app_edit_option = '//li[text()=" 编辑 "]'
    app_edit_save_button = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div[1]/div[1]/div/div/button[2]'
    app_del_option = '//li[text()=" 删除 "]'
    app_del_confirm = '/html/body/div[3]/div/div/div[3]/button[2]'
    no_data_text_div = '//*[@id="pane-pro0"]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/div[1]/div/div/span/div'

    # 初始化App管理tab
    def init_app_manage_tab(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.app_manage_tab)))
        app_manage_tab = self.driver.find_element(By.XPATH, self.app_manage_tab)
        app_manage_tab.click()

    # 创建App
    def create_app(self, app_name, package, launch_file_path, launch_params, pool_name):
        # 点击创建按钮
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.new_app_button)))
        new_app_button = self.driver.find_element(By.XPATH, self.new_app_button)
        new_app_button.click()
        # 输入App名称
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.app_name_input)))
        app_name_input = self.driver.find_element(By.XPATH, self.app_name_input)
        app_name_input.click()
        app_name_input.send_keys(app_name)

        # 选择server的游戏包
        server_package = self.driver.find_element(By.XPATH, self.server_package_select)
        server_package.click()
        server_package.send_keys(package)
        sleep(2)
        server_packages_li = self.driver.find_elements(By.CLASS_NAME, self.server_packages_li)
        server_packages_li[0].click()
        # 输入server的启动文件路径
        server_launch_file_path = self.driver.find_element(By.XPATH, self.server_launch_file_path)
        server_launch_file_path.click()
        server_launch_file_path.send_keys(launch_file_path)
        # 输入server的启动参数
        server_launch_params = self.driver.find_element(By.XPATH, self.server_launch_params)
        server_launch_params.click()
        server_launch_params.send_keys(launch_params)
        # 选择资源池
        server_pool_input = self.driver.find_element(By.XPATH, self.server_pool_input)
        server_pool_input.click()
        sleep(1)
        server_pool_input.send_keys(pool_name, Keys.UP, Keys.ENTER)

        # 输入merger的启动文件路径
        merger_launch_file_path = self.driver.find_element(By.XPATH, self.merger_launch_file_path)
        merger_launch_file_path.click()
        merger_launch_file_path.send_keys(launch_file_path)
        # 输入merger的启动参数
        merger_launch_params = self.driver.find_element(By.XPATH, self.merger_launch_params)
        merger_launch_params.click()
        merger_launch_params.send_keys(launch_params)
        # 选择资源池
        merger_pool_input = self.driver.find_element(By.XPATH, self.merger_pool_input)
        merger_pool_input.click()
        merger_pool_input.send_keys(pool_name, Keys.UP, Keys.ENTER)
        sleep(2)
        # 选择merger游戏包
        merger_package = self.driver.find_element(By.XPATH, self.merger_package_select)
        merger_package.click()
        sleep(2)
        merger_package.send_keys(package, Keys.DOWN, Keys.ENTER)
        sleep(2)

        # 点击创建按钮
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, self.app_create_button)))
        app_create_button = self.driver.find_element(By.XPATH, self.app_create_button)
        app_create_button.click()

    # 搜索App是否创建成功
    def search_app(self, app_name):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.app_search_input)))
        app_search_input = self.driver.find_element(By.XPATH, self.app_search_input)
        app_search_input.click()
        app_search_input.send_keys(app_name, Keys.TAB)
        app_name_text_div = self.driver.find_element(By.XPATH, self.app_name_text_div).text.strip()
        assert app_name_text_div != ''

    # 编辑App
    def edit_app_info(self, update_app_name):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.app_operate_icon)))
        app_operate_icon = self.driver.find_element(By.XPATH, self.app_operate_icon)
        app_operate_icon.click()
        operation_list_ul = self.driver.find_element(By.XPATH, self.operation_list_ul)
        sleep(2)
        app_edit_option = operation_list_ul.find_element(By.XPATH, self.app_edit_option)
        app_edit_option.click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.app_name_input)))
        app_name_input = self.driver.find_element(By.XPATH, self.app_name_input)
        app_name_input.click()
        app_name_input.clear()
        app_name_input.send_keys(update_app_name)
        app_edit_save_button = self.driver.find_element(By.XPATH, self.app_edit_save_button)
        app_edit_save_button.click()

    # 删除App
    def del_app(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.app_operate_icon)))
        app_operate_icon = self.driver.find_element(By.XPATH, self.app_operate_icon)
        app_operate_icon.click()
        operation_list_ul = self.driver.find_element(By.XPATH, self.operation_list_ul)
        sleep(2)
        app_del_option = operation_list_ul.find_element(By.XPATH, self.app_del_option)
        app_del_option.click()
        sleep(2)
        app_del_confirm = self.driver.find_element(By.XPATH, self.app_del_confirm)
        app_del_confirm.click()

    # 搜索App是否删除成功
    def search_deleted_app(self, update_app_name):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.app_search_input)))
        app_search_input = self.driver.find_element(By.XPATH, self.app_search_input)
        app_search_input.click()
        app_search_input.clear()
        app_search_input.send_keys(update_app_name, Keys.TAB)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.no_data_text_div)))
        no_data_text_div = self.driver.find_element(By.XPATH, self.no_data_text_div).text.strip()
        assert no_data_text_div == '暂无数据'
