# class tracker:
#     def __init__(self):
#         self.instances=[]
#         # RGB Color 분포 유사율
#         self.histogram_criteria=50
#         # 크기 유사율
#         self.size_criteria=50
#         # 거리 가까운 정도
#         self.distance_criteria=50
    
#     # 새로운 인스턴스
#     def append_new_instance(self,x):
#         self.instances.append(x)
    
#     # 기존의 인스턴스와 같은 것을 합치고 위치함.
#     def merge_instance(self,instance_idx,instance):
#         instance+=self.instances[instance_idx]
#         self.instances[instance_idx]=instance

#     def distance(self,instance_a,instance_b):
#         return 1
    
#     def histogram(self,instance_a,instance_b):
#         return 1

#     def size_sim(self,instance_a,instance_b):
#         return 1

#     def is_one(self,instance_a,instance_b) -> bool:
#         return (
#             # 각 인스턴스는 a ^ b = True를 만족해야하고
#             # 각 인스턴스는 activation > -1 을 만족해야함.
#             # is_available 은 위의 두사항을 만족하는지 검사함.
#             instance_a.is_available ^ instance_b.is_available and 
#             self.distance(instance_a,instance_b) > self.distance_criteria and
#             self.histogram(instance_a,instance_b) > self.histogram_criteria and
#             self.size_sim(instance_a,instance_b) > self.size_criteria
#         )

#     def merge(self,new_instances):
#         if len(self.instances) == 0:
#             for instance in new_instances:
#                 self.append_new_instance(instance)
#         elif len(self.instance) > 0:
#             for new_instance in new_instances:
#                 for idx,org_instance in enumerate(self.instances):
#                     # 첫번째 항목이 최근에 합쳐진 인스턴스
#                     org_instance=org_instance[0]
                    
#                     if is_one(new_instance,org_instance):
#                         self.merge_instance(idx,new_instance)
#                         # 이번 분기에서 새로운 인스턴스를 합쳤기 때문에 반복을 끝냄.
#                         break
#         for instance in self.instances:
#             instance=instance[0]
#             if instance.activation is not -1
#                 instance.activation+=1

# if __name__ == "__main__":
#     print("hello")

from tracker.Mask.mask import Mask
import json

class Tracker:
    def __init__(self,json_src=None):
        self.masks=[]
        self.json=None

        self.load_json(json_src)

    def sort_masks(self):
        # 마스크들을 정리함
        for idx,mask in enumerate(self.masks):
            mask=self.pick_mask(mask)
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

                    elif mask.activation == mask2.activation:
                        print("두 마스크의 세대가 같음")
                        continue
                    elif mask2.activation == -1:
                        print("마스크 하나가 비활성화 상태임")
                        continue
                    elif mask.there_not_equal(mask2):
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
                else:
                    print("합쳐질게 없음")

        for idx,mask in enumerate(self.masks):
            mask=self.pick_mask(mask)
            mask.increase_activation()  


    def make_mask_from_json(self,masks_info):
        frame_no=masks_info['frame']
        img_path="frame_{0}.jpg".format(frame_no)
        
        for i in masks_info['info']:
            mask=Mask(x=i['box'][0],y=i['box'][1],width=i['box'][2]-i['box'][0],height=i['box'][3]-i['box'][1],label=i['label'],src_image="./nascar_Extract/{0}".format(img_path))
            self.create_mask(mask)

            
    def load_json(self,json_src):
        try:
            with open(json_src) as f:
                self.json=json.load(f)
        except FileNotFoundError as e:
            print("FileNotFoundError : {0}".format(e))
            raise Exception("JSON is None")
            return None

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
    