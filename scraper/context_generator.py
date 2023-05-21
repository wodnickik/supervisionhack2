import hashlib
import json
import re
from urllib.parse import urlparse
from datetime import datetime
import time
from os import path
from pathlib import Path

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


def generate_context(keywords, driver=None, cookies_out=None):
    if driver is None:
        flag = True

        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")
        options.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.notifications": 1}
        )
        driver = webdriver.Chrome(options=options)

    # TODO zaakceptować używanie plików cookie w google
    for keyword in keywords:
        driver.get('https://www.google.com/search?q=' + keyword.replace(' ', '+'))
        time.sleep(2)

    if cookies_out is not None:
        with open(cookies_out, "w") as file:
            json.dump(driver.get_cookies(), file)

    if flag:
        driver.quit()
