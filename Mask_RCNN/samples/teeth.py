import os
import sys
import json
import numpy as np
import datetime
import skimage.io
from skimage import data, draw
from skimage import transform, util
from skimage import filters, color
from matplotlib import pyplot as plt

# Root directory of the project
ROOT_DIR = os.path.abspath("../../")
# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn.config import Config
from mrcnn import model as modellib, utils
from mrcnn import visualize

# Path to trained weights file
COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# Directory to save logs and model checkpoints, if not provided
# through the command line argument --logs
DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")
RESULTS_DIR = os.path.join(ROOT_DIR, "results/teeth/")

dic = { 'teeth' : 'teeth.1', 'acid' : 'teeth.2','silver':'teeth.3', 'gold':'teeth.4'}

#===========================
class TeethConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "teeth"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 2

    # Number of classes (including background)
    NUM_CLASSES = 1 + 4  # Background + teeth_class

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 203

    # 작은 이미지일때 속도가 증가
    IMAGE_MIN_DIM = 1024
    IMAGE_MAX_DIM = 1024

    # 여러가지 크기를 설정(이미지와 물체 구분이 되도록)
    RPN_ANCHOR_SCALES = (32, 128, 384, 728, 1000)

    # 이미지당 ROIS 을 설정
    TRAIN_ROIS_PER_IMAGE = 32

    # 점검
    VALIDATION_STPES = 10


class TeethDataset(utils.Dataset):
    def load_teeth(self,dataset_dir,subset):
        
        
        self.add_class("teeth",1,"teeth")
        self.add_class("teeth",2,"acid")
        self.add_class("teeth",3,"silver")
        self.add_class("teeth",4,"gold")
        
        
        assert subset in ["train","val"]
        dataset_dir = os.path.join(dataset_dir,subset)
        file_list = next(os.walk(dataset_dir))[2]
        file_list.sort()

        annotations_list = []

        for f in file_list:
            if f.endswith(".json"):
                annotations_list.append(json.load(open(os.path.join(dataset_dir,f))))

        for annotation in annotations_list:
            image_path = os.path.join(dataset_dir,annotation["imagePath"])
            image = skimage.io.imread(image_path)
            height, width = image.shape[:2]
            self.add_image("teeth",image_id=annotation["imagePath"],path=image_path,width=width,height=height,annotation=annotation["shapes"])
            
        

    def load_mask(self,image_id):
        image_info = self.image_info[image_id]
        if image_info["source"] != "teeth":
            return super(self.__class__,self).load_mask(image_id)
        info = self.image_info[image_id]
        count = len(info["annotation"])
        mask = np.zeros([info["height"], info["width"], count],dtype=np.uint8)
        polygon_list =[]
        class_ids = []
        
        for i in info["annotation"]:
            polygon_list.append(i["points"])
            class_id = self.map_source_class_id(dic[i['label']])
            class_ids.append(class_id)

        for i,poly in enumerate(polygon_list):
            pc = np.array([p[0] for p in poly])
            pr = np.array([p[1] for p in poly])
            rr,cc = draw.polygon(pr,pc)
            mask[rr, cc, i] = 1

        occlusion = np.logical_not(mask[:, :, -1]).astype(np.uint8)
        for i in range(count - 2, -1, -1):
            mask[:, :, i] = mask[:, :, i] * occlusion
            occlusion = np.logical_and(
                occlusion, np.logical_not(mask[:, :, i]))
        # one classes
        # return mask.astype(np.bool), np.ones([mask.shape[-1]], dtype=np.int32)
        return mask.astype(np.bool), np.array(class_ids, dtype=np.int32)

    def image_reference(self, image_id):
        """Return the path of the image."""
        info = self.image_info[image_id]
        if info["source"] == "teeth":
            return info["path"]
        else:
            super(self.__class__, self).image_reference(image_id)


def train(model):
    """Train the model."""
    # Training dataset.
    dataset_train = TeethDataset()
    dataset_train.load_teeth(args.dataset, "train")
    dataset_train.prepare()

    # Validation dataset
    dataset_val = TeethDataset()
    dataset_val.load_teeth(args.dataset, "val")
    dataset_val.prepare()

    # *** This training schedule is an example. Update to your needs ***
    # Since we're using a very small dataset, and starting from
    # COCO trained weights, we don't need to train too long. Also,
    # no need to train all layers, just the heads should do it.
    print("Training network heads")
    model.train(dataset_train, dataset_val,
                learning_rate=config.LEARNING_RATE,
                epochs=50,
                layers='heads')

    # print("Train all layers")
    # model.train(dataset_train, dataset_val,
    #             learning_rate=config.LEARNING_RATE,
    #             epochs=20,layers='all')


