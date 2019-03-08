class Config:
    DISTANCE=200
    HISTOGRAM=700
    SIZE=300

    def __init__(self):
        pass
        
    def set_config(self,opt):
        self.DISTANCE=opt[0]
        self.HISTOGRAM=opt[1]
        self.SIZE=opt[2]