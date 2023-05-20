from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from datetime import datetime
import time
from os import path
import re


images_path = 'img'
url = 'https://www.onet.pl/'
headers = {
    'Refer': 'https://www.google.com/',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
}

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("start-maximized")
options.add_argument("--disable-extensions")
options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)
with webdriver.Chrome(options=options) as driver:
    driver.get(url)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'cmp-intro_acceptAll'))).click()

    pattern = re.compile("^google_ads_iframe.*")

    elements = []
    for i in range(2):
        time.sleep(2)
        elements.extend(driver.find_elements(By.TAG_NAME, 'iframe'))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print(len(elements))
    elements = [_ for _ in elements if pattern.match(_.get_attribute('id'))]
    tmp = dict()
    for element in elements:
        tmp[element.get_attribute('id')] = element
    elements = tmp
    print(len(elements))

    for key in elements:
        element = elements[key]
        print(key)
        ActionChains(driver).move_to_element(element).perform()
        # driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(1)

        WebDriverWait(driver, 10, ignored_exceptions=StaleElementReferenceException).until(EC.presence_of_element_located((By.ID, key)))
        element.screenshot(path.join(images_path, f'screenshot_{datetime.now()}.png'))

    time.sleep(5)
