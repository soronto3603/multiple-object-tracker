"""
path,dir_name 출력될 dir 설정
capturing할 video path 설정
"""

import numpy as np
import cv2
import os

path="./"
dir_name="frame"
video_path='../dataset/vdd/video/b2e54795-d8c2ba7d.mov'
directory_path=path+dir_name

try:
    os.stat(directory_path)
except:
    os.mkdir(directory_path)

cap = cv2.VideoCapture('../dataset/vdd/video/b726c429-11f5acde.mov')
# cap = cv2.VideoCapture(video_path)

frame_no=0
drop_frame_no=60

while(cap.isOpened()):
    frame_no+=1
    ret, frame = cap.read()

    if( frame_no % drop_frame_no != 0 ):
        continue
    
    # cv2.imshow('frame',frame)
    cv2.imwrite('./vdd/vdd'+str(frame_no)+'.jpg',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()