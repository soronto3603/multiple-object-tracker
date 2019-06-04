# Multiple-object-tracker == MOT
import os
import time
import click
# from Mask_RCNN.samples import get_masking_inform
from Mask_RCNN.samples import cut_video
from Mask_RCNN.samples import FrameIterator as fi
from blackclue import blackclue
from nmea2gpx import nmea2gpx
from Mask_RCNN.samples import get_masking_inform as MaskRCNN
from tracker import tracker
from tracker.Mask import mask
import math

import gpxpy
import gpxpy.gpx
import time
import datetime
import json


import time
from time import strftime
# @click.command()
# @click.option('--videopath', help='Number of greetings.')
# @click.option('--imgjson', help='The person to greet.')
# @click.option('--geojson', help='The person to greet.')
# @click.option('--datapath', help='The person to greet.')

def guessTimestamp( timeArray ,framePerSecond , frameNumber ):
        if( frameNumber % framePerSecond == 0):
                return timeArray[ int(frameNumber/framePerSecond) ]
        else:
                # print( framePerSecond )
                timeRate = int(1000 / framePerSecond)
                # print( timeRate )
                return timeArray[ math.floor(frameNumber/framePerSecond) ] + timeRate * (frameNumber % framePerSecond) 

def guessCameraLoc( framePerSecond, frameNumber, coordArray, timeArray ):
	# out :  ( x , y , t, direction )
        # 인덱스와 맞는 위치에는 해당 값을 반환..
        if( frameNumber % framePerSecond == 0 ):
                x = coordArray[ int(frameNumber/framePerSecond) ]["lat"]
                # y
                y = coordArray[ int(frameNumber/framePerSecond) ]["lon"]
                # t
                print(timeArray[0], framePerSecond, frameNumber )
                t = guessTimestamp( timeArray, framePerSecond,frameNumber)
                # d
                d = None
                if( int(frameNumber/framePerSecond) is not 0 ):
                        p1x = coordArray[ int(frameNumber/framePerSecond) -1 ]["lat"]
                        p1y = coordArray[ int(frameNumber/framePerSecond) -1 ]["lon"]

                        p2x = coordArray[ int(frameNumber/framePerSecond) ]["lat"]
                        p2y = coordArray[ int(frameNumber/framePerSecond) ]["lon"]

                        d = math.degrees( math.atan2( p2x - p1x, p2y - p1y ))
                        if( d < 0 ): d = 360 + d
                return ( x, y ,t, d)
                # 인덱스와 맞지 않는 위치에는 이전과 다음 위치에의해 프레임 비율로 생성하여 넣음..
                # todo..
        else:
                # x
                x = coordArray[ int(frameNumber/framePerSecond) ]["lat"]
                # y
                y = coordArray[ int(frameNumber/framePerSecond) ]["lon"]
                # t
                t = guessTimestamp( timeArray, framePerSecond,frameNumber)
                # d
                d = None
                if( int(frameNumber/framePerSecond) is not 0 ):
                        p1x = coordArray[ int(frameNumber/framePerSecond) -1 ]["lat"]
                        p1y = coordArray[ int(frameNumber/framePerSecond) -1 ]["lon"]

                        p2x = coordArray[ int(frameNumber/framePerSecond) ]["lat"]
                        p2y = coordArray[ int(frameNumber/framePerSecond) ]["lon"]

                        d = math.degrees( math.atan2( p2x - p1x, p2y - p1y ))
                        if( d < 0 ): d = 360 + d
                return ( x, y ,t, d)

def detectObjectLocations( videoUri, aiModel='mscoco', saveFilepath = '/tmp' , gpxUri=None, coordArray=None, timeArray=None):
        # mp4 파일 만 줬을때
        if(not gpxUri):
                # in : videoUri(mp4), gpxUri(GPX XML)
                # out : [ geojson ] => geoJson = (objid, objType, [ x y timeStamp ])

                C_TIMESTAMP = str( int( time.time() ) )
                RESULT_DIR = "./" + saveFilepath + "/"

                blackclue.dump( file = [videoUri], dest_path = RESULT_DIR )
                nmea2gpx.convert(RESULT_DIR+"output.nmea",RESULT_DIR+"output.gpx")

                detectObjectLocations( videoUri, aiModel, saveFilepath, gpxUri = RESULT_DIR + "output.gpx" )

        # mp4 + gpx 줬을때
        elif(not coordArray and not timeArray):
                # in : videoUri(mp4), gpxUri(GPX XML)
                # out : [ geojson ] => geoJson = (objid, objType, [ x y timeStamp ])
                gpx = None
                try:
                        with open( gpxUri ) as f:
                            gpx = gpxpy.parse(f)
                except FileNotFoundError as e:
                        print("FileNotFoundError : {0}".format(e))
                        raise Exception("JSON is None")
                
                for track in gpx.tracks:
                        for segment in track.segments:
                                gpx = segment.points
                
                coordArray = []
                timeArray = []
                
                for i in gpx:
                        # print(i,type(i.time),i.longitude)
                        timestamp = time.mktime(i.time.timetuple())
                        
                        coordArray.append({"lat":i.latitude,"lon":i.longitude})
                        timeArray.append(timestamp)
                detectObjectLocations( videoUri, aiModel, saveFilepath, gpxUri = gpxUri, coordArray = coordArray, timeArray = timeArray )
        # 뭐가있든 신경안씁 coordarray , timearray
        else:
                # in : videoUri(mp4 with GPS/acc )
                # out : [ geojson ] => geoJson = (objid, objType, [ x y timeStamp ]) 
                
                start_time = time.time()
                
                print("start_time", start_time) #출력해보면, 시간형식이 사람이 읽기 힘든 일련번호형식입니다.
                print("#1 Complete")
                print("--- %s seconds ---" %(time.time() - start_time))
                
                detectObjectLocArray = getFrameIterator( videoUri, coordArray, timeArray )
                print("#2 Complete")
                print("--- %s seconds ---" %(time.time() - start_time))
                print(detectObjectLocArray)
                detectObjectLocArray = trackDetectObjectLocArray( detectObjectLocArray )
                print("#3 Complete")
                trackDetectObjectLocArray( detectObjectLocArray )
                transformDetectedArrayToGeoJson(detectObjectLocArray)

