from tracker.Mask.mask import Mask
from PIL import Image,ImageDraw
import json
import datetime
import math

class Tracker:
    def __init__(self,default_path,json_name,geo_json):
        self.masks=[]
        self.default_path=default_path
        self.json_path=default_path+"/"+json_name

        self.load_json(self.json_path)
        self.load_geo_json(default_path+"/"+geo_json)

        self.save_file_index_no=0
        # activation max val
        self.ACTIVATION_MAX = 3

        self.saveJsonData = []
        self.idCounter = 1

        self.currentTimestamp = None
        self.currentDirection = None
    def get_absolute_angle(self,p1x,p1y,p2x,p2y):
        R = math.degrees( math.atan2(p2x - p1x, p2y - p1y) )
        if ( R < 0 ):
            return 360 + R
        return R 
    def run(self):
        for idx,file_info in enumerate(self.json):

            self.currentTimestamp = self.geo_json['locations'][idx]
            if( idx != 0 ):
                # lat=geo_json['latitude'],lon=geo_json['longitude']
                p1x = self.geo_json['locations'][idx-1]['latitude']
                p1y = self.geo_json['locations'][idx-1]['longitude']

                p2x = self.geo_json['locations'][idx]['latitude']
                p2y = self.geo_json['locations'][idx]['longitude']
                
                print("이전좌표")
                print("p1", p1x,p1y)
                print("p2",p2x,p2y)

                # self.currentDirection = self.get_absolute_angle(p1x,p1y,p2x,p2y)
                self.currentDirection = self.get_absolute_angle(p2x,p2y,p1x,p1y)
                print("이전 좌표와의 방향" , self.currentDirection)

            file_name=self.default_path+"/"+file_info['file_name']
            print("===========================>",file_name)
            self.make_mask_from_json(file_name,file_info,self.geo_json['locations'][idx])
            self.sort_masks()
            self.figure_distance()

            self.writeJson()

            # output image
            self.display_current_figure(file_name)
        
        # print for debuging
        for m in self.masks:
            print(m)
        print("TOTAL:",str(len(self.masks)))
        self.save_json()
    def writeJson(self):
        for _,mask in enumerate(self.masks):
            mask=self.pick_mask(mask)
            if( mask.timestamp == self.currentTimestamp ): 
                pass
    def figure_distance(self):
        for mask_list in self.masks:
            if ( len(mask_list) < 2 ):
                continue
            if ( mask_list[0].lat == None or mask_list[0].lon == None):
                continue
            mask_list[0].get_distance_from_camera_with(mask_list[1])
            if ( self.currentDirection != None ):
                print("current direction = ",self.currentDirection)
                print("entering")

                mask_list[0].get_absolute_position( self.currentDirection )
                print(mask_list[0].locate_x , mask_list[0].locate_y)
    def save_json(self):
        # DEL
        # jsonlist=[]
        # for m in self.masks:
        #     m=self.pick_mask(m)
        #     jsonlist.append(m.to_dict())
        #     # return {"label":self.label,"x":self.locate_x,"y":self.locate_y,"lat":self.lat,"lon":self.lon}


        with open('data.json', 'w') as outfile:
            json.dump(self.saveJsonData, outfile)
    
    def display_current_figure(self,image_path):
        main_image = Image.open(image_path).convert("RGB").transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_90)
        main_image_draw = ImageDraw.Draw(main_image)
        for mask_list in self.masks:

            main_color = mask_list[0].color
            
            
            # ##### 모든 인스턴스의 네모를 표시 & 라벨을 표시 & 거리를 표시
            # for mask in mask_list:
            #     print("Mask DRAW=============")
            #     main_image_draw.rectangle(((mask.x,mask.y),(mask.x+mask.width,mask.y+mask.height)),outline=main_color,width=5)
            #     main_image_draw.text((mask.x,mask.y),mask.label)
            #     try:
            #         main_image_draw.text((mask.x,mask.y+10),str(round(mask.distance,2)))
            #     except TypeError as e:
            #         print("FileNotFoundError : {0} \n 인스턴스의 가장 끝 이미지는 계산되지 않습니다.".format(e))
            #     print((mask.x,mask.y),(mask.x+mask.width,mask.y+mask.height))

            # ##### 각 첫번째의 인스턴스의 네모를 표시 & 라벨을 표시 & 거리를 표시
            # ##### 나머지 인스턴스를 선으로 표시

            for idx,mask in enumerate(mask_list):
                # 비활성화된 객체들은 표시하지 않음
                if( mask.activation == -1 ):
                    continue
                print("Mask DRAW=============")
                if( idx == 0 ):
                    try:
                        main_image_draw.text((mask.x,mask.y+10),str(round(mask.locate_x,5))+", "+str(round(mask.locate_y,5)))
                        main_image_draw.text((mask.x,mask.y+20),str(round(mask.distance*1000))+":::"+str(round(mask.distance,5)))
                        main_image_draw.text((mask.x,mask.y+30),"ACTIVATION:"+str(mask.activation))
                    except TypeError as e:
                        print("FileNotFoundError : {0} \n 인스턴스의 가장 끝 이미지는 계산되지 않습니다.".format(e))
                    
                if( idx == len(mask_list)-1 ):
                    main_image_draw.rectangle(((mask.x,mask.y),(mask.x+mask.width,mask.y+mask.height)),outline=main_color,width=2)
                    # main_image_draw.text((mask.x,mask.y),mask.label)
                    # print((mask.x,mask.y),(mask.x+mask.width,mask.y+mask.height))
                else:
                    main_image_draw.rectangle(((mask.x+mask.width/2-2,mask.y+mask.height/2-2),(mask.x+mask.width/2+2,mask.y+mask.height/2+2)),outline=main_color,width=2)
                    main_image_draw.line((mask.x+mask.width/2,mask.y+mask.height/2,mask_list[idx+1].x+mask_list[idx+1].width/2,mask_list[idx+1].y+mask_list[idx+1].height/2),fill=main_color,width=5)
        now=datetime.datetime.now()
        main_image.save("./results/test"+now.strftime("%Y%m%d%H%M%S")+"_"+str(self.save_file_index_no)+".jpg")
        self.save_file_index_no+=1

    def sort_masks(self):
        # 마스크들을 정리함
        idx=-1
        while( idx+1 < len(self.masks)):
            idx+=1
            mask = self.masks[idx]
            mask = self.pick_mask(mask)
            if mask.activation != 0:
                continue
            else:
                # 합칠 마스크를 찾음
                # 마스크들을 순회 하면서 가장 유사도가 낮은 대상을 찾음
                sim_mask=None
                sim_point=0xffffff
                sim_mask_idx=None
                
                for idx2,mask2 in enumerate(self.masks):
                    print(idx,":",mask,idx2,":",mask2)
                    mask2=self.pick_mask(mask2)
                    
                    if mask is mask2:
                        print("두 마스크가 같음")
                        continue

                    if mask.activation == mask2.activation:
                        print("두 마스크의 세대가 같음")
                        continue
                    if mask2.activation == -1:
                        print("마스크 하나가 비활성화 상태임")
                        continue
                    if mask.there_not_equal(mask2):
                        print("두마스크의 거리 혹은 라벨이 다름")
                        continue
                    
                    _sim_point=mask.get_similarity_with(mask2)
                    print(_sim_point,sim_point)
                    if(_sim_point < sim_point):
                        sim_point=_sim_point
                        sim_mask=mask2
                        sim_mask_idx=idx2

                # 찾았으면
                if sim_mask != None :
                    print("합쳐짐",idx,"<-",sim_mask_idx)
                    self.add_mask_at(sim_mask,idx)
                    del self.masks[sim_mask_idx]
                    idx-=1
                else:
                    print("합쳐질게 없음")

        for _,mask in enumerate(self.masks):
            mask=self.pick_mask(mask)
            if( mask.activation == -1 ):
                continue
            mask.increase_activation()  
            if( mask.activation >= self.ACTIVATION_MAX ):
                mask.disactivation()
        

    def make_mask_from_json(self,file_name,json,geo_json=None):
        # frame_no=masks_info['frame']
        # img_path="frame_{0}.jpg".format(frame_no)
        if(geo_json == None):
            print("위치정보가 없습니다. 거리를 계산할 수 없습니다.")
            for i in json['infos']:
                mask=Mask(id=self.idCounter,x=i['box'][0],y=i['box'][1],width=i['box'][2]-i['box'][0],height=i['box'][3]-i['box'][1],label=i['label'],src_image="{0}".format(file_name))
                self.create_mask(mask)
            
        # else:
        #     print(geo_json)
        #     raise Exception(123)
            # {'course': 313.4961853027344, 'timestamp': 1490565865000, 'latitude': 37.782350103962116, 'speed': 0.0, 'longitude': -122.40737524281286, 'accuracy': 10.0}
        else:
            for i in json['infos']:
                mask=Mask(id=self.idCounter,x=i['box'][0],y=i['box'][1],width=i['box'][2]-i['box'][0],height=i['box'][3]-i['box'][1],label=i['label'],src_image="{0}".format(file_name),lat=geo_json['latitude'],lon=geo_json['longitude'],timestamp=geo_json['timestamp'])
                self.create_mask(mask)

            
    def load_json(self,json_src):
        try:
            with open(json_src) as f:
                self.json=json.load(f)
        except FileNotFoundError as e:
            print("FileNotFoundError : {0}".format(e))
            raise Exception("JSON is None")

    def load_geo_json(self,geo_json):
        try:
            with open(geo_json) as f:
                self.geo_json=json.load(f)
        except FileNotFoundError as e:
            print("FileNotFoundError : {0}".format(e))
            raise Exception("JSON is None")

    def get_result(self):
        return []

    def create_mask(self,mask):
        mask_index=len(self.masks)
        self.masks.append([mask])
        return mask_index
    
    def add_mask_at(self,mask,index):
        self.masks[index].insert(0,mask)

    def pick_mask(self,mask):
        return mask[0]
    
    def __repr__(self):
        return str(self.masks)
    