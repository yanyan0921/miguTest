import logging
import time
import unittest
import sys

import pytest

sys.path.append("../../ui-test")
sys.path.append("../..")
sys.path.append("../../")
from common import ui_common as C, utility as u
from ui_test.page import LoginClass, AdminHomeMenu, AccountPageClass, AccountAddPage, OrgPageClass, OrgInfoPage
from common import utility
from ui_test.lib.accountSystem import accountSys
from selenium import webdriver

logger = logging.getLogger("main")
logger.setLevel(level=logging.INFO)


class TestCaseInfo(object):
    def __init__(self, test_id="", name="", owner="", result="Failed", start="", end="", error_info=""):
        self.id = test_id
        self.name = name
        self.owner = owner
        self.result = result
        self.start = start
        self.end = end
        self.info = error_info


class TestPlatformFunction(unittest.TestCase):
    # def setUp(self):
    #     self.driver = webdriver.Chrome()
    #     self.base_url = C.base_url()
    #     self.testCaseInfo = TestCaseInfo()
    #     self.driver.maximize_window()

    @pytest.fixture()
    def PlatformFunctionModel(self):
        print('****** inPlatformFunction setup *********')
        self.testCaseInfo = TestCaseInfo()

    @pytest.fixture()
    def PlatformFunction(self):
        print('****** inPlatformFunction setup *********')
        self.driver = webdriver.Chrome()
        self.base_url = C.base_url()
        self.driver.maximize_window()

    def test_delete_account(self):
        # 测试创建账号--删除账号
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
        login_page.set_userinfo('admin_mengran', 'Unity@123')
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
        # accountSys.loginPlatform()
        msg = add_page.create_account(create_name, 'mengran.piao+66@unity.cn')
        assert msg != ''
        # 搜索/编辑/删除新增用户
        account_page.init_page()
        account_page.search_account(create_name)
        save_msg = account_page.edit_account_info(update_name)
        assert save_msg != ''
        account_page.delete_searched_account(update_name)

    def test_edit_account(self):
        create_name = 'auto' + utility.random_str(5)
        self.testCaseInfo.start = C.current_time()
        # 打开网页
        logger.info("Open Base site" + self.base_url)
        self.driver.get(self.base_url)

        login_page = LoginClass.LoginClass(self.driver)
        login_page.init_page()

        logger.info("Login web with admin_mengran")
        login_page.set_userinfo('admin_mengran', 'Unity@123')
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
        msg = add_page.create_account(create_name, 'mengran.piao+66@unity.cn')
        assert msg != ''
        # 验证添加组织关联
        account_page.init_page()
        account_page.search_account(create_name)
        modify_msg = account_page.org_connect(7)
        self.assertIn('开发者同时关联最多3个组织', modify_msg)

        modify_true_msg = account_page.org_connect(3)
        self.assertIn('更新操作成功', modify_true_msg)

    # except Exception as err:
    #     self.testCaseInfo.error_info = str(err)
    #     logger.error(("AutoTestOrg Got error: " + str(err)))
    # finally:
    #     self.testCaseInfo.end = C.current_time()
    #     self.testCaseInfo.secondsDuration = C.time_diff(self.testCaseInfo.start, self.testCaseInfo.end)

    # class test_org_e2e(unittest.TestCase):
    #     def setUp(self):
    #         option = webdriver.ChromeOptions()
    #         option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    #         self.driver = webdriver.Chrome(options=option)
    #         self.driver.maximize_window()
    #         self.base_url = C.base_url()
    #         self.testCaseInfo = TestCaseInfo()

    def test_create_delete_org(self):
        # 组织管理
        admin_list = 0
        test_org_name = 'AutoOrgName'
        link_admin_name = 'ke'
        link_member_name = 'meng'
        # try:
        self.testCaseInfo.start = C.current_time()
        # 打开网页
        logger.info("Open Base site" + self.base_url)
        self.driver.get(self.base_url)

        login_page = LoginClass.LoginClass(self.driver)
        login_page.init_page()

        logger.info("Login web with admin_mengran")
        login_page.set_userinfo('admin_mengran', 'Unity@123')
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
        admin_list = org_info_page.new_org_admin(link_admin_name)()

        org_page.search_org(test_org_name)
        # 验证添加是否成功
        list_li, msg = org_info_page.verify_add()
        self.assertIn(link_admin_name, msg)
        self.assertEqual(admin_list, list_li)

        org_info_page.click_memeber_link()
        org_info_page.add_member_link(link_member_name)

        searched_name = org_info_page.search_member('meng')
        self.assertIn('meng', searched_name)

        # 添加成员后返回组织管理面板
        org_info_page.back_to_org_page()
        org_page.init_page()
        org_page.search_org(test_org_name)

        # 删除组织
        delete_msg = org_page.delete_org(test_org_name)
        assert delete_msg != ''
        org_page.search_org(test_org_name)
        search_nodata = org_page.verify_deleted_org()
        self.assertIn('暂无数据', search_nodata)

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

    # class test_org_edit_name(unittest.TestCase):
    # def setUp(self):
    #     self.driver = webdriver.Chrome()
    #     self.driver.maximize_window()
    #     self.base_url = C.base_url()
    #     self.testCaseInfo = TestCaseInfo()

    def test_org_edit_name(self):
        # 组织更改基础信息，更改资源分配
        search_org_str = 'AutoTestOrg'
        # try:
        self.testCaseInfo.start = C.current_time()
        # 打开网页
        logger.info("Open Base site" + self.base_url)
        self.driver.get(self.base_url)

        login_page = LoginClass.LoginClass(self.driver)
        login_page.init_page()

        logger.info("Login web with admin_mengran")
        login_page.set_userinfo('admin_mengran', 'Unity@123')
        # login_page.set_username('admin_mengran')
        # login_page.set_password('Unity@123')
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
        org_info_page.back_to_org_page()

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
    # 资源管理模块

    def tearDown(self):
        self.driver.quit()
