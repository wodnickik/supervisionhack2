from model.model import predict
from model.utils import get_img_text
from thefuzz import fuzz
import json
import os
from typing import List, Optional

def get_ads_predictions(keywords: Optional[List[str]] = None) -> List:

    BUFFOR_DIR = 'out/'
    files_imgs = os.listdir(BUFFOR_DIR)
    meta_path = files_imgs.pop(files_imgs.index('metadata.json'))
    meta_data = json.load(open(BUFFOR_DIR + meta_path, 'r'))

    ads_list = []
    for ad in meta_data:
        id = ad['id']
        img_name = ad.get('img_name', None)
        if img_name is not None:
            words = get_img_text(BUFFOR_DIR + img_name)
            if keywords:
                is_ok = True
                for keyword in keywords:
                    if fuzz.partial_ratio(words, keyword) < 50:
                        is_ok = False
                        break
                if is_ok == False:
                    continue
        link = ad.get('link', None)
        post_text = ad.get('post_text', None)
        prediction, confidence = predict(BUFFOR_DIR + img_name, link, post_text)
        ads = {
            'name': id,
            'prediction': prediction,
            'confidence': confidence,
            'destination url': link,
            'words': words,
            'img_path': BUFFOR_DIR + img_name
        }
        ads_list.append(ads)
    
    return ads_list
