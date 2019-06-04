from Mask_RCNN.samples import FrameIterator as fi
from Mask_RCNN.samples import get_masking_inform as MaskRCNN
import math

def guessTime( timeArray, framePerSecond, frameNumber ):
    if( frameNumber % framePerSecond == 0):
        return timeArray[ int(frameNumber/framePerSecond) ]
    else:
        # print( framePerSecond )
        timeRate = int(1000 / framePerSecond)
        # print( timeRate )
        return timeArray[ math.floor(frameNumber/framePerSecond) ] + timeRate * (frameNumber % framePerSecond) 

def guessCameraLoc( framePerSecond, frameNumber, coordArray, timeArray ):
	# out :  ( x , y , t, direction )
    if( frameNumber % framePerSecond == 0 ):
        x = coordArray[ int(frameNumber/framePerSecond) ]["lat"]
        # y
        y = coordArray[ int(frameNumber/framePerSecond) ]["lon"]
        # t
        t = guessTime( timeArray, framePerSecond,frameNumber)
        # d
        d = None
        return ( x, y ,t, d)
    else:
        # todo...
        # x
        x = coordArray[ int(frameNumber/framePerSecond) ]["lat"]
        # y
        y = coordArray[ int(frameNumber/framePerSecond) ]["lon"]
        # t
        t = guessTime( timeArray, framePerSecond,frameNumber)
        # d
        d = None
        return ( x, y ,t, d)
coordArray = [{"lat":23,"lon":34},{"lat":24,"lon":35},{"lat":25,"lon":36}
    ,{"lat":26,"lon":37},{"lat":27,"lon":38},{"lat":28,"lon":39}]
timeArray = [1000,2000,3000,4000,5000,6000]

framePerSecond = fi.getFramePerSecond( "C:/Users/MCA/Documents/28.blackvue_mp4/28.blackvue_mp4/20190510_133411_NF.mp4" )
# def frameGenerator( self, fileUrl, resultUri, frameSet=None, rotation=0 ):
for f,i in fi.frameGenerator( "C:/Users/MCA/Documents/28.blackvue_mp4/28.blackvue_mp4/20190510_133411_NF.mp4", "./result",frameSet=1 ):
    # detectedObjectArray = MaskRCNN.detectObject(f,"MSCOCO")
    
    frameTime = guessTime( timeArray ,framePerSecond , i )
    cameraLoc = guessCameraLoc(framePerSecond, i, coordArray, timeArray )
    print(cameraLoc)

