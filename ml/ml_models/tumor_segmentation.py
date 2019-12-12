import json
import os
import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np
import skimage.draw
import tensorflow as tf
from matplotlib import lines, patches
from matplotlib.patches import Polygon

# Root directory of the project
ROOT_DIR = os.path.abspath('ml_models/Mask_RCNN/')
# Import Mask RCNN
sys.path.append(ROOT_DIR)

import pycocotools.coco as coco
import mrcnn.model as modellib
from mrcnn import utils, visualize
from mrcnn.config import Config
from mrcnn.model import log



# fixing a tf bug
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
allow_growth_session = tf.Session(config=config)
tf.keras.backend.set_session(allow_growth_session)
# fixing a tf bug


# Import COCO config
sys.path.append(os.path.join(ROOT_DIR, 'samples/coco/'))


plt.rcParams['figure.facecolor'] = 'white'


def get_ax(rows=1, cols=1, size=7):
    """Return a Matplotlib Axes array to be used in
    all visualizations in the notebook. Provide a
    central point to control graph sizes.

    Change the default size attribute to control the size
    of rendered images
    """
    _, ax = plt.subplots(rows, cols, figsize=(size*cols, size*rows))
    return ax


class TumorConfig(Config):
    """Configuration for training on the brain tumor dataset.
    """
    # Give the configuration a recognizable name
    NAME = 'tumor_detector'
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    NUM_CLASSES = 1 + 1  # background + tumor
    DETECTION_MIN_CONFIDENCE = 0.85
    STEPS_PER_EPOCH = 100
    LEARNING_RATE = 0.001


# use this config to create Segmentation class instances
config = TumorConfig()
config.display()


class BrainScanDataset(utils.Dataset):

    def load_brain_scan(self, dataset_dir, subset):
        """Load a subset of the FarmCow dataset.
        dataset_dir: Root directory of the dataset.
        subset: Subset to load: train or val
        """
        # Add classes. We have only one class to add.
        self.add_class("tumor", 1, "tumor")

        # Train or validation dataset?
        assert subset in ["train", "val", 'test']
        dataset_dir = os.path.join(dataset_dir, subset)

        annotations = json.load(
            open(os.path.join(DATASET_DIR, subset, 'annotations_'+subset+'.json')))
        annotations = list(annotations.values())  # don't need the dict keys

        # The VIA tool saves images in the JSON even if they don't have any
        # annotations. Skip unannotated images.
        annotations = [a for a in annotations if a['regions']]

        # Add images
        for a in annotations:
            # Get the x, y coordinaets of points of the polygons that make up
            # the outline of each object instance. These are stores in the
            # shape_attributes (see json format above)
            # The if condition is needed to support VIA versions 1.x and 2.x.
            if type(a['regions']) is dict:
                polygons = [r['shape_attributes']
                            for r in a['regions'].values()]
            else:
                polygons = [r['shape_attributes'] for r in a['regions']]

            # load_mask() needs the image size to convert polygons to masks.
            # Unfortunately, VIA doesn't include it in JSON, so we must read
            # the image. This is only managable since the dataset is tiny.
            image_path = os.path.join(dataset_dir, a['filename'])
            image = skimage.io.imread(image_path)
            height, width = image.shape[:2]

            self.add_image(
                "tumor",
                image_id=a['filename'],  # use file name as a unique image id
                path=image_path,
                width=width,
                height=height,
                polygons=polygons
            )

    def load_mask(self, image_id):
        """Generate instance masks for an image.
       Returns:
        masks: A bool array of shape [height, width, instance count] with
            one mask per instance.
        class_ids: a 1D array of class IDs of the instance masks.
        """
        # If not a farm_cow dataset image, delegate to parent class.
        image_info = self.image_info[image_id]
        if image_info["source"] != "tumor":
            return super(self.__class__, self).load_mask(image_id)

        # Convert polygons to a bitmap mask of shape
        # [height, width, instance_count]
        info = self.image_info[image_id]
        mask = np.zeros([info["height"], info["width"], len(info["polygons"])],
                        dtype=np.uint8)
        for i, p in enumerate(info["polygons"]):
            # Get indexes of pixels inside the polygon and set them to 1
            rr, cc = skimage.draw.polygon(p['all_points_y'], p['all_points_x'])
            mask[rr, cc, i] = 1

        # Return mask, and array of class IDs of each instance. Since we have
        # one class ID only, we return an array of 1s
        return mask.astype(np.bool), np.ones([mask.shape[-1]], dtype=np.int32)

    def image_reference(self, image_id):
        """Return the path of the image."""
        info = self.image_info[image_id]
        if info["source"] == "tumor":
            return info["path"]
        else:
            super(self.__class__, self).image_reference(image_id)


