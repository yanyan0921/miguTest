from ui_test.page.BasePage import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import re
import pytesseract
import pillow
from PIL import Image
import time

class LoginClass(BasePage):
    # 定位元素
    username = '//*[@id="app"]/div/div[2]/div/form/div[1]/div/div/input'
    password = '//*[@id="app"]/div/div[2]/div/form/div[2]/div/div[1]/input'
    sign_in = '//*[@id="app"]/div/div[2]/div/form/button'
    skip_button = '//*[@id="app"]/div/div[2]/div/form/div[3]/button'
    verify = '//*[@id="app"]/div/div[2]/div/form/div[3]/div/div/div[1]/div/input'
    update_verify = '//*[@id="app"]/div/div[2]/div/form/div[3]/div/div/div[1]/div/span/span/i/svg'



    def init_page(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.username)))





    # 设置用户名
    # def set_username(self, username):
    #     name = self.driver.find_element(By.XPATH, self.username)
    #     name.send_keys(username)
    #
    # # 输入密码
    # def set_password(self, pwd):
    #     password = self.driver.find_element(By.XPATH, self.password)
    #     password.send_keys(pwd)

    def set_userinfo(self, username, pwd):
          name = self.driver.find_element(By.XPATH, self.username)
          password = self.driver.find_element(By.XPATH, self.password)
          name.send_keys(username)
          password.send_keys(pwd)

    # 输入验证码
    def set_verify(self, verify):
        verify = self.driver.find_element(By.XPATH, self.verify)
        verify.seng_keys(verify)

        # 识别登录验证码图片 打开浏览器获取验证码图片

    def get_pictures(self):
        self.driver.save_screenshots('pictures.png')
        page_snap_obj = Image.open('pictures.png')
        img = self.find_element(By.TAG_NAME, self.picture)
        time.sleep(2)
        location = img.location
        size = img.size
        left = location['x']
        top = location["y"]
        right = left + size['width']
        bottom = top + size['height']
        image_obj = page_snap_obj.crop((left, top, right, bottom))
        image_obj.show()
        return image_obj

        # 灰度，二值化

    def processing_image(self):
        image_obj = self.get_pictures()
        img = image_obj.convert("L")
        pixdata = img.load()
        w, h = img.size
        #   设置阈值
        threshold = 150
        for y in range(h):
            for x in range(w):
                if pixdata[x, y] < threshold:
                    pixdata[x, y] = 0
                else:
                    pixdata[x, y] = 255
        return img

        # 降噪

    def delete_spot(self):
        images = self.processing_image()
        data = images.getdata()
        w, h = images.size
        black_point = 0
        for x in range(1, w - 1):
            for y in range(1, h - 1):
                mid_pixel = data[w * y + x]  # 中央像素点像素值
                if mid_pixel < 50:  # 找出上下左右四个方向像素点像素值
                    top_pixel = data[w * (y - 1) + x]
                    left_pixel = data[w * y + (x - 1)]
                    down_pixel = data[w * (y + 1) + x]
                    right_pixel = data[w * y + (x + 1)]
                    # 判断上下左右的黑色像素点总个数
                    if top_pixel < 10:
                        black_point += 1
                    if left_pixel < 10:
                        black_point += 1
                    if down_pixel < 10:
                        black_point += 1
                    if right_pixel < 10:
                        black_point += 1
                    if black_point < 1:
                        images.putpixel((x, y), 255)
                    black_point = 0
        # images.show()
        return images

        # 去除特殊字符

    def image_str(self):
        image = self.delete_spot()
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # 设置pyteseract路径
        result = pytesseract.image_to_string(image)  # 图片转文字
        result_j = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", result)  # 去除识别出来的特殊字符
        result_four = result_j[0:4]  # 只获取前4个字符
        # print(result_j)  # 打印识别的验证码
        return result_four

    # 更新验证码
    def update(self):
        update_ver = self.driver.find_element(By.XPATH,self.update_verify)
        update_ver.click()

    # 提交登录
    def sign(self, current_handle):
        submit = self.driver.find_element(By.XPATH, self.sign_in)
        submit.click()
        time.sleep(3)
        handles = self.driver.windows_handles
        # 遍历所有窗口，找到新开的窗口
        for handle in handles:
            if handle != current_handle:
                new_handle = handle
                break
    #     比较两个窗口句柄是否一致
        if new_handle != current_handle:
            return True
        else:
            return False




    def skip_click(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, self.skip_button)))
        skip_button = self.driver.find_element(By.XPATH, self.skip_button)
        skip_button.click()
