# video_infos.py
import json


class InfosTest:
    def __init__(self,file):
        with open(file) as data_file:
            self.data = json.load(data_file)

        
    def __repr__(self):
        print(self.data.keys())
        print(len(self.data['locations']))


# test
if __name__ == "__main__":
    vi=InfosTest("./infos.json")
    print(len(vi.data)) 
    # 58


