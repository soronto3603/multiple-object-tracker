# https://github.com/kunalprompt/tdd-python-unittest-example/blob/master/tests/test_app.py

from PIL import Image, ImageDraw
import os
import json

def tofilepath(frame_no) -> str:
    return "./nascar_Extract/frame_{0}".format(frame_no)

default_path="./nascar_Extract"
files=os.listdir(default_path)

info=[]
for filepath in files:
    if filepath.endswith('.json'):
        with open(default_path+"/"+filepath,"r+") as f:
            info=json.load(f)

# for frame in info:
#     print(frame["frame"])