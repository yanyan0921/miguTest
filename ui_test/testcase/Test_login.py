import logging
import time
import unittest
import sys
import json

from ddt import ddt, data, unpack

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


@ddt
class test_org_admin_login(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = C.base_url()
        self.testCaseInfo = TestCaseInfo()
        self.driver.maximize_window()
        self.current_window_handle

    def test_org_administrator_login(self):
        try:
            self.testCaseInfo.start = C.current_time()
            # 打开网页
            logger.info("Open Base site" + self.base_url)
            self.driver.get(self.base_url)
            login_page = LoginClass.LoginClass(self.driver)
            login_page.init_page()
            # 点击刷新验证码
            login_page.update()

            # 读取json数据
            def readfile():
                with open('user.json', 'r', encoding='utf-8') as f:
                    result = json.load(f)
                    return result

            @data(*readfile())
            @unpack
            def read(user, pwd):
                return user, pwd

            login_page.set_userinfo(read)
            # login_page.set_password('Unity@123')
            # 获取验证码
            get_verify = login_page.image_str()
            # 写入验证码
            login_page.set_verify(get_verify)

            time.sleep(10)
            # 获取当前窗口句柄，判断是否成功登录
            current_handle = self.current_window_handle
            Login = login_page.sign(current_handle)

            # login_page.skip_click()

            # 断言返回结果确定登录状态
            self.assertEqual('True', Login)

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
            login_page.set_username('ranmeng')
            login_page.set_password('Unity@123@')

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
