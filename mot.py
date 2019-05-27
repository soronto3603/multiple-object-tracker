# Multiple-object-tracker == MOT
import os
import time
import click
# from Mask_RCNN.samples import get_masking_inform
from Mask_RCNN.samples import cut_video
from blackclue import blackclue
from nmea2gpx import nmea2gpx
from Mask_RCNN.samples import get_masking_inform
from tracker import tracker
from tracker.Mask import mask

@click.command()
@click.option('--videopath', help='Number of greetings.')
@click.option('--imgjson', help='The person to greet.')
@click.option('--geojson', help='The person to greet.')
@click.option('--datapath', help='The person to greet.')



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
                get_masking_inform.run(RESULT_DIR,FILENAME)

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

def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)

if __name__ == '__main__':
    run()