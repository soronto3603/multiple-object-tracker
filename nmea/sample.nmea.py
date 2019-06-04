from blackclue import blackclue
from nmea2gpx import nmea2gpx

RESULT_DIR = "./sample_result/"
videopath = "C:/Users/MCA/Documents/28.blackvue_mp4/28.blackvue_mp4/20190510_133411_NF.mp4"

blackclue.dump( file = [videopath], dest_path = RESULT_DIR )

nmea2gpx.convert(RESULT_DIR+"output.nmea",RESULT_DIR+"output.gpx")