from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ui_test.page.BasePage import BasePage


class AppPublishTab(BasePage):
    # 定位元素
    AppPublishTab = '//*[@id="tab-pro2"]'
    create_publish_app_button = '//*[@id="pane-pro2"]/div/div/div/div/div/div[1]/button'
    publish_app_name_input = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div/div[2]/div[2]/div/div/input'
    game_name_input = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div/div[2]/div[3]/div/div/input'
    description_input = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div/div[2]/div[4]/div/div/textarea'
    image_input = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div/div[2]/div[5]/div/div[1]/div/input'
    save_publish_app_button = '//*[@id="app"]/section/section/main/div[2]/div/h2/div[2]/button[1]'
    search_publish_app_input = '//*[@id="pane-pro2"]/div/div/div/div/div/div[1]/div/input'
    publish_app_name_div = '//*[@id="pane-pro2"]/div/div/div/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[1]/div'
    publish_page_button = '//*[@id="pane-pro2"]/div/div/div/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[4]/div/button[2]'
    create_publish_version_button = '//*[@id="app"]/section/section/main/div[2]/div/div[1]/div/div/div[1]/button'
    publish_description_input = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div[1]/div[2]/div[4]/div/div/textarea'
    publish_version_input = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div[1]/div[2]/div[7]/div/div/input'
    copy_app_input = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div[1]/div[2]/div[6]/div/div/div/div/input'
    copy_appli = '//*[@id="el-popper-container-3671"]/div[3]/div/div/div[1]/ul/li[1]'
    save_publish_version_button = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div[1]/div[1]/div/div/button[2]'
    publish_operation_icon = '//*[@id="app"]/section/section/main/div[2]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[5]/div/div/div/span'
    operation_ul = '//*[@class="el-dropdown-menu el-dropdown-menu--default"]'
    edit_button = '//li[text()=" 编辑 "]'
    save_edit_button = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div[1]/div[1]/div/div/button[2]'
    submit_check_button = '//li[text()=" 提交审核 "]'
    confirm_submit_button = '/html/body/div[3]/div/div/div[3]/button[2]'
    submit_back_button = '//li[text()=" 撤回 "]'
    confirm_submit_back_button = '/html/body/div[3]/div/div/div[3]/button[2]'

    merger_package_input = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div[5]/div[2]/div[2]/div/div/div/div/div/input'
    merger_path_input = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div[5]/div[2]/div[3]/div/div/input'
    merger_launch_parms_input = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div[5]/div[2]/div[4]/div/div/input'
    merger_pool_name_input = '//*[@id="app"]/section/section/main/div[2]/div/form/div/div[5]/div[2]/div[5]/div/div/div/div/input'

    create_version_success_msg = "//p[contains(text(),'应用添加成功！')]"
    edit_version_success_msg = "//p[contains(text(),'应用更新成功！')]"
    submit_check_success_msg = "//p[contains(text(),'已成功提交发布审核！')]"
    submit_back_success_msg = "//p[contains(text(),'已成功撤回发布审核！')]"
    app_detail = '//*[@id="pane-pro2"]/div/div/div/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[4]/div/button[1]/span'
    version_app = '//*[@id="app"]/section/section/main/div[2]/div[1]/form[2]/div/div/div/div[1]/div/div/span'
    game_name = '//*[@id="app"]/section/section/main/div[2]/div[1]/form[2]/div/div/div/div[2]/div/div[2]/div/label'

    # 初始化App发布tab
    def init_page(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.AppPublishTab)))
        AppPublish_Tab = self.driver.find_element(By.XPATH, self.AppPublishTab)
        AppPublish_Tab.click()

    # 创建发布App
    def create_publish_app(self, AppName, GameName, Description, file_path):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.create_publish_app_button)))
        create_publish_app_button = self.driver.find_element(By.XPATH, self.create_publish_app_button)
        create_publish_app_button.click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.publish_app_name_input)))
        publish_app_name_input = self.driver.find_element(By.XPATH, self.publish_app_name_input)
        game_name_input = self.driver.find_element(By.XPATH, self.game_name_input)
        description_input = self.driver.find_element(By.XPATH, self.description_input)
        image_input = self.driver.find_element(By.XPATH, self.image_input)
        save_publish_app_button = self.driver.find_element(By.XPATH, self.save_publish_app_button)

        publish_app_name_input.click()
        publish_app_name_input.send_keys(AppName)
        game_name_input.click()
        game_name_input.send_keys(GameName)
        description_input.click()
        description_input.send_keys(Description)
        image_input.send_keys(file_path)
        sleep(2)
        save_publish_app_button.click()

    # 搜索已创建的发布App
    def search_publish_app(self, AppName):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.search_publish_app_input)))
        search_publish_app_input = self.driver.find_element(By.XPATH, self.search_publish_app_input)
        search_publish_app_input.click()
        search_publish_app_input.send_keys(AppName, Keys.TAB)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.publish_app_name_div)))
        publish_app_name_div = self.driver.find_element(By.XPATH, self.publish_app_name_div).text.strip()
        assert publish_app_name_div != ''

    # 创建新版本 - 自定义包配置
    def create_new_version_customed_config(self, PublishDescription, VersionNumber, Path, LaunchParms, PoolName):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.publish_page_button)))
        publish_page_button = self.driver.find_element(By.XPATH, self.publish_page_button)
        publish_page_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.create_publish_version_button)))
        create_publish_version_button = self.driver.find_element(By.XPATH, self.create_publish_version_button)
        create_publish_version_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.publish_description_input)))
        publish_description_input = self.driver.find_element(By.XPATH, self.publish_description_input)
        publish_description_input.clear()
        publish_description_input.send_keys(PublishDescription)

        publish_version_input = self.driver.find_element(By.XPATH, self.publish_version_input)
        publish_version_input.click()
        publish_version_input.send_keys(VersionNumber)

        # 输入包配置信息
        merger_package_input = self.driver.find_element(By.XPATH, self.merger_package_input)
        merger_package_input.click()
        sleep(1)
        merger_package_input.send_keys(Keys.UP, Keys.ENTER)

        merger_path_input = self.driver.find_element(By.XPATH, self.merger_path_input)
        merger_path_input.click()
        merger_path_input.send_keys(Path)

        merger_launch_parms_input = self.driver.find_element(By.XPATH, self.merger_launch_parms_input)
        merger_launch_parms_input.click()
        merger_launch_parms_input.send_keys(LaunchParms)

        merger_pool_name_input = self.driver.find_element(By.XPATH, self.merger_pool_name_input)
        merger_pool_name_input.click()
        sleep(1)
        merger_pool_name_input.send_keys(PoolName, Keys.UP, Keys.ENTER)

        save_publish_version_button = self.driver.find_element(By.XPATH, self.save_publish_version_button)
        save_publish_version_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.create_version_success_msg)))
        create_version_success_msg = self.driver.find_element(By.XPATH, self.create_version_success_msg).text.strip()
        assert create_version_success_msg != ''

    # 创建新版本 - 复制已有应用的配置
    def create_new_version_copy_config(self, PublishDescription, VersionNumber):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.create_publish_version_button)))
        create_publish_version_button = self.driver.find_element(By.XPATH, self.create_publish_version_button)
        create_publish_version_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.publish_description_input)))
        publish_description_input = self.driver.find_element(By.XPATH, self.publish_description_input)
        publish_description_input.send_keys(PublishDescription)

        copy_app_input = self.driver.find_element(By.XPATH, self.copy_app_input)
        copy_app_input.click()
        sleep(1)
        copy_appli = self.driver.find_element(By.XPATH, self.copy_appli)
        copy_appli.click()
        publish_version_input = self.driver.find_element(By.XPATH, self.publish_version_input)
        publish_version_input.click()
        publish_version_input.send_keys(VersionNumber)
        sleep(1)

        save_publish_version_button = self.driver.find_element(By.XPATH, self.save_publish_version_button)
        save_publish_version_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.create_version_success_msg)))
        create_version_success_msg = self.driver.find_element(By.XPATH, self.create_version_success_msg).text.strip()
        assert create_version_success_msg != ''

    # 编辑版本信息
    def edit_version_info(self, UpdatePublishDescription):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.publish_operation_icon)))
        publish_operation_icon = self.driver.find_element(By.XPATH, self.publish_operation_icon)
        publish_operation_icon.click()

        operation_ul = self.driver.find_element(By.XPATH, self.operation_ul)
        sleep(2)
        edit_button = operation_ul.find_element(By.XPATH, self.edit_button)
        edit_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.publish_description_input)))
        publish_description_input = self.driver.find_element(By.XPATH, self.publish_description_input)
        publish_description_input.click()
        publish_description_input.clear()
        publish_description_input.send_keys(UpdatePublishDescription)

        save_edit_button = self.driver.find_element(By.XPATH, self.save_edit_button)
        save_edit_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.edit_version_success_msg)))
        edit_version_success_msg = self.driver.find_element(By.XPATH, self.edit_version_success_msg).text.strip()
        assert edit_version_success_msg != ''

    # 提交审核
    def submit_check(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.publish_operation_icon)))
        publish_operation_icon = self.driver.find_element(By.XPATH, self.publish_operation_icon)
        publish_operation_icon.click()

        operation_ul = self.driver.find_element(By.XPATH, self.operation_ul)
        sleep(2)
        submit_check_button = operation_ul.find_element(By.XPATH, self.submit_check_button)
        submit_check_button.click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.confirm_submit_button)))
        confirm_submit_button = self.driver.find_element(By.XPATH, self.confirm_submit_button)
        confirm_submit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.submit_check_success_msg)))
        submit_check_success_msg = self.driver.find_element(By.XPATH, self.submit_check_success_msg).text.strip()
        assert submit_check_success_msg != ''

    # 撤回提交审核
    def submit_back_check(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.publish_operation_icon)))
        publish_operation_icon = self.driver.find_element(By.XPATH, self.publish_operation_icon)
        publish_operation_icon.click()

        operation_ul = self.driver.find_element(By.XPATH, self.operation_ul)
        sleep(2)
        submit_back_button = operation_ul.find_element(By.XPATH, self.submit_back_button)
        submit_back_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.confirm_submit_back_button)))
        confirm_submit_back_button = self.driver.find_element(By.XPATH, self.confirm_submit_back_button)
        confirm_submit_back_button.click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.submit_back_success_msg)))
        submit_back_success_msg = self.driver.find_element(By.XPATH, self.submit_back_success_msg).text.strip()
        assert submit_back_success_msg != ''

    def app_publish(self, app_name):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.search_publish_app_input)))
        search_publish_app_input = self.driver.find_element(By.XPATH, self.search_publish_app_input)
        search_publish_app_input.click()
        search_publish_app_input.send_keys(app_name, Keys.TAB)
        app_detail = self.driver.find_element(By.XPATH, self.app_detail)
        app_detail.click()
        version_app = self.driver.find_element(By.XPATH, self.app_detail)
        version_app.click()
        game_name = self.driver.find_element(By.XPATH, self.game_name).text()
        return game_name


