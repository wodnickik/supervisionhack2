from pathlib import Path
import os
import sys

API_DIR = Path(__file__).resolve().parent
PROJ_DIR = Path(__file__).resolve().parent.parent.parent
TEST_DIR = Path(__file__).resolve().parent.parent
sys.path.append(os.path.join(API_DIR, ""))
sys.path.append(os.path.join(PROJ_DIR, ""))
sys.path.append(os.path.join(TEST_DIR, ""))

from waitress import serve

from ads_detect.wsgi import application

if __name__ == '__main__':
    serve(application, port=8000)