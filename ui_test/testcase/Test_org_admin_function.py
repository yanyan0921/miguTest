import unittest
import sys

sys.path.append("../../ui-test")
sys.path.append("../..")
sys.path.append("../../")
from ui_test.page import AccountManagePage, Login, PoolManagePage, ProjectManagePage, PackageManageTab, AppManageTab, \
    AppPublishTab
from selenium import webdriver
from common import utility
import time


class TestOrgAdmin(unittest.TestCase):
    # global username, password
    # username, password = 'mengran_1', 'Unity@123'

    def setUp(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        self.driver = webdriver.Chrome(options=option)
        self.driver.get('https://cloud-platform.migu.cn/#/')
        self.driver.maximize_window()

    # # 登录
    # def test_login(self):
    #     login_page = Login.Login(self.driver)
    #     login_page.set_username(username)
    #     login_page.set_password(password)
    #     time.sleep(2)
    #     login_page.sign()

    # 登录 - > 账号管理tab
    def test_account_manage(self):
        login_page = Login.Login(self.driver)
        login_page.set_username(username)
        login_page.set_password(password)
        time.sleep(10)
        account_page = AccountManagePage.AccountManagePage(self.driver)
        account_page.init_page()
        account_page.link_dev_account('mengran_2')
        time.sleep(3)
        account_page.search_linked_dev_accout('mengran_2')
        time.sleep(3)
        account_page.cancel_link_dev_accout()
        time.sleep(3)
        account_page.search_canceled_dev_accout('mengran_2')

    #  登录 - > 资源池列表管理
    def test_create_del_pool(self):
        pool_name = "AutoTest-" + utility.random_str(5)
        update_pool_name = "Update-" + utility.random_str(4)
        # 登录
        login_page = Login.Login(self.driver)
        login_page.set_username(username)
        login_page.set_password(password)
        time.sleep(10)
        # 资源池管理页面
        pool_page = PoolManagePage.PoolManagePage(self.driver)
        pool_page.init_page()
        pool_page.create_pool()
        time.sleep(1)
        pool_page.input_pool_info(pool_name, '弹性', 'PUB_3060_弹性', 1, 'test pool; automation testing')
        time.sleep(1)
        # 搜索创建的资源池
        pool_page.search_pool(pool_name)
        # 编辑资源池信息
        pool_page.edit_pool_info(update_pool_name)
        # 搜索update的资源池
        pool_page.search_pool(update_pool_name)
        # 删除创建的资源池
        pool_page.del_searched_pool()
        # 搜索删除的资源池是否存在
        time.sleep(2)
        pool_page.search_deleted_pool(update_pool_name)

    # # 登录---》项目管理
    def test_created_del_project(self):
        # 项目信息
        project_name = 'test_project' + utility.random_str(5)
        project_description = 'test_project_description' + utility.random_str(5)
        update_project_name = 'test_project' + utility.random_str(1)
        login_page = Login.Login(self.driver)
        login_page.set_username(username)
        login_page.set_password(password)
        time.sleep(10)
        # 项目管理页面
        project_page = ProjectManagePage.ProjectManagePage(self.driver)
        project_page.init_project_manage_page()
        project_page.create_project(project_name, project_description)
        project_page.search_project(project_name)
        project_page.enter_project_details_page()
        project_page.edit_project_info(update_project_name)
        time.sleep(2)
        project_page.search_project(update_project_name)
        time.sleep(5)
        project_page.del_project()
        project_page.search_deleted_project(update_project_name)

    # # 登录---》游戏包上传 在org_03组织的test项目下进行
    def test_package_manage(self):
        package_path = 'D:\DownloadApp\Browser Download\Chrome\p001.zip'
        package_name = 'p001.zip'
        increment_package_path = 'D:\DownloadApp\Browser Download\Chrome\p002.zip'
        rename_package = 'rename_' + utility.random_str(5)
        # 登录
        login_page = Login.Login(self.driver)
        login_page.set_username(username)
        login_page.set_password(password)
        time.sleep(10)
        # 项目管理 - test项目详情页面
        project_page = ProjectManagePage.ProjectManagePage(self.driver)
        project_page.init_project_manage_page()
        project_page.search_project('test')
        project_page.enter_project_details_page()
        # 游戏包管理页面
        package_manage_tab = PackageManageTab.PackageManageTab(self.driver)
        package_manage_tab.init_package_manage_tab()
        package_manage_tab.upload_package(package_path)
        time.sleep(2)
        package_manage_tab.search_package(package_name)
        package_manage_tab.upload_incremental_package(increment_package_path, package_name, rename_package)
        time.sleep(3)
        package_manage_tab.search_package(rename_package)
        time.sleep(2)
        package_manage_tab.del_package()
        time.sleep(2)
        package_manage_tab.search_deleted_package(rename_package)

    # 登录---》App管理 在org_03组织的test项目下进行
    def test_project_manage(self):
        app_name = 'automation_' + utility.random_str(5)
        package_name = 'p001.zip'
        launch_file_path = utility.random_str(4)
        launch_params = '-test ' + utility.random_str(1)
        pool_name = 'New_image_GPU_3060'
        update_app_name = 'update_' + utility.random_str(4)
        # 登录
        login_page = Login.Login(self.driver)
        login_page.set_username(username)
        login_page.set_password(password)
        time.sleep(10)
        # 项目管理 - test项目详情页面
        project_page = ProjectManagePage.ProjectManagePage(self.driver)
        project_page.init_project_manage_page()
        project_page.search_project('test')
        project_page.enter_project_details_page()
        # App管理tab
        app_manage_tab = AppManageTab.AppManageTab(self.driver)
        app_manage_tab.init_app_manage_tab()
        app_manage_tab.create_app(app_name, package_name, launch_file_path, launch_params, pool_name)
        app_manage_tab.search_app(app_name)
        app_manage_tab.edit_app_info(update_app_name)
        app_manage_tab.search_app(update_app_name)
        app_manage_tab.del_app()
        app_manage_tab.search_deleted_app(update_app_name)

    # 登录-》App发布
    def test_create_publish_app(self):
        app_name = "AutoAppName_" + utility.random_str(5)
        game_name = 'Game' + utility.random_str(5)
        description = "AutoDescription:" + utility.random_str(10)
        file_path = 'D:\Pictures\picture.png'
        publish_description = 'AutoPublishDescription:' + utility.random_str(6)
        update_publish_description = 'Update - AutoPublishDescription:' + utility.random_str(10)
        version1 = '1.1.1'
        version2 = '1.1.2'
        package_path = 'auto/path/' + utility.random_str(3)
        package_params = '-test ' + utility.random_str(2)
        pool_name = 'test_gpu'

        #     # 登录
        login_page = Login.Login(self.driver)
        login_page.set_username(username)
        login_page.set_password(password)
        time.sleep(10)
        # 进入test项目
        project_page = ProjectManagePage.ProjectManagePage(self.driver)
        project_page.init_project_manage_page()
        project_page.search_project('test')
        project_page.enter_project_details_page()
        # App发布Tab
        publish_app_tab = AppPublishTab.AppPublishTab(self.driver)
        publish_app_tab.init_page()
        publish_app_tab.create_publish_app(app_name, game_name, description, file_path)
        publish_app_tab.search_publish_app(app_name)
        publish_app_tab.create_new_version_customed_config(publish_description, version1, package_path, package_params,
                                                           pool_name)
        publish_app_tab.create_new_version_copy_config(publish_description, version2)
        publish_app_tab.edit_version_info(update_publish_description)
        publish_app_tab.submit_check()
        publish_app_tab.submit_back_check()
        publish_app_tab.submit_check()

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    # 测试集
    suite = unittest.TestSuite()
    suite.addTest(TestOrgAdmin("test_login"))
    suite.addTest(TestOrgAdmin("test_account_manage"))
    suite.addTest(TestOrgAdmin("test_create_del_pool"))
    suite.addTest(TestOrgAdmin("test_created_del_project"))
    suite.addTest(TestOrgAdmin("test_package_manage"))
    suite.addTest(TestOrgAdmin("test_project_manage"))
    suite.addTest(TestOrgAdmin("test_create_publish_app"))
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
