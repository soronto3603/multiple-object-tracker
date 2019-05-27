import os
import sys
import random
import math
import json
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
import colorsys

import itertools

import numpy as np
from skimage.measure import find_contours
import matplotlib.pyplot as plt
from matplotlib import patches,  lines
from matplotlib.patches import Polygon
import IPython.display
from mrcnn.config import Config

# Root directory of the project
ROOT_DIR = os.path.abspath("../")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
# Import COCO config
sys.path.append(os.path.join(ROOT_DIR, "../coco/"))  # To find local version
import coco

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

# Directory of images to run detection on
IMAGE_DIR = os.path.join(ROOT_DIR, "images")

class CocoConfig(Config):
    """Configuration for training on MS COCO.
    Derives from the base Config class and overrides values specific
    to the COCO dataset.
    """
    # Give the configuration a recognizable name
    NAME = "coco"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 2

    # Uncomment to train on 8 GPUs (default is 1)
    # GPU_COUNT = 8

    # Number of classes (including background)
    NUM_CLASSES = 1 + 80  # COCO has 80 classes


class InferenceConfig(CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
config.display()

# Create model object in inference mode.
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# Load weights trained on MS-COCO
model.load_weights(COCO_MODEL_PATH, by_name=True)

# COCO Class names
# Index of the class in the list is its ID. For example, to get ID of
# the teddy bear class, use: class_names.index('teddy bear')
class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']
def random_colors(N, bright=True):
    """
    Generate random colors.
    To get visually distinct colors, generate them in HSV space then
    convert to RGB.
    """
    brightness = 1.0 if bright else 0.7
    hsv = [(i / N, 1, brightness) for i in range(N)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    random.shuffle(colors)
    return colors

def apply_mask(image, mask, color, alpha=0.5):
    """Apply the given mask to the image.
    """
    for c in range(3):
        image[:, :, c] = np.where(mask == 1,
                                  image[:, :, c] *
                                  (1 - alpha) + alpha * color[c] * 255,
                                  image[:, :, c])
    return image

def display_instances(image, boxes, masks, class_ids, class_names,
                      scores=None, title="",
                      figsize=(16, 16), ax=None,
                      show_mask=True, show_bbox=True,
                      colors=None, captions=None):
    """
    boxes: [num_instance, (y1, x1, y2, x2, class_id)] in image coordinates.
    masks: [height, width, num_instances]
    class_ids: [num_instances]
    class_names: list of class names of the dataset
    scores: (optional) confidence scores for each box
    title: (optional) Figure title
    show_mask, show_bbox: To show masks and bounding boxes or not
    figsize: (optional) the size of the image
    colors: (optional) An array or colors to use with each object
    captions: (optional) A list of strings to use as captions for each object
    """
    # Number of instances
    N = boxes.shape[0]
    if not N:
        print("\n*** No instances to display *** \n")
    else:
        assert boxes.shape[0] == masks.shape[-1] == class_ids.shape[0]

    # If no axis is passed, create one and automatically call show()
    auto_show = False
    if not ax:
        _, ax = plt.subplots(1, figsize=figsize)
        auto_show = True

    # Generate random colors
    colors = colors or random_colors(N)

    # Show area outside image boundaries.
    height, width = image.shape[:2]
    ax.set_ylim(height + 10, -10)
    ax.set_xlim(-10, width + 10)
    ax.axis('off')
    ax.set_title(title)

    masked_image = image.astype(np.uint32).copy()

    infos=[]

    for i in range(N):
        info={}

        color = colors[i]


        # Bounding box
        if not np.any(boxes[i]):
            # Skip this instance. Has no bbox. Likely lost in image cropping.
            continue
        y1, x1, y2, x2 = boxes[i]
        info['box']=boxes[i].tolist()
        if show_bbox:
            p = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2,
                                alpha=0.7, linestyle="dashed",
                                edgecolor=color, facecolor='none')
            ax.add_patch(p)

        # Label
        if not captions:
            class_id = class_ids[i]
            score = scores[i] if scores is not None else None
            label = class_names[class_id]
            info['label']=label
            caption = "{} {:.3f}".format(label, score) if score else label
        else:
            caption = captions[i]
        ax.text(x1, y1 + 8, caption,
                color='w', size=11, backgroundcolor="none")
        
        # Mask
        mask = masks[:, :, i]
        if show_mask:
            masked_image = apply_mask(masked_image, mask, color)

        # Mask Polygon
        # Pad to ensure proper polygons for masks that touch image edges.
        padded_mask = np.zeros(
            (mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
        padded_mask[1:-1, 1:-1] = mask
        contours = find_contours(padded_mask, 0.5)
        
        polygons=[]
        for verts in contours:
            # Subtract the padding and flip (y, x) to (x, y)
            verts = np.fliplr(verts) - 1
            p = Polygon(verts, facecolor="none", edgecolor=color)
            polygons.append(verts.tolist())
            ax.add_patch(p)
        info['polygons']=polygons

        infos.append(info)

    # ax.imshow(masked_image.astype(np.uint8))
    # if auto_show:
        # plt.show()

    return infos

# video_infos.py
import json
import gpxpy
import gpxpy.gpx


class VideoInfos:
    def __init__(self,file):
        with open(file) as data_file:

            gpx = gpxpy.parse(data_file)

   
            for track in gpx.tracks:
                for segment in track.segments:           
                    self.len = len(segment.points)
                    break
                    # for point in segment.points:
                    #     print(point.latitude,point.longitude,point.time)
            
            # self.data = json.load(data_file)
            # self.len = len(self.data['locations'])

            self.data = ""
            print(self.len)
        
    def __repr__(self):
        pass
        # print(self.data.keys())
        # print(len(self.data['locations']))

    # 입력 이미지를 json의 타임스탬프 기준으로 평준하게/골고루 맞춰줌 
    def select_genel(self,input_images):
        len_input_images = len(input_images)

        new_list = []
    
        if( len_input_images > self.len ):
            rate = len_input_images / self.len

            idx = 0
            while(True):
                if(round(idx) >= len(input_images) ):
                    break

                new_list.append( input_images[round(idx)] )
                idx+=rate
                    

            
            return new_list
        else:
            # 이미지 개수가 모자람
            pass


def run(dirpath,filename):
    # Load a random image from the images folder
    IMAGE_DIR = "./vdd"
    file_names = next(os.walk(dirpath))[2]

    # sort list
    for i in range(len(file_names)):
        for j in range(len(file_names)):
            if(file_names[i].endswith(".jpg") and file_names[j].endswith(".jpg")):
                if( file_names[i] == "output.jpg"):continue
                
                try:
                    if( int(file_names[i].replace(filename,"").replace(".jpg","")) < int(file_names[j].replace(filename,"").replace(".jpg","")) ):
                        temp=file_names[i]
                        file_names[i]=file_names[j]
                        file_names[j]=temp
                except ValueError as e:
                    print(e)

    vi=VideoInfos(dirpath+"output.gpx")
    file_names=vi.select_genel(file_names)

    print("video_infos test #############")
    print(len(file_names),vi.len)

    image_infos=[]
    for file_name in file_names:
        if file_name.endswith('.jpg'):
            image = skimage.io.imread(os.path.join(dirpath, file_name))

            # Run detection
            results = model.detect([image], verbose=1)
            r = results[0]

            # print(results)
            # print(len(r['rois']))
            # print(len(r['class_ids']))
            # print(len(r['scores']))
            # print((r['masks'][0][0:1]))

            # Visualize results
            infos=display_instances(image, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])
            # print("infos:",infos)
            file_info={'file_name':file_name,'infos':infos}
            image_infos.append(file_info)

    with open(dirpath+'infos.json','w') as f:
        json.dump(image_infos,f,ensure_ascii=False)
    print(image_infos)

