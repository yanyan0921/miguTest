import logging
import time
import unittest
import sys
import json

import ddt

sys.path.append("../../ui-test")
sys.path.append("../..")
sys.path.append("../../")

from common import ui_common as C
from ui_test.page import LoginClass, AdminHomeMenu, HomeMenuClass

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


def readfile():
    with open('user.json', 'r', encoding='utf-8') as f:
        # user_data = []
        result = json.load(f)
        # for i in result:
        #     user_data.append((i.get('username'), i.get('password'), i.get('expect')))
        # print(user_data)
        return result


@ddt.ddt
class test_org_admin_login(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = C.base_url()
        self.testCaseInfo = TestCaseInfo()
        self.driver.maximize_window()

    # def read(self, username, password, expect):
    #     print(username, password, expect)
    #     return username, password, expect

    @ddt.file_data('./user.json')
    @ddt.unpack
    def test_org_administrator_login(self, username, password, expect):
        print(username, password, expect)
        try:
            self.testCaseInfo.start = C.current_time()
            # 打开网页
            logger.info("Open Base site" + self.base_url)
            self.driver.get(self.base_url)
            login_page = LoginClass.LoginClass(self.driver)
            login_page.init_page()
            # 点击刷新验证码
            login_page.update()

            login_page.set_userinfo(username, password)
            # login_page.set_password('Unity@123')
            # 获取验证码
            get_verify = login_page.image_str()
            time.sleep(3)
            # 写入验证码
            login_page.set_verify(get_verify)

            time.sleep(5)
            # 获取当前窗口url，判断是否成功登录
            c_url = self.driver.current_url
            Login = login_page.sign(c_url)

            # login_page.skip_click()

            # 断言返回结果确定登录状态
            self.assertEqual(expect, Login)

            home_menu = HomeMenuClass.HomeMenuClass(self.driver)
            home_menu.init_page()


        except Exception as err:
            self.testCaseInfo.error_info = str(err)
            logger.error(("aaron Got error: " + str(err)))
        finally:
            self.testCaseInfo.end = C.current_time()
            self.testCaseInfo.secondsDuration = C.time_diff(self.testCaseInfo.start, self.testCaseInfo.end)

    def tearDown(self):
        self.driver.quit()


class test_Platform_admin_login(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = C.base_url()
        self.testCaseInfo = TestCaseInfo()
        self.driver.maximize_window()

    def test_org_administrator_login(self):
        try:
            self.testCaseInfo.start = C.current_time()
            # 打开网页
            logger.info("Open Base site" + self.base_url)
            self.driver.get(self.base_url)

            login_page = LoginClass.LoginClass(self.driver)
            login_page.init_page()

            logger.info("Login web with aaronpeng")
            login_page.set_userinfo('ranmeng', 'Unity@123')
            # login_page.set_password('Unity@123@')

            time.sleep(10)
            # login_page.sign()

            home_menu = AdminHomeMenu.AdminHomeMenu(self.driver)
            home_menu.init_page()


        except Exception as err:
            self.testCaseInfo.error_info = str(err)
            logger.error(("aaron Got error: " + str(err)))
        finally:
            self.testCaseInfo.end = C.current_time()
            self.testCaseInfo.secondsDuration = C.time_diff(self.testCaseInfo.start, self.testCaseInfo.end)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    # 测试集
    suite = unittest.TestSuite()
    suite.addTest(test_org_admin_login("test_org_administrator_login"))
    suite.addTest(test_Platform_admin_login("test_org_administrator_login"))
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run()
