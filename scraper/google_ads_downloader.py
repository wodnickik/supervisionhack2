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


def hash_encode(s: str):
    """
    Wygeneruj hash
    :param s: napis
    :return: hash
    """
    return hashlib.md5(s.encode()).hexdigest()


# tej funkcji zdarza się rzucić wyjątek
# prawdopodobnie lepsze waity rozwiążą problem
# odpalenie jej drugi raz prawie zawsze to naprawia
def download_ads(
    url: str,
    output_destination: str = 'out',
    cookies_location: str = 'cookies',
    verbose: bool = 0
):
    """
    Scrapeuje google adsy z zadanego urla
    :param url: url strony do scrapowania
    :param output_destination: folder w którym zostaną zapisane jsony i pngi
    :param cookies_location: folder z kontekstem
    :param verbose: czy printować
    :return: create json file with metadata, cookies context and ad images
    """

    # opcje potrzebne do prawidłowego funkcjonowania drivera
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")
    options.add_experimental_option(
        "prefs", {"profile.default_content_setting_values.notifications": 1}
    )

    # pusta lista na metadane reklam
    json_ads = []

    # tworzenie drivera
    with webdriver.Chrome(options=options) as driver:

        # wczytywanie cookies potrzebnych do obejścia
        # wyskakującego okienka "zaakceptuj pliki cookies"
        # trzeba mieć wcześniej plik cookies z tej witryny
        # na niektórych witrynach nie działa, wtedy trzeba specjalnie dalej kombinować (na przykład wp)
        # jeśli nie uda się obejść "zaakceptuj pliki cookies" to po prostu nie pobierze reklam ze strony
        # ale się nie wywali
        driver.get(url)
        if verbose: print(driver.current_url)
        domain = urlparse(driver.current_url).netloc
        cookies = json.loads(Path(path.join(cookies_location, f'{domain}_cookies.json')).read_text())

        # można ładować ciasteczka z kilku plików
        # w ten sposób można dodać ładowanie dodatkowego kontekstu
        for cookie in cookies:
            if 'sameSite' in cookie:
                cookie['sameSite'] = 'Strict'
            driver.add_cookie(cookie)
        # ładujemy stronę jeszcze raz po załądowaniu cookies
        # żeby pozbyć się popupu "zaakceptuj cookies"
        # to bardzo sprytne, prosimy docenić pomysłowość workarounda :)
        driver.get(url)

        # wyrażenie charakterystyczne dla google ads
        pattern = re.compile("^google_ads_iframe.*")

        # wybieranie elementów z reklamami
        elements = []
        for i in range(2):
            time.sleep(2)
            elements.extend(driver.find_elements(By.TAG_NAME, 'iframe'))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        elements = [_ for _ in elements if pattern.match(_.get_attribute('id'))]

        # filter dla regexa
        tmp = dict()
        for element in elements:
            tmp[element.get_attribute('id')] = element
        elements = tmp
        if verbose: print(len(elements))

        # po przefiltrowaniu iterujemy się po każdym elemencie
        for key in elements:
            element = elements[key]
            ActionChains(driver).move_to_element(element).perform()
            time.sleep(1)

            # robimy zdjęcie reklamy
            WebDriverWait(driver, 10, ignored_exceptions=StaleElementReferenceException).until(
                EC.presence_of_element_located((By.ID, key)))
            hash_value = hash_encode(f'{driver.current_url}_{datetime.now()}')
            element.screenshot(path.join(output_destination, f'{hash_value}.png'))

            # pobieramy docelowy url
            ActionChains(driver).click(element).perform()
            parent = driver.window_handles[0]
            child = driver.window_handles[-1]
            driver.switch_to.window(child)
            ad_url = driver.current_url
            driver.close()
            driver.switch_to.window(parent)

            # zbiermay metadane
            json_dict = {"id": hash_value,
                         "img_name": f'{hash_value}.png',
                         "link": ad_url}
            json_ads.append(json_dict)

        # zapisujemy cookies
        with open(path.join(output_destination, "cookies.json"), "w") as file:
            json.dump(driver.get_cookies(), file)

    # zapisujemy metadane
    with open(path.join(output_destination, "metadata.json"), "w") as file:
        json.dump(json_ads, file)
