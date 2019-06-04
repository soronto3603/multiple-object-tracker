from scipy import ndimage
import cv2

def frameGenerator( fileUrl, resultUri, frameSet=None, rotation=0 ):
    cap = cv2.VideoCapture(fileUrl)
    frameRate = int( cap.get(5) )

    print("Frame Rate : " + str( frameRate ))      
    print("Frame Set : " + str( frameSet ))

    fileName = fileUrl.split("/")[-1].split(".")[0]
    filePath = fileUrl.split( fileName )[0]

    if( cap.isOpened() == False ):
        print("Error opening video stream or file.")
    if( frameRate == 0 ):
        frameRate = 1

    if( frameSet is None ):
        frameSet = frameRate

    frameNum = 0
    

    frameSec = ( 1000 * frameSet / frameRate )
    sec = 0
    index = 0
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret is True:
            # print( frameNum , frameSet)
            if frameNum % frameSet == 0:
                frame = ndimage.rotate( frame , rotation )

                yield (frame,frameNum)
                
                sec_ = int( (sec + frameSec) / 1000 )
                # cv2.imwrite( resultUri + fileName + str(index) + ".jpg", frame )
                index += 1
                sec += frameSec
        else:
            break
        
        frameNum += 1

    cap.release()
    cv2.destroyAllWindows()
    print("File read complete.")

def getFramePerSecond(fileUrl):
    cap = cv2.VideoCapture(fileUrl)
    frameRate = int( cap.get(5) )
    return frameRate