############################################################
#  RLE Encoding
############################################################

def rle_encode(mask):
    """Encodes a mask in Run Length Encoding (RLE).
    Returns a string of space-separated values.
    """
    assert mask.ndim == 2, "Mask must be of shape [Height, Width]"
    # Flatten it column wise
    m = mask.T.flatten()
    # Compute gradient. Equals 1 or -1 at transition points
    g = np.diff(np.concatenate([[0], m, [0]]), n=1)
    # 1-based indicies of transition points (where gradient != 0)
    rle = np.where(g != 0)[0].reshape([-1, 2]) + 1
    # Convert second index in each pair to lenth
    rle[:, 1] = rle[:, 1] - rle[:, 0]
    return " ".join(map(str, rle.flatten()))


def rle_decode(rle, shape):
    """Decodes an RLE encoded list of space separated
    numbers and returns a binary mask."""
    rle = list(map(int, rle.split()))
    rle = np.array(rle, dtype=np.int32).reshape([-1, 2])
    rle[:, 1] += rle[:, 0]
    rle -= 1
    mask = np.zeros([shape[0] * shape[1]], np.bool)
    for s, e in rle:
        assert 0 <= s < mask.shape[0]
        assert 1 <= e <= mask.shape[0], "shape: {}  s {}  e {}".format(shape, s, e)
        mask[s:e] = 1
    # Reshape and transpose
    mask = mask.reshape([shape[1], shape[0]]).T
    return mask


def mask_to_rle(image_id, mask, scores):
    "Encodes instance masks to submission format."
    assert mask.ndim == 3, "Mask must be [H, W, count]"
    # If mask is empty, return line with image ID only
    if mask.shape[-1] == 0:
        return "{},".format(image_id)
    # Remove mask overlaps
    # Multiply each instance mask by its score order
    # then take the maximum across the last dimension
    order = np.argsort(scores)[::-1] + 1  # 1-based descending
    mask = np.max(mask * np.reshape(order, [1, 1, -1]), -1)
    # Loop over instance masks
    lines = []
    for o in order:
        m = np.where(mask == o, 1, 0)
        # Skip if empty
        if m.sum() == 0.0:
            continue
        rle = rle_encode(m)
        lines.append("{}, {}".format(image_id, rle))
    return "\n".join(lines)

############################################################
#  Detection
############################################################
def get_ax(rows=1, cols=1, size=16):
    """Return a Matplotlib Axes array to be used in
    all visualizations in the notebook. Provide a
    central point to control graph sizes.
    
    Adjust the size attribute to control how big to render images
    """
    _, ax = plt.subplots(rows, cols, figsize=(size*cols, size*rows))
    return ax

def simply_polygon(polygons):
    simply = []

    tpoint = None

    for polygon in polygons:

        points = []

        for point in polygon:

            if tpoint is None:

                tpoint = point

                points.append(tpoint)

            else:

                if tpoint[0] != point[0] and tpoint[1] != point[1]:

                    points.append(tpoint)

                tpoint = point

        if points[0][0] != points[-1][0] and points[0][1] != points[-1][1]:
            points.append(points[0])

        simply.append(points)

    return simply

