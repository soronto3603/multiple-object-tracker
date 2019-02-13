import math
from PIL import Image,ImageDraw

class Mask:
    def __init__(self,x=0,y=0,width=0,height=0):
        self.width=width
        self.height=height
        self.x=x
        self.y=y

        self.x1=None
        self.x2=None
        self.y1=None
        self.y2=None

        self.h=None
        self.s=None
        self.d=None

        self.activation=0
    
    def disactivation(self):
        self.activation=-1

    def increase_activation(self):
        self.activation+=1

    def isclose(self,a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
    
    def get_distance_to(self,mask):
        return (math.sqrt((self.x-mask.x)**2+(self.y-mask.y)**2))

    def get_difference_size_to(self,mask):
        return (abs(self.width*self.height-mask.width*mask.height))
    
    def load_image(self,path):
        try:
            img=Image.open(path)
        except FileNotFoundError as e:
            print("FileNotFoundError : {0}".format(e))
            return None
        else:
            return img
