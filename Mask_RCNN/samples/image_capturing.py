"""
path,dir_name 출력될 dir 설정
capturing할 video path 설정
"""



import numpy as np
import cv2
import os

def imageCapture(videoPath,resultPath="./result/"):
    path="./"
    dir_name="frame"
    video_path= videoPath
    directory_path=path+dir_name

    try:
        os.stat(directory_path)
    except:
        os.mkdir(directory_path)

    cap = cv2.VideoCapture(video_path)
    # cap = cv2.VideoCapture(video_path)

    frame_no=0
    drop_frame_no=60

    while(cap.isOpened()):
        frame_no+=1
        ret, frame = cap.read()

        if( frame_no % drop_frame_no != 0 ):
            continue
        
        # cv2.imshow('frame',frame)
        cv2.imwrite(resultPath+str(frame_no)+'.jpg',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

    cv2.destroyAllWindows()

if __name__=="__main__":
    imageCapture("C:/Users/MCA/Documents/28.blackvue_mp4/28.blackvue_mp4/20190510_133411_NF.mp4")
