import logging
import time
import unittest
import sys
sys.path.append("../../ui-test")
sys.path.append("../..")
sys.path.append("../../")
from common import ui_common as C, utility as u
from ui_test.page import LoginClass, AdminHomeMenu, AccountPageClass, AccountAddPage, OrgPageClass, OrgInfoPage
from common import utility

from selenium import webdriver


logger = logging.getLogger("main")
logger.setLevel(level=logging.INFO)

class TestCaseInfo(object):
    def __init__(self, test_id = "", name = "", owner = "", result = "Failed", start = "", end = "", error_info = ""):
        self.id = test_id
        self.name = name
        self.owner = owner
        self.result = result
        self.start = start
        self.end = end
        self.info = error_info


class test_delete_account(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.base_url = C.base_url()
        self.testCaseInfo = TestCaseInfo()

    def test_delete_account(self):
            create_name = 'auto' + utility.random_str(5)
            update_name = 'UpdateName' + utility.random_str(5) 
        # try:
            self.testCaseInfo.start = C.current_time()
            # 打开网页
            logger.info("Open Base site" + self.base_url)
            self.driver.get(self.base_url)

            login_page = LoginClass.LoginClass(self.driver)
            login_page.init_page()

            logger.info("Login web with admin_mengran")
            login_page.set_username('admin_mengran')
            login_page.set_password('Unity@123')
            time.sleep(10)
            # login_page.sign()


            home_menu = AdminHomeMenu.AdminHomeMenu(self.driver)
            home_menu.init_page()

            home_menu.choose_account__manage()

            account_page = AccountPageClass.AccountPageClass(self.driver)
            account_page.init_page()
            account_page.new_account()

            add_page = AccountAddPage.AccountAddPageClass(self.driver)
            add_page.init_page()
            add_page.create_account(create_name, 'mengran.piao+66@unity.cn')

            account_page.init_page()
            account_page.search_account(create_name)
            # account_page.edit_account_info(update_name)
            account_page.delete_searched_account(update_name)


        # except Exception as err:
        #     self.testCaseInfo.error_info = str(err)
        #     logger.error(("AutoTestOrg Got error: " + str(err)))
        # finally:
        #     self.testCaseInfo.end = C.current_time()
        #     self.testCaseInfo.secondsDuration = C.time_diff(self.testCaseInfo.start, self.testCaseInfo.end)


    def tearDown(self):
        self.driver.quit()



class test_org_e2e(unittest.TestCase):
    def setUp(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        self.driver = webdriver.Chrome(options=option)
        self.driver.maximize_window()
        self.base_url = C.base_url()
        self.testCaseInfo = TestCaseInfo()

    def test_create_delete_org(self):
            test_org_name = 'AutoOrgName'
            link_addmin_name = 'mengran_1'
            link_member_name = 'mengran_3'
        # try:
            self.testCaseInfo.start = C.current_time()
            # 打开网页
            logger.info("Open Base site" + self.base_url)
            self.driver.get(self.base_url)

            login_page = LoginClass.LoginClass(self.driver)
            login_page.init_page()

            logger.info("Login web with admin_mengran")
            login_page.set_username('admin_mengran')
            login_page.set_password('Unity@123')
            time.sleep(10)


            home_menu = AdminHomeMenu.AdminHomeMenu(self.driver)
            home_menu.init_page()

            home_menu.choose_org_manage()

            org_page = OrgPageClass.OrgPageClass(self.driver)
            org_page.init_page()
            org_page.new_org(test_org_name)
            org_page.search_org(test_org_name)

            org_page.click_org_detail(test_org_name)
            org_info_page = OrgInfoPage.OrgInfoPage(self.driver)
            org_info_page.init_page()
            org_info_page.new_org_admin(link_addmin_name)

            org_info_page.click_memeber_link()
            org_info_page.add_memeber_link(link_member_name)

            searched_name = org_info_page.search_member('mengran_3')
            assert searched_name == 'mengran_3'

            # 添加成员后返回组织管理面板
            org_info_page.back_to_org_page()
            org_page.init_page()
            org_page.search_org(test_org_name)
            org_page.delete_org(test_org_name)
            org_page.search_org(test_org_name)
            org_page.verify_deleted_org()




            # add_page = AccountAddPage.AccountAddPageClass(self.driver)
            # add_page.init_page()
            # add_page.create_account('AutoTestOrgtest', 'AutoTestOrgpeng+12@unity3d.com')
            #
            # account_page.init_page()
            # account_page.search_account('AutoTestOrgtest')
            # account_page.delete_searched_account('AutoTestOrgtest')


        # except Exception as err:
        #     self.testCaseInfo.error_info = str(err)
        #     logger.error(("AutoTestOrg Got error: " + str(err)))
        # finally:
        #     self.testCaseInfo.end = C.current_time()
        #     self.testCaseInfo.secondsDuration = C.time_diff(self.testCaseInfo.start, self.testCaseInfo.end)


    def tearDown(self):
        self.driver.quit()


class test_org_edit_name(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.base_url = C.base_url()
        self.testCaseInfo = TestCaseInfo()

    def test_org_edit_name(self):
            search_org_str = 'AutoTestOrg'
        # try:
            self.testCaseInfo.start = C.current_time()
            # 打开网页
            logger.info("Open Base site" + self.base_url)
            self.driver.get(self.base_url)

            login_page = LoginClass.LoginClass(self.driver)
            login_page.init_page()

            logger.info("Login web with admin_mengran")
            login_page.set_username('admin_mengran')
            login_page.set_password('Unity@123')
            time.sleep(10)

            home_menu = AdminHomeMenu.AdminHomeMenu(self.driver)
            home_menu.init_page()
            home_menu.choose_org_manage()

            org_page = OrgPageClass.OrgPageClass(self.driver)
            org_page.init_page()
            org_page.search_org(search_org_str)
            org_page.click_org_detail(search_org_str)

            org_info_page = OrgInfoPage.OrgInfoPage(self.driver)
            org_info_page.init_page()
            random_org_name = 'AutoTestOrg' + u.random_number(5)
            org_info_page.edit_org_name(random_org_name)
            org_info_page.save_update()
            org_info_page.basic_back_to_org_page()

            # 修改后返回验修改信息
            org_page.init_page()
            org_page.search_org(random_org_name)
            org_page.verify_org_edit_success(random_org_name)


        # except Exception as err:
        #     self.testCaseInfo.error_info = str(err)
        #     logger.error(("AutoTestOrg Got error: " + str(err)))
        # finally:
        #     self.testCaseInfo.end = C.current_time()
        #     self.testCaseInfo.secondsDuration = C.time_diff(self.testCaseInfo.start, self.testCaseInfo.end)


    def tearDown(self):
        self.driver.quit()


















