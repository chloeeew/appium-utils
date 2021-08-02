"""
==================
Author:Chloeee
Time:2021/4/4 16:35
Contact:403505960@qq.com
==================
"""
import time
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.common.mobileby import MobileBy
from common.logger_handler import logger
from selenium.webdriver.common.by import By
from appium.common.exceptions import *
from common.keys import Keys


class BasePage:
    # 系统九宫格图案
    nine_grid_locator = ('id', 'com.android.keyguard:id/lockPatternView')

    def __init__(self,driver_arg):
        self.driver = driver_arg
        self.size = self.driver.get_window_size()
        self.height = self.size['height']
        self.width = self.size['width']


    def swipe_move(self, begin_x_rate=0.5, begin_y_rate=0.5, end_x_rate=0.5, end_y_rate=0.5):
        time.sleep(3)
        self.driver.swipe(start_x=self.width*begin_x_rate, start_y=self.height * begin_y_rate,
                          end_x=self.width * end_x_rate, end_y=self.height * end_y_rate)
        time.sleep(3)


    def swipe_to_left(self):
        self.swipe_move(begin_x_rate=0.9,end_x_rate=0.1)

    def swipe_to_right(self):
        self.swipe_move(begin_x_rate=0.1,end_x_rate=0.9)

    def swipe_to_bottom(self):
        self.swipe_move(begin_y_rate=0.1, end_y_rate=0.9)

    def swipe_to_top(self):
        self.swipe_move(begin_y_rate=0.9,end_y_rate=0.1)


    def get_nine_patter_grid(self,num:int):
        """获取九宫格1-9的位置"""
        if 1 > num or num > 9:
            raise ValueError
        nine_gird_ele = self.find_element_by_locator(self.nine_grid_locator)
        rect = nine_gird_ele.rect
        rect_x = rect['x']
        rect_y = rect['y']
        rect_height = rect['height']
        rect_width = rect['width']

        grid_1_po = {'x': rect_x + 1 / 6 * rect_width, 'y': rect_y + 1 / 6 * rect_height}
        grid_2_po = {'x': rect_x + 1 / 2 * rect_width, 'y': rect_y + 1 / 6 * rect_height}
        grid_3_po = {'x': rect_x + 5 / 6 * rect_width, 'y': rect_y + 1 / 6 * rect_height}
        grid_4_po = {'x': rect_x + 1 / 6 * rect_width, 'y': rect_y + 1 / 2 * rect_height}
        grid_5_po = {'x': rect_x + 1 / 2 * rect_width, 'y': rect_y + 1 / 2 * rect_height}
        grid_6_po = {'x': rect_x + 5 / 6 * rect_width, 'y': rect_y + 1 / 2 * rect_height}
        grid_7_po = {'x': rect_x + 1 / 6 * rect_width, 'y': rect_y + 5 / 6 * rect_height}
        grid_8_po = {'x': rect_x + 1 / 2 * rect_width, 'y': rect_y + 5 / 6 * rect_height}
        grid_9_po = {'x': rect_x + 5 / 6 * rect_width, 'y': rect_y + 5 / 6 * rect_height}

        grid_dict = {1:grid_1_po,2:grid_2_po,3:grid_3_po,4:grid_4_po,5:grid_5_po,6:grid_6_po,
                     7:grid_7_po,8:grid_8_po,9:grid_9_po}

        return grid_dict[num]

    def nine_pattern_gird_unlock(self):
        """Z字解锁"""
        time.sleep(2)
        self.driver.lock(3)
        time.sleep(2)
        self.driver.back()
        time.sleep(2)

        at = TouchAction(self.driver)
        at.press(**self.get_nine_patter_grid(1)).wait(2000). \
            move_to(**self.get_nine_patter_grid(2)).wait(200). \
            move_to(**self.get_nine_patter_grid(3)).wait(2000). \
            move_to(**self.get_nine_patter_grid(5)).wait(2000). \
            move_to(**self.get_nine_patter_grid(7)).wait(2000). \
            move_to(**self.get_nine_patter_grid(8)).wait(2000). \
            move_to(**self.get_nine_patter_grid(9)).wait(2000). \
            release().perform()

        time.sleep(2)


    def volume_up(self):
        """按下音量键+"""
        self.driver.press_keycode(Keys.VOLUME_UP)
        return self


    def volume_down(self):
        """按下音量键+"""
        self.driver.press_keycode(Keys.VOLUME_DOWN)
        return self

    def press_home(self):
        """按下首页键"""
        self.driver.press_keycode(Keys.HOME)


    def zoom_in(self,offset):
        """按照偏移量放大"""
        mid_width = self.width / 2
        mid_height = self.height / 2
        mid_height_offset_plus = mid_height + offset
        mid_height_offset_minus = mid_height + offset

        if mid_height_offset_minus<0 or mid_height_offset_plus>self.height:
            return

        a1 = TouchAction(self.driver)
        a1.press(x=mid_width , y=mid_height).move_to(x=mid_width, y=mid_height_offset_minus).perform()

        a2 = TouchAction(self.driver)
        a2.press(x=mid_width, y=mid_height).move_to(x=mid_width, y=mid_height_offset_plus).perform()

        mul = MultiAction(self.driver)
        mul.add(a1,a2).perform()
        return self


    def pinch_out(self, offset):
        """按照偏移量缩小"""
        mid_width = self.width / 2
        mid_height = self.height / 2
        mid_height_offset_plus = mid_height + offset
        mid_height_offset_minus = mid_height + offset

        if mid_height_offset_minus < 0 or mid_height_offset_plus > self.height:
            return

        a1 = TouchAction(self.driver)
        a1.press(x=mid_width, y=mid_height_offset_minus).move_to(x=mid_width, y=mid_height).perform()

        a2 = TouchAction(self.driver)
        a2.press(x=mid_width, y=mid_height_offset_plus).move_to(x=mid_width, y=mid_height).perform()

        mul = MultiAction(self.driver)
        mul.add(a1, a2).perform()
        return self


    def get_toast(self,text_info):
        return self.driver.find_element(By.XPATH,f"//*[@text={text_info}]")

    def find_element_by_locator(self,locator:tuple):
        try:
            el = self.driver.find_element(*locator)
        except NoSuchContextException as e:
            logger.error(f"找不到该元素{e}")
            raise e
        else:
            return el

    def click_element(self,target_locator:tuple):
        """点击元素"""
        el = self.find_element_by_locator(target_locator)
        el.click()
        time.sleep(1)
        return self


    def send_text(self, locator: tuple, content):
        """向元素输入文字"""
        el = self.find_element_by_locator(locator)
        el.send_keys(content)
        return self


    def get_element_text_by_locator(self,locator):
        """根据locator获取元素text值"""
        el = self.find_element_by_locator(locator)
        return el.text

