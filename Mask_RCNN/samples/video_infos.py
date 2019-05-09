# video_infos.py
import json


class VideoInfos:
    def __init__(self,file):
        with open(file) as data_file:
            self.data = json.load(data_file)
            self.len = len(self.data['locations'])
        
    def __repr__(self):
        print(self.data.keys())
        print(len(self.data['locations']))

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
    vi=VideoInfos("../dataset/vdd/info/b2e54795-d8c2ba6d.json")

    a=vi.select_genel([x for x in range(200,300)])
    print(len(a),vi.len)
