import video_infos

# import test
vi=video_infos.VideoInfos("../dataset/vdd/info/b726c429-11f5acde.json")

a=vi.select_genel([x for x in range(200,300)])
print(len(a),vi.len)
if( len(a) == vi.len ):
    print("test succes")

#
IMAGE_DIR = "./vdd"
import os
file_names = next(os.walk(IMAGE_DIR))[2]

# sort list
for i in range(len(file_names)):
    for j in range(len(file_names)):
        if(file_names[i].endswith(".jpg") and file_names[j].endswith(".jpg")):
            if( int(file_names[i].replace("b726c429-11f5acde","").replace(".jpg","")) < int(file_names[j].replace("b726c429-11f5acde","").replace(".jpg","")) ):
                temp=file_names[i]
                file_names[i]=file_names[j]
                file_names[j]=temp
print("###############")
print(len(file_names),vi.len)

import video_infos
vi=video_infos.VideoInfos("../dataset/vdd/info/b726c429-11f5acde.json")
file_names=vi.select_genel(file_names)

print("video_infos test #############")
print(len(file_names),vi.len)