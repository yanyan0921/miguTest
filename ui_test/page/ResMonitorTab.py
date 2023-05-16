from ui_test.page.BasePage import BasePage
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ResMonitorTab(BasePage):
    # 定位元素
    res_monitor_tab = '//*[@id="app"]/section/section/aside/ul/li[4]'
    dashboard_tab = '//*[@id="tab-mon0"]'
    card_header1 = '//*[@id="pane-mon0"]/div/div[1]/div[1]/div[1]/div/span'
    caed_header2 = '//*[@id="pane-mon0"]/div/div[1]/div[2]/div[1]/div'
    card_header3 = '//*[@id="pane-mon0"]/div/div[2]/div[1]/div[1]/div/span'
    card_header4 = '//*[@id="pane-mon0"]/div/div[2]/div[2]/div[1]/div/span'
    tatal_res = ''
    res_remain_number = '//*[@id="pane-mon0"]/div/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]'
    data_report = '//*[@id="tab-mon3"]'