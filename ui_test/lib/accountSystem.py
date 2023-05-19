import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from ui_test.page.BasePage import BasePage
from common import ui_common as C, utility as u
from ui_test.page import LoginClass, AdminHomeMenu, AccountPageClass, AccountAddPage, OrgPageClass, OrgInfoPage
from common import utility
import time

logger = logging.getLogger("main")
logger.setLevel(level=logging.INFO)


class AccountSystem:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.driver = webdriver.Chrome()
        self.base_url = C.base_url()
        self.driver.maximize_window()

    # def Info(self, test_id="", name="", owner="", result="Failed", start="", end="", error_info=""):
    #     self.id = test_id
    #     self.name = name
    #     self.owner = owner
    #     self.result = result
    #     self.start = start
    #     self.end = end
    #     self.info = error_info

    def loginPlatform(self):
        # 登录平台管理--创建账号
        create_name = 'auto' + utility.random_str(5)
        update_name = 'UpdateName' + utility.random_str(5)
        # try:
        # self.Info.start = C.current_time()
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


accountSys = AccountSystem()
