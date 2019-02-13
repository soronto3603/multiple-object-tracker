import math
class Mask:
    def __init__(self,x=0,y=0):
        self.width=None
        self.height=None
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