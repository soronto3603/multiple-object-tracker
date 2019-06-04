from blackclue import blackclue
from nmea2gpx import nmea2gpx

RESULT_DIR = "./sample_result/"
videopath = "./20190510_133411_NR.mp4"

blackclue.dump( file = [videopath], dest_path = RESULT_DIR )

nmea2gpx.convert(RESULT_DIR+"output.nmea",RESULT_DIR+"output.gpx")