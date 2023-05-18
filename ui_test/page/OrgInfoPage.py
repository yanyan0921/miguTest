from ui_test.page.BasePage import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging

logger = logging.getLogger("main")
logger.setLevel(level=logging.INFO)


class OrgInfoPage(BasePage):
    # 定位元素
    save_modify_button = '//*[@id="app"]/section/section/main/div[2]/div/h2/div[2]/button[2]'
    new_org_admin_button = '//*[@id="pane-orgInfo"]/div[1]/div[1]/div/button'
    add_org_admin_name_txt = '//*[@id="pane-orgInfo"]/div[2]/div/div/div[2]/div/form/div/div/div[2]/div/div/input'
    # admin_name = "//span[contains(text(),'mengran_1')]"
    link_button = '//*[@id="pane-orgInfo"]/div[2]/div/div/div[3]/span/button[2]'
    link_admin_success_message = "//p[contains(text(),'添加组织管理员成功！')]"
    org_name_txt = '//*[@id="pane-orgInfo"]/div[1]/div[2]/form/div[1]/div/div/input'
    drop_down_box = '//*[@id="el-popper-container-4139"]/div[6]/div/div/div[1]/ul'
    drop_down_li = '//*[@id="el-popper-container-4139"]/div[6]/div/div/div[1]/ul/li[1]'
    member_manage_tab = '//*[@id="tab-orgMember"]'
    link_member_button = '//*[@id="pane-orgMember"]/div/div[1]/div/div/div[1]/button'
    choose_account_name_input = '//*[@id="pane-orgMember"]/div/div[2]/div/div/div[2]/div/form/div/div/div[2]/div/div/input'
    member_link = '//*[@id="pane-orgMember"]/div/div[2]/div/div/div[3]/span/button[2]'
    # member_name = "//span[contains(text(),'mengran_3')]"
    drop_down_box02 = '//*[@id="el-popper-container-4139"]/div[9]/div/div/div[1]/ul'
    drop_down_li02 = '//*[@id="el-popper-container-4139"]/div[9]/div/div/div[1]/ul/li[1]'
    link_member_success_message = "//p[contains(text(),'绑定账号成功！')]"
    edit_org_success_message = "//p[contains(text(),'修改组织信息成功！')]"

    search_member_txt = '//*[@id="pane-orgMember"]/div/div[1]/div/div/div[1]/div/input'
    searched_account_name = '//*[@id="pane-orgMember"]/div/div[1]/div/div/div[3]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[2]/div'

    go_back_button = '//*[@id="app"]/section/section/main/div[2]/div/h2/div[2]/button'



    def init_page(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.save_modify_button)))

    def new_org_admin(self, admin_account_name):
        new_org_admin_button = self.driver.find_element(By.XPATH, self.new_org_admin_button)
        new_org_admin_button.click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.add_org_admin_name_txt)))
        add_org_admin_name_txt = self.driver.find_element(By.XPATH, self.add_org_admin_name_txt)
        link_button = self.driver.find_element(By.XPATH, self.link_button)

        add_org_admin_name_txt.send_keys(admin_account_name)
        # 点击下拉框账号选择关联对象
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.drop_down_box)))
        admin_name = self.driver.find_element(By.XPATH, self.drop_down_li)
        admin_name.click()
        link_button.click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.link_admin_success_message)))
        link_admin_success_message = self.driver.find_element(By.XPATH, self.link_admin_success_message).text.strip()
        logger.info("the link org's admin success msg: " + link_admin_success_message)
        assert link_admin_success_message != ''

    def click_memeber_link(self):
        member_manage_tab = self.driver.find_element(By.XPATH, self.member_manage_tab)
        member_manage_tab.click()

    def add_member_link(self, member_name):
        # 成员管理tab--关联新账号
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.link_member_button)))
        link_member_button = self.driver.find_element(By.XPATH, self.link_member_button)
        link_member_button.click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.choose_account_name_input)))
        choose_account_name_input = self.driver.find_element(By.XPATH, self.choose_account_name_input)

        choose_account_name_input.send_keys(member_name)

        # 点击下拉框账号选择关联对象
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.drop_down_box02)))
        member_name = self.driver.find_element(By.XPATH, self.drop_down_li02)
        member_name.click()

        # 点击关联按钮
        member_link = self.driver.find_element(By.XPATH, self.member_link)
        member_link.click()

    def search_member(self, member_name):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.search_member_txt)))

        search_member_txt = self.driver.find_element(By.XPATH, self.search_member_txt)
        search_member_txt.send_keys(member_name, Keys.TAB)

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.searched_account_name)))
        searched_account_name = self.driver.find_element(By.XPATH, self.searched_account_name)
        return searched_account_name.text.strip()

    def edit_org_name(self, random_name):
        org_name_txt = self.driver.find_element(By.XPATH, self.org_name_txt)
        logger.info("the org name is: " + random_name)
        org_name_txt.clear()
        org_name_txt.send_keys(random_name)

    def save_update(self):
        save_modify_button = self.driver.find_element(By.XPATH, self.save_modify_button)
        save_modify_button.click()

    # def basic_back_to_org_page(self):
    #     go_back_basic = self.driver.find_element(By.XPATH,self.go_back_basic)
    #     go_back_basic.click()

    def back_to_org_page(self):
        go_back_button = self.driver.find_element(By.XPATH, self.go_back_button)
        go_back_button.click()
