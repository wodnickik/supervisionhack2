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


# ta funkcja ma tylko bardzo podstawową funkcjonalność
# żeby pokazać poc naszego pomysłu na generowanie kontekstu
def generate_context(
keywords: list(str),
driver: webdriver = None,
cookies_out: str = None):
    """
    Generuje kontekst którego można użyć do scrapowania reklam,
    najlepiej podać przyjanmniej jedno z dwóch driver/cookies_out bo inaczej kontekst się gdzieś zgubi
    :param keywords: lista fraz kluczowych do generowania kontekstu
    :param driver: opcjonalny parametr w którym można przekazać driver żeby nabijać kontekst bezpośrednio w sesji
    :param cookies_out: opcjonalny parametr z lokalizcją do zapisu ciasteczek
    :return: brak
    """

    # jeśli nie otrzymujemy na wejściu drivera
    # to tworzymy nowy i pamiętamy, że trzeba go na koniec zamknąć
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

    # dla każdego słowa kluczowego wyszukujemy je w googlu
    for keyword in keywords:
        driver.get('https://www.google.com/search?q=' + keyword.replace(' ', '+'))
        # dalej moglibyśmy na przykąłd klikać losowe linki z wyniku
        # akceptować cookies na stronach na które trafimy
        # i w ten sposób tworzyć kontekst
        time.sleep(2)

    # zapisujemy plik z kontekstem
    if cookies_out is not None:
        with open(cookies_out, "w") as file:
            json.dump(driver.get_cookies(), file)

    # jeśli jest taka potrzeba zamykamy driver
    if flag:
        driver.quit()
