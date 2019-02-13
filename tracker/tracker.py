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

from tracker.instance.instance import Instance

class Tracker:
    def __init__(self):
        pass
    
    def get_result(self):
        return []