def visualize_instance(image, boxes, masks, class_ids, class_names,scores=None, title="",figsize=(16, 16), ax=None,show_mask=True, show_bbox=True,colors=None, captions=None):

    from skimage.measure import find_contours
    import matplotlib.pyplot as plt
    from matplotlib import patches, lines
    from matplotlib.patches import Polygon
    import random
    import json


    # Number of instances
    N = boxes.shape[0]
    
    title = 'teeth'
    if not N:
        print("\n*** No instances to display *** \n")
    else:
        assert boxes.shape[0] == masks.shape[-1] == class_ids.shape[0]

    # If no axis is passed, create one and automatically call show()
    auto_show = False
    if not ax:
        _, ax = plt.subplots(1, figsize=figsize)
        auto_show = True

    height, width = image.shape[:2]
    ax.set_ylim(height + 10, -10)
    ax.set_xlim(-10, width + 10)
    ax.set_title(title)

    colors = visualize.random_colors(N)
    masked_image = image.astype(np.uint32).copy()

    info_list = {'instance':'{}'.format(N)}
    tmp_dic_list = []


    y_sum = 0
    for i in range(N):
        # Mask
        color = colors[i]
        # Bounding box
        if not np.any(boxes[i]):
            # Skip this instance. Has no bbox. Likely lost in image cropping.
            continue
        y1, x1, y2, x2 = boxes[i]
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
            x = random.randint(x1, (x1 + x2) // 2)
            caption = "{} {:.3f}".format(label, score) if score else label
        else:
            caption = captions[i]
        ax.text(x1, y1 + 8, caption,
                color='w', size=11, backgroundcolor="none")            
        
        mask = masks[:, :, i]
        masked_image = visualize.apply_mask(masked_image, mask, color)

        # Mask Polygon
        # Pad to ensure proper polygons for masks that touch image edges.
        padded_mask = np.zeros(
            (mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
        padded_mask[1:-1, 1:-1] = mask
        contours = find_contours(padded_mask, 0.5)
        
        polygon_list =[]
        for verts in contours:
            # Subtract the padding and flip (y, x) to (x, y)
            verts = np.fliplr(verts) - 1
            p = Polygon(verts, facecolor="none",edgecolor=color)
            if len(p.get_path().vertices) < 50:
                continue
            polygon_list.append(p.get_path().vertices)
            ax.add_patch(p)
        if len(polygon_list) ==0:
            continue
        data_list = simply_polygon(polygon_list)
        x_list = []
        y_list = []
        result = []
        
        for p in data_list[0]:
            x_list.append(p[0])
            y_list.append(p[1])
            result.append(p)

        x_max = max(x_list)
        y_max = max(y_list)
        x_min = min(x_list)
        y_min = min(y_list)
        avgX = (x_max + x_min) / 2
        avgY = (y_max + y_min) / 2
        y_sum += avgY
    #     print("x_min:{} x_max:{}".format(x_min,x_max))
    #     print("y_min:{} y_max:{}".format(y_min,y_max))
    #     print("avgX:{} avgY:{}".format(avgX,avgY))
        result = sorted(result,key=lambda x: x[0])
    #     print("\n\n\n\n\n sorted \n\n\n\n")
    #     print(result)
        distance = (x_max-x_min,y_max-y_min)
        center_point = (avgX,avgY)
    
        info_dic = {'polygons':result,'distance': distance,'center_point':center_point}
        tmp_dic_list.append(info_dic)
    
        xline = lines.Line2D([x_min,x_max],[avgY,avgY])
        yline = lines.Line2D([(avgX,avgX)],[(y_min,y_max)])
        
        ax.add_line(xline)
        ax.add_line(yline)
        
        if i == N-1:
            up_count = 1
            down_count = 1
            y_avg = y_sum / N
            mid = int(N / 4)
            print("mid {}".format(mid))
            pixelsPerMetrics = None
            info_list['shape'] = sorted(tmp_dic_list,key=lambda x:x['center_point'][0])
            for info in info_list['shape']:
                data = info['center_point']
                if data[1] < y_avg:
                    if up_count == mid:     
                        _,axis = info['distance']
                        # print(axis)
                        pixelsPerMetrics = axis / 1.0  
                    info['location'] = 'up{}'.format(up_count)
                    up_count += 1
                    print("upcount {}".format(up_count))
                    
                elif data[1] > y_avg:
                    info['location'] = 'down{}'.format(down_count)
                    down_count +=1
            
            for info in info_list['shape']:
                x,y = info['center_point']
                width,height = info['distance']
                print(width,height,pixelsPerMetrics)
                dimA = width / pixelsPerMetrics
                dimB = height / pixelsPerMetrics
                x_text = "w : {0:0.3f}".format(dimA)
                y_text = "h : {0:0.3f}".format(dimB)
                ax.text(x-40, y + 20, x_text,
                    color='r', size=9, backgroundcolor="none")
                ax.text(x+10, y - 10, y_text,
                    color='b', size=9, backgroundcolor="none")
        
        ax.imshow(masked_image.astype(np.uint8))            
        if auto_show:
            plt.show();         

def detect(model, dataset_dir,subset):
    """Run detection on images in the given directory."""
    print("Running on {}".format(dataset_dir))

    # Create directory
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
    submit_dir = "submit_{:%Y%m%dT%H%M%S}".format(datetime.datetime.now())
    submit_dir = os.path.join(RESULTS_DIR, submit_dir)
    os.makedirs(submit_dir)

    # Read dataset
    dataset = TeethDataset()
    dataset.load_teeth(dataset_dir, subset)
    dataset.prepare()
    # Load over images
    submission = []
    for image_id in dataset.image_ids:
        # Load image and run detection
        image = dataset.load_image(image_id)
        # Detect objects
        ax = get_ax(1)
        r = model.detect([image], verbose=0)[0]
        # Encode image to RLE. Returns a string of multiple lines
        source_id = dataset.image_info[image_id]["id"]
        rle = mask_to_rle(source_id, r["masks"], r["scores"])
        submission.append(rle)
        # Save image with masks
        # visualize.display_instances(
        #     image, r['rois'], r['masks'], r['class_ids'],
        #     dataset.class_names, r['scores'],
        #     show_bbox=False, show_mask=False,
        #     title="Predictions")
        visualize_instance(image,r['rois'],r['masks'],r['class_ids'],dataset.class_names,r['scores'],
        show_bbox=True,ax=ax,show_mask=True,title="Predictions")
        plt.savefig("{}/{}.png".format(submit_dir, dataset.image_info[image_id]["id"]))
#
#     # Save to csv file
#     submission = "ImageId,EncodedPixels\n" + "\n".join(submission)
#     file_path = os.path.join(submit_dir, "submit.csv")
#     with open(file_path, "w") as f:
#         f.write(submission)
#     print("Saved to ", submit_dir)

############################################################
#  Training
############################################################

if __name__ == '__main__':
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Train Mask R-CNN to detect teeths.')
    parser.add_argument("command",
                        metavar="<command>",
                        help="'train' or 'detect'")
    parser.add_argument('--dataset', required=False,
                        metavar="/path/to/teeth/dataset/",
                        help='Directory of the teeth dataset')
    parser.add_argument('--weights', required=True,
                        metavar="/path/to/weights.h5",
                        help="Path to weights .h5 file or 'coco'")
    parser.add_argument('--logs', required=False,
                        default=DEFAULT_LOGS_DIR,
                        metavar="/path/to/logs/",
                        help='Logs and checkpoints directory (default=logs/)')
    parser.add_argument('--image', required=False,
                        metavar="path or URL to image",
                        help='Image to apply the color splash effect on')
    parser.add_argument('--video', required=False,
                        metavar="path or URL to video",
                        help='Video to apply the color splash effect on')
    args = parser.parse_args()

    # Validate arguments
    if args.command == "train":
        assert args.dataset, "Argument --dataset is required for training"

    print("Weights: ", args.weights)
    print("Dataset: ", args.dataset)
    print("Logs: ", args.logs)

    # Configurations
    if args.command == "train":
        config = TeethConfig()
    else:
        class InferenceConfig(TeethConfig):
            # Set batch size to 1 since we'll be running inference on
            # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
            GPU_COUNT = 1
            IMAGES_PER_GPU = 1
        config = InferenceConfig()
    config.display()

    # Create model
    if args.command == "train":
        model = modellib.MaskRCNN(mode="training", config=config,
                                  model_dir=args.logs)
    else:
        model = modellib.MaskRCNN(mode="inference", config=config,
                                  model_dir=args.logs)

    # Select weights file to load
    if args.weights.lower() == "coco":
        weights_path = COCO_WEIGHTS_PATH
        # Download weights file
        if not os.path.exists(weights_path):
            utils.download_trained_weights(weights_path)
    elif args.weights.lower() == "last":
        # Find last trained weights
        weights_path = model.find_last()
    elif args.weights.lower() == "imagenet":
        # Start from ImageNet trained weights
        weights_path = model.get_imagenet_weights()
    else:
        weights_path = args.weights

    # Load weights
    print("Loading weights ", weights_path)
    if args.weights.lower() == "coco":
        # Exclude the last layers because they require a matching
        # number of classes
        model.load_weights(weights_path, by_name=True, exclude=[
            "mrcnn_class_logits", "mrcnn_bbox_fc",
            "mrcnn_bbox", "mrcnn_mask"])
    else:
        model.load_weights(weights_path, by_name=True)

    # Train or evaluate
    if args.command == "train":
        train(model)
    elif args.command == "detect":
         detect(model,args.dataset,"train")

    else:
        print("'{}' is not recognized. "
              "Use 'train' or 'detect'".format(args.command))
