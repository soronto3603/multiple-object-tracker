# video_infos.py
import json
import gpxpy
import gpxpy.gpx


class VideoInfos:
    def __init__(self,file):
        with open(file) as data_file:

            gpx = gpxpy.parse(data_file)

   
            for track in gpx.tracks:
                for segment in track.segments:           
                    self.len = len(segment.points)
                    break
                    # for point in segment.points:
                    #     print(point.latitude,point.longitude,point.time)
            
            # self.data = json.load(data_file)
            # self.len = len(self.data['locations'])

            self.data = ""
            print(self.len)
        
    def __repr__(self):
        pass
        # print(self.data.keys())
        # print(len(self.data['locations']))

    # 입력 이미지를 json의 타임스탬프 기준으로 평준하게/골고루 맞춰줌 
    def select_genel(self,input_images):
        len_input_images = len(input_images)

        new_list = []
    
        if( len_input_images > self.len ):
            rate = len_input_images / self.len

            idx = 0
            while(True):
                if(round(idx) >= len(input_images) ):
                    break

                new_list.append( input_images[round(idx)] )
                idx+=rate
                    

            
            return new_list
        else:
            # 이미지 개수가 모자람
            pass

# test
if __name__ == "__main__":
    vi=VideoInfos("C:/Users/MCA/Documents/1/multiple-object-tracker/result/1558363191/output.gpx")

    a=vi.select_genel([x for x in range(200,300)])
    print(len(a),vi.len)