def setUpCameraPosition( cameraInstallHeight = 120, cameraHAngle = 90, cameraVAngle = 80 ):
        # out : FOV_INIT = ( cameraInstallHeight, cameraHAngle, cameraVAngle, cameraHDirectionAdust=0, camearaVDirectionAdust=0 )
        return { "cameraInstallHeight":120,"cameraHAngle":90,"cameraVAngle":80,"cameraHDirectionAdust":0,"cameraVdirectionAdust":0 }
	
	
def getFrameIterator( videoUri, coordArray, timeArray, detectionFrameSet=1, rotation=0, saveFilePath = '/tmp' ):
	# out :  frameIterator
	# example :
	#		detectObjectLocArray = null
	#            if frameIterator.hasMore() 
	#				( aFrame, frameNumber ) = frameIterator.next();
	#				detectedObjArray = detectObjects( aFrame, aiModelObject ) # out :[ ( objType, x1, y1, x2, y2 ) ]
	#				frameTime = guessTime( framePerSecond, frameNumber ) # out: timestamp
	#				cameraLoc = guessCameraLoc( frameTime, coordArray, timeArray )
	# 				locArray = guessDetectedObjLoc( cameraLoc, FOV_INIT, detectedObjArray ) # out: [ ( x, y ) ]
	#				detectObjectLocArray.push(detectedObjArray, locArray, frameTime )
	#     return detectedObjectLocArray
        framePerSecond = fi.getFramePerSecond( videoUri )
        detectObjectLocArray = []
        for aframe, frameNumber in fi.frameGenerator( videoUri, saveFilePath, detectionFrameSet , rotation ):
                detectedObjectArray = MaskRCNN.detectObject(aframe,"MSCOCO")
                frameTime = guessTimestamp( timeArray ,framePerSecond , frameNumber )
                cameraLoc = guessCameraLoc(framePerSecond, frameNumber, coordArray,timeArray)
                FOV_INIT = setUpCameraPosition()
                # locArray = guessDetectedObjLoc( cameraLoc, FOV_INIT, detectedObjectArray )
                detectObjectLocArray.append([detectedObjectArray,FOV_INIT,frameTime,cameraLoc,aframe])

                if(frameNumber == 5):
                        break

        return detectObjectLocArray

def trackDetectObjectLocArray( detectedObjectLocArray ):
        tr = tracker.Tracker( detectedObjectLocArray = detectedObjectLocArray )
        return tr.traking()

	
def transformDetectedArrayToGeoJson( detectedObjectLocArray,saveFilePath = '/tmp' ):
        # out : GeoJSON
        json.dump(detectedObjectLocArray , saveFilePath + "/output.json")
	
	
	

	
def run(videopath,imgjson,geojson,datapath):
        # python mot.py --videopath C:/Users/MCA/Documents/28.blackvue_mp4/28.blackvue_mp4/20190510_133411_NF.mp4
        if(datapath == None):
                if(videopath == None):
                        print("it's need videopath. please input videopath. -h")
                        return
                print(videopath,imgjson,geojson)

                DEFAULT_RESULT_DIR = "./result/"
                C_TIMESTAMP = str( int( time.time() ) )
                RESULT_DIR = DEFAULT_RESULT_DIR + C_TIMESTAMP + "/"
                FILENAME = videopath.split("/")
                FILENAME = FILENAME[len(FILENAME)-1].split(".")[0]

                if( not os.path.exists( RESULT_DIR ) ):
                        os.makedirs( RESULT_DIR )
                
                m = cut_video.Movie()
                m.cut( videopath , RESULT_DIR , rotation=0 )
                blackclue.dump( file = [videopath], dest_path = RESULT_DIR )
                
                nmea2gpx.convert(RESULT_DIR+"output.nmea",RESULT_DIR+"output.gpx")
                MaskRCNN.run(RESULT_DIR,FILENAME)

                DEFAULT_PATH = "./result/"+C_TIMESTAMP
                JSON_NAME = "infos.json"
                GEO_JSON_NAME = "output.gpx"
                tr = tracker.Tracker(default_path=DEFAULT_PATH,json_name=JSON_NAME,geo_json=GEO_JSON_NAME)
                tr.run()

        # python mot.py --datapath 1558521388
        else:
                DEFAULT_PATH="./result/"+datapath
                JSON_NAME="infos.json"
                GEO_JSON_NAME="output.gpx"
                tr = tracker.Tracker(default_path=DEFAULT_PATH,json_name=JSON_NAME,geo_json=GEO_JSON_NAME)
                tr.run()



if __name__ == '__main__':
        detectObjectLocations( "C:/Users/MCA/Documents/28.blackvue_mp4/28.blackvue_mp4/20190510_133411_NF.mp4" )
