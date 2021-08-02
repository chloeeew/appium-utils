"""
==================
Author:Chloeee
Time:2021/4/4 19:18
Contact:403505960@qq.com
==================
"""

import pytest
import time
from appium.webdriver import Remote
from pages.user import UserPage
from pages.nav import NavPage

@pytest.fixture()
def open_app():
    desired_cap = {
        "automationName": "UiAutomator2",
        "platformName": "Android",
        "platformVersion": "5.1.1",
        "deviceName": "Huawei P40 Pro",
        "appPackage": "com.have.been.erased",
        "appActivity": "com.have.been.erased.activity.WelcomeActivity",
        "noReset": False
    }

    driver = Remote(command_executor="http://127.0.0.1:4723/wd/hub",
                    desired_capabilities=desired_cap)
    driver.implicitly_wait(10)
    yield driver
    time.sleep(5)
    driver.quit()


@pytest.fixture()
def login_app(open_app):
    login_driver = open_app
    nav = NavPage(login_driver)
    nav.click_user()
    bp = UserPage(login_driver)
    bp.login_lemon("135318","89")
    yield login_driver


@pytest.fixture()
def into_topic():
    pass



def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode-escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')