import pandas as pd
import numpy as np
import os
from utils import *

# folder jest pusty z powodu redundancji danych z folderem imgs4training
DATA_DIR = './data/imgs_cropped/'  

bad_imgs = [img for img in os.listdir(DATA_DIR + 'bad')]
good_imgs = [img for img in os.listdir(DATA_DIR + 'good')]

imgs = bad_imgs + good_imgs
labels = [1] * len(bad_imgs) + [0] * len(good_imgs)


df = pd.DataFrame({
    'label': labels,
    'name': imgs,
    'text': None,
})

for i, row in df.iterrows():
    print("Processing image", i+1, "of", len(df), flush=True)
    try:
        df.loc[i, 'text'] = get_img_text(DATA_DIR + row['name'])
    except:
        df.loc[i, 'text'] = None

df.to_csv('./data/imgs_with_text.csv', index=False)