from tracker.Mask.config import Config
from PIL import Image,ImageDraw,ImageChops
import math, operator
import random


class Mask:
    def __init__(self,id=None,x=0,y=0,width=0,height=0,label=None,src_image="",lat=None,lon=None,timestamp=None):
        self.id = id

        self.width=width
        self.height=height
        self.x=x
        self.y=y

        self.src_image=src_image
        self.src_image_width=None
        self.src_image_height=None
        self.croped_img=None

        self.x1=None
        self.x2=None
        self.y1=None
        self.y2=None

        self.h=None
        self.s=None
        self.d=None

        self.activation=0

        self.label=label

        self.Config=Config

        self.locate_x=None
        self.locate_y=None
        
        self.mask=None
        self.angle=None
        r = lambda: random.randint(0,255)
        self.color = (r(),r(),r(),255)

        self.distance = None

        self.timestamp = timestamp
        if( lat == None or lon == None ):                                                                                                                          
            print(self.src_image,"해당 파일의 위치정보가 입력되지 않았습니다.")
        else:
            self.lat=lat
            self.lon=lon

        if(src_image):
            self.load_image()
    def to_dict(self):
        return {"label":self.label,"x":self.locate_x,"y":self.locate_y,"lat":self.lat,"lon":self.lon}
    # 두이미지의 삼각측량법으로 거리를 구할때는 각도와 속도가 필요함
    def get_distance_by_lat_long(self,t):

        # approximate radius of earth in km
        R = 6373.0

        lat1=math.radians(self.lat)
        lon1=math.radians(self.lon)
        lat2=math.radians(t.lat)
        lon2=math.radians(t.lon)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        # a = math.sin( dlat / 2 )**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        # c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
        a = math.sin( dlat / 2 )**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))


        distance = R * c

        return distance

    def rotation_matrix(self,x,y,angle):
        # https://en.wikipedia.org/wiki/Rotation_matrix
        # return x,y
        x_ = math.cos(angle) * x + -1 * math.sin(angle) * y
        y_ = math.sin(angle) * x + math.cos(angle) * y
        return x_,y_ 

    def get_distance_from_camera_with(self,t):
        
        # https://en.wikipedia.org/wiki/Triangulation_(surveying)
        # Distance to a point by measuring two fixed angles

        l = self.get_distance_by_lat_long(t)
        

        
        d = l * ( math.sin(self.angle) * math.sin(t.angle) ) / math.sin(self.angle + t.angle)
        # print(d," = ", l ,self.angle,t.angle,self.angle ,t.angle) 
        self.distance = d
        # 상대좌표 계산 공식
        # 이 자리가 아님.
        # TODO
        self.locate_x = d * math.sin( self.angle )
        self.locate_y = d * math.cos( self.angle )


    def get_angle(self):
        center_x = self.src_image_width / 2
        target_x = self.x
        
        # left
        if( center_x > target_x ):
            a = center_x - target_x
            b = self.width / 2 
            an = self.Config.ANGLE
            T = self.src_image_width / 2
            
            self.angle = math.radians(( an * ( a + b ) ) / T)

        # right
        elif( center_x < target_x ):
            a = center_x - (self.src_image_width - target_x)
            b = self.width / 2
            an = self.Config.ANGLE
            T = self.src_image_width / 2

            self.angle = math.radians(( an * ( a + b ) ) / T)

        # same
        else:
            self.angle= math.radians(0)

    def disactivation(self):
        self.activation=-1

    def increase_activation(self):
        self.activation+=1

    def isclose(self,a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
    
    def get_distance_with(self,t_mask):
        """
            Euclidean distance
            https://en.wikipedia.org/wiki/Euclidean_distance
        """
        return (math.sqrt((self.x - t_mask.x)**2+(self.y - t_mask.y)**2))

    def get_difference_size_with(self,mask):
        """
            Calculate a size difference between two rectangles
        """
        return (abs(self.width*self.height-mask.width*mask.height))
    
    def load_image(self):
        try:
            img=Image.open(self.src_image)
            img=self.image_flip_90_degree(img)

            self.src_image_width,self.src_image_height = img.size
            self.get_angle()
        except FileNotFoundError as e:
            print("FileNotFoundError : {0}".format(e))
            return None
        else:
            self.croped_img=img.crop((self.x,self.y,self.x+self.width,self.y+self.height))
    def get_histogram_with(self,t_mask):
        """
            Calculate the root-mean-square difference between two image's histogram
        """

        h = ImageChops.difference(self.croped_img,t_mask.croped_img).histogram()

        return math.sqrt(sum(h*(i**2)for i,h in enumerate(h))/(float(self.croped_img.size[0])*t_mask.croped_img.size[1]))

    def is_label_equal_with(self,t_mask):
        if(t_mask.label == self.label):
            return True
        else:
            return False


    def get_similarity_with(self,t_mask):
        sim_point=0

        dis=t_mask.get_distance_with(t_mask)
        # if(dis < self.Config.DISTANCE):
        #     sim_point+=dis
        # else:
        #     return 0xffffff
        size=t_mask.get_difference_size_with(t_mask)
        if( size < self.Config.SIZE):
            sim_point+=size
        else:
            return 0xffffff
        hist=t_mask.get_histogram_with(t_mask)
        if( hist < self.Config.HISTOGRAM):
            sim_point+=hist
        else:
            return 0xffffff
 
        return sim_point
    def there_not_equal(self,t_mask):
        dis=(math.sqrt((self.x - t_mask.x)**2+(self.y - t_mask.y)**2))

        if(self.is_label_equal_with(t_mask)):
            if(dis<self.Config.DISTANCE):
                return False
        return True
        
    def image_flip_90_degree(self,image):
        return image.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_90)

    def __repr__(self):
        return "x:{0} y:{1} h:{2} w:{3} label:{4} activation:{5}".format(self.x,self.y,self.height,self.width,self.label,self.activation)