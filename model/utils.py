import easyocr
import numpy as np
from urllib.parse import urlparse
from typing import List
import re

def get_img_text(image_path: str) -> str:
    """
    Get text from image
    :param image_path: path to image
    :return: text from image
    """
    reader = easyocr.Reader(['pl', 'en'])
    result = reader.readtext(image_path)

    return ' '.join([text[1] for text in result])


def get_link_features(link: str) -> List:
    """
    Get features from link
    :param link: link to website
    :return: list of features
    """
    domain = urlparse(link).netloc
    is_https_in_domain = int('https' in domain)
    is_https = int(urlparse(link).scheme == "https")
    has_double_slash = int("//" in link[:7])
    has_at = int("@" in link)
    has_numbers_in_domain = int(any(char.isdigit() for char in domain))
    count_dots = link.count('.')
    count_slashes = link.count('/')
    count_dashes = link.count('-')
    has_ip = int(re.match(r'.*(?:\d{1,3}\.){3}\d{1,3}.*', domain) is not None)
    # length = len(link)
    # return np.array([is_https_in_domain, is_https, has_double_slash, has_at, has_numbers_in_domain,
    #                     count_dots, count_slashes, count_dashes, has_ip, length])
    return [is_https_in_domain, is_https, has_double_slash, has_at, has_numbers_in_domain,
                        count_dots, count_slashes, count_dashes, has_ip]
