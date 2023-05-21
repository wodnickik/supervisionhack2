import facebook_scraper as fs
import pandas as pd
import urllib
import requests
import facebook_scraper as fs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time
import os
import json
from webdriver_manager.chrome import ChromeDriverManager

def save_data(df, parent_dict):
    posts_json = []
    for i in range(df.shape[0]):
        post = df.iloc[i,:]
        post_id = post.loc["post_id"]
        img_name = post_id + ".jpg"
        link = post.loc["link"]
        parsed_uri = urllib.request.urlparse(link)
        link = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        post_text = post.loc["text"]
        url = post.loc["image"]

        if url == None:
            url = df.iloc[i,:].loc["image_lowquality"]
            if url != None:
                response = requests.get(url)
                with open(os.path.join(parent_dict,img_name), "wb") as f:
                    f.write(response.content)
            else:
                img_name = "null"
                
        json_dict = {"id": post_id,
                    "img_name": img_name,
                    "link": link,
                    "post_text": post_text}
        posts_json.append(json_dict)

    with open(os.path.join(parent_dict, "metadata.json"), "w") as file:
        json.dump(posts_json, file)


def check_facebook_url(url):
    parsed_uri = urllib.request.urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    after_domain = url.replace(domain, '').rsplit('/')
    if len(after_domain) == 1:
        return after_domain[0]
    elif after_domain[0] == "groups":
        if len(after_domain) == 2:
            return after_domain[1]
        elif after_domain[2] == "permalink":
            return after_domain[3]
        else:
            return None
    else:
        return None


def scrape_facebook(page_name, cookies, posts_limit=30):

    posts_df = pd.DataFrame(columns = [])
    url_start = "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=PL&view_all_page_id="
    url_end = "&search_type=page&media_type=all"
    browser = webdriver.Chrome(ChromeDriverManager().install())
    i = 0
    while True:
        # flag = False
        # try:
        #     print("1")
        #     gen = fs.get_posts(post_urls=[page_name], timeout=240, extra_info=False, cookies=cookies, options={"comments": False, "posts_per_page": 4})
        # except:
        #     print("2")
        #     flag = True
        link = check_facebook_url(page_name)
        # if flag and link != None:
        #     try:
        #         print("3")
        #         print(link)
        #         gen = fs.get_posts(link, timeout=240, extra_info=False, cookies='cookies.txt', options={"comments": False, "posts_per_page": 4})
        #     except:
        #         print("4")
        #         return None
        # else:
        #     return None
        for post in fs.get_posts(link, timeout=240, extra_info=False, cookies=cookies, options={"comments": False, "posts_per_page": 4}):
            if i == posts_limit:
                return posts_df
            else:
                i += 1
            page_id = post["page_id"]
            if type(page_id) != type("string"):
                continue
            url = url_start + page_id + url_end
            browser.get(url)
            try:
                element = browser.find_element(By.XPATH, '//button[text()="Allow all cookies"]')
                element.click()
            except:
                pass
            
            url2 = browser.current_url
            if re.search(page_id, url2) == None:
                continue
            else:
                time.sleep(2)
                html = browser.page_source
                try:
                    first_line = post["text"].split('\n')[0]
                except:
                    first_line = None
                try:
                    search_result = re.search(first_line, html)
                except:
                    continue
                    
                if (search_result == None) or (re.search("0 results", html) != None):
                    continue
                else:
                    if len(posts_df) != 0 and post["post_id"] in list(posts_df.iloc[:,0]):
                        continue
                    else:
                        fb_post_df = pd.DataFrame.from_dict(post, orient='index')
                        fb_post_df = fb_post_df.transpose()
                        posts_df = posts_df.append(fb_post_df)

    browser.close()
    return posts_df