from ui_test.page.BasePage import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AccountAddPageClass(BasePage):
    # 定位元素
    create_button = '//*[@id="app"]/section/section/main/div[2]/div/h2/div[2]/button[2]'
    name__txt = '//*[@id="app"]/section/section/main/div[2]/div/div[1]/div/div[2]/form/div[1]/div/div/input'
    email__txt = '//*[@id="app"]/section/section/main/div[2]/div/div[1]/div/div[2]/form/div[2]/div/div/input'
    account_type__select = '//*[@id="app"]/section/section/main/div[2]/div/div[1]/div/div[2]/form/div[3]/div/div/div/div/input'
    option_platform = "//span[contains(text(),'平台')]"
    # create_success_msg = "//p[contains(text(),'恭喜您，添加成功~')]"

    def init_page(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.create_button)))

    def create_account(self, name, email):
        create_button = self.driver.find_element(By.XPATH, self.create_button)
        name__txt = self.driver.find_element(By.XPATH, self.name__txt)
        email__txt = self.driver.find_element(By.XPATH, self.email__txt)
        account_type__select = self.driver.find_element(By.XPATH, self.account_type__select)

        # create_button.click()
        name__txt.send_keys(name)
        email__txt.send_keys(email)
        account_type__select.click()

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, self.option_platform))).click()

        create_button.click()

        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.create_success_msg)))
        # create_success_msg = self.driver.find_element(By.XPATH, self.create_success_msg).text.strip()
        create_success_msg = self.driver.switch_to.alert.text
        # assert create_success_msg != ''
        return create_success_msg
