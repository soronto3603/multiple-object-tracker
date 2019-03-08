from tracker.Mask.config import Config
from PIL import Image,ImageDraw,ImageChops
import math, operator

class Mask:
    def __init__(self,x=0,y=0,width=0,height=0,label=None,src_image=""):
        self.width=width
        self.height=height
        self.x=x
        self.y=y

        self.src_image=src_image
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


        if(src_image):
            self.load_image()
    
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
        
    def __repr__(self):
        return "x:{0} y:{1} h:{2} w:{3} label:{4} activation:{5}".format(self.x,self.y,self.height,self.width,self.label,self.activation)