from scipy import ndimage
import cv2

class Movie:
    def cut(self, file_url,resultPath, frame_set=None, rotation=0):
        print(file_url + " 파일의 영상을 자르기를 시작합니다.")
        if file_url is not None:
            cap = cv2.VideoCapture(file_url)
            print("1!::",cap.get(5))
            frame_rate = int(cap.get(5))
            if frame_set is None:
                frame_set = frame_rate
            print("Frame Rate : " + str(frame_rate))
            print("Frame Set : " + str(frame_set))
            file_name = file_url.split("/")[-1].split(".")[0]
            file_path = file_url.split(file_name)[0]
            print(file_name)
            if (cap.isOpened() == False):
                print("Error opening video stream or file")
            frame_num = 0
            print(frame_rate)
            if(frame_rate == 0):
                frame_rate = 1 
            frame_sec = (1000 * frame_set) / frame_rate
            sec = 0
            index = 0
            print(resultPath)
            while (cap.isOpened()):
                ret, frame = cap.read()
                if ret is True:
                    if frame_num % frame_set == 0:
                        frame = ndimage.rotate(frame, rotation)
                        sec_ = int((sec+frame_sec)/1000)
                        print("작업 : " + str(sec_) + "s")
                        cv2.imwrite(resultPath+file_name+str(index)+".jpg" ,frame)
                        index+=1
                        sec += frame_sec
                else:
                    break
                frame_num += 1
            cap.release()
            cv2.destroyAllWindows()
        else:
            print("Error opening video stream or file")
        print(file_url + "파일의 영상을 자르기를 종료합니다.")



# m=Movie()
# m.cut("../dataset/vdd/video/0a0c3694-f3444902.mov",frame_set=1,rotation=90)