class Segmentation_Model:

    def __init__(self, config, train=False):
        """        
        Arguments:
            config {[TumorConfig]} -- [a class containing model's configs ]

        Keyword Arguments:
            train {bool} -- [whether to train model from the start or no] (default: {False})
        """
        self.config = config
        self.trainedf = False
        # directory to save logs and trained model
        self.MODEL_DIR = os.path.join(ROOT_DIR, 'logs')
        # ANNOTATIONS_DIR = 'brain-tumor/data/new/annotations/' # directory with annotations for train/val sets
        self.DATASET_DIR = 'brain-tumor/data_cleaned/'  # directory with image data
        self.DEFAULT_LOGS_DIR = 'logs'

        # Local path to trained weights file
        self.COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
        # Download COCO trained weights from Releases if needed
        if not os.path.exists(self.COCO_MODEL_PATH):
            utils.download_trained_weights(self.COCO_MODEL_PATH)

        if train:
            self.model = modellib.MaskRCNN(
                # mode='training',
                mode='training',
                config=config,
                model_dir=self.DEFAULT_LOGS_DIR)
        else:
            self.model = modellib.MaskRCNN(
                # mode='training',
                mode='inference',
                config=config,
                model_dir=self.DEFAULT_LOGS_DIR)

    def _prepare_data_for_training(self):
        # Training dataset.
        self.dataset_train = BrainScanDataset()
        self.dataset_train.load_brain_scan(self.DATASET_DIR, 'train')
        self.dataset_train.prepare()

        # Validation dataset
        self.dataset_val = BrainScanDataset()
        self.dataset_val.load_brain_scan(self.DATASET_DIR, 'val')
        self.dataset_val.prepare()

        self.dataset_test = BrainScanDataset()
        self.dataset_test.load_brain_scan(self.DATASET_DIR, 'test')
        self.dataset_test.prepare()

    def train_model(self):
        _prepare_data_for_training(self)
        # Since we're using a very small dataset, and starting from
        # COCO trained weights, we don't need to train too long. Also,
        # no need to train all layers, just the heads should do it.
        print("Training network heads")
        self.model.train(
            self.dataset_train, self.dataset_val,
            learning_rate=self.config.LEARNING_RATE,
            epochs=15,
            layers='heads')
        self.trainedf = True

    def load_weights(self, last=False, model_path=None):
        # Get path to saved weights
        # Either set a specific path or find last trained weights
        model_path = os.path.join(ROOT_DIR, "mask_rcnn_tumor_detector_0015.h5")
        if last:
            model_path = self.model.find_last()

        # Load trained weights
        print("Loading weights from ", model_path)
        self.model.load_weights(model_path, by_name=True)
        self.trainedf = True

    def predict_image_(self, image, plot=True, save=False, save_path=None):
        """Predicts tumor's mask and box for a given image

        Arguments:
            image {[np.array(np.float64)]} -- [np.array of shape (1024,1024,3) of an image]

        Raises:
            NotImplementedError: [If model isn't trained yet or has no weights loaded]
        """
        if not self.trainedf:
            raise NotImplementedError("NotTrainedError")

        r = self.model.detect([image], verbose=0)[0]
        conf = r['scores']
        r["tumor_detected"] = True



        #if found no tumor on the image
        if len(r["rois"]) == 0:
            r["tumor_detected"] = False
            return r


    
        mask = np.reshape(r['masks'], (1024, 1024))
        y1, x1, y2, x2 = r['rois'][0]
        p = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=4,
                              alpha=0.3, linestyle="dashed",
                              edgecolor='r', facecolor='none')
        fig = plt.figure()
        ax = plt.gca()


        ax.add_patch(p)
        ax.imshow(image)
        ax.imshow(mask, cmap='jet', alpha=0.5)  # interpolation='none'
        if plot:        
            plt.show()
        if save:
            fig.savefig(save_path)

        return r

    @staticmethod
    def load_image(im_path):
        """Reads image from file

        Arguments:
            im_path {[str]} -- [path ti image]

        Returns:
            [np.array] -- [array representation of image with shape (1024,1024,3); could be got by load_image()]
        """

        custom_im = cv2.imread(im_path)
        custom_im = cv2.resize(custom_im, (1024, 1024))
        return custom_im

    def __predict_and_plot_differences(self, dataset, img_id):
        original_image, image_meta, gt_class_id, gt_box, gt_mask =\
            modellib.load_image_gt(dataset, self.config,
                                   img_id, use_mini_mask=False)

        results = self.model.detect([original_image], verbose=0)
        r = results[0]

        visualize.display_differences(
            original_image,
            gt_box, gt_class_id, gt_mask,
            r['rois'], r['class_ids'], r['scores'], r['masks'],
            class_names=['tumor'], title="", ax=get_ax(),
            show_mask=True, show_box=True)

    def __display_image(self, dataset, ind):
        plt.figure(figsize=(5, 5))
        plt.imshow(dataset.load_image(ind))
        plt.xticks([])
        plt.yticks([])
        plt.title('Original Image')
        plt.show()


"""

ind = 0
display_image(dataset_val, ind)
predict_and_plot_differences(dataset_val, ind)

ind = 10
display_image(dataset_val, ind)
img = predict_and_plot_differences(dataset_val, ind)



ind = 4
display_image(dataset_val, ind)
img =predict_and_plot_differences(dataset_val, ind)

ind = 0
display_image(dataset_test, ind)
predict_and_plot_differences(dataset_test, ind)

ind = 2
display_image(dataset_test, ind)
img = predict_and_plot_differences(dataset_test, ind)
"""
