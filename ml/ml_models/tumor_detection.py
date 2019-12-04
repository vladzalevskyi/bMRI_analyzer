import os
import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np
from keras import layers
from keras.applications.vgg16 import VGG16
from keras.callbacks import EarlyStopping
from keras.models import Model, Sequential, load_model
from keras.optimizers import RMSprop
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer

absp = os.path.abspath("")
sys.path.append(absp)


# print(keras.backend.tensorflow_backend._get_available_gpus())

RANDOM_SEED = 123
IMG_SIZE = (224, 224)
NUM_CLASSES = 1
EPOCHS = 30


class Classification_Model:
    def __init__(self):
        self.aug = None
        base_model = VGG16(include_top=False, input_shape=IMG_SIZE + (3,))

        self.model = Sequential()
        self.model.add(base_model)
        self.model.add(layers.Flatten())
        self.model.add(layers.Dropout(0.5))
        self.model.add(layers.Dense(NUM_CLASSES, activation='sigmoid'))

        self.model.layers[0].trainable = False

        self.model.compile(
            loss='binary_crossentropy',
            optimizer=RMSprop(lr=1e-4),
            metrics=['accuracy']
        )

        self.model.summary()

    def train_model(self):
        self.aug = ImageDataGenerator(
            rotation_range=15,
            width_shift_range=0.05,
            height_shift_range=0.05,
            rescale=1./255,
            shear_range=0.05,
            brightness_range=[0.1, 1.5],
            horizontal_flip=True,
            vertical_flip=True
        )
        train_generator = aug.flow_from_directory(
            absp + "/data/train/", seed=RANDOM_SEED, target_size=(224, 224), class_mode='binary')
        test_generator = aug.flow_from_directory(
            absp + "/data/test/", seed=RANDOM_SEED, target_size=(224, 224), class_mode='binary')

        es = EarlyStopping(
            monitor='val_acc',
            mode='max',
            patience=6
        )

        history = self.model.fit_generator(
            train_generator,
            steps_per_epoch=50,
            epochs=EPOCHS,
            validation_data=test_generator,
            validation_steps=25,
            callbacks=[es]
        )

    def load_model(self, path_to_model):
        self.model = load_model(path_to_model)

    def predict_image(self, img):
        """Predicts prb of an image having a tumor 

        Arguments:
            img {[np.array]} -- [array representation of image of size (224,224,3); could be got by load_image()]
        """
        pred = self.model.predict(img)
        if pred[0][0] > 0.5:
            return(pred[0][0], f"Tumor detected with a probability: {pred[0][0]}")
        else:
            return(pred[0][0], f"NO tumors detected with a probability: {1- pred[0][0]}")

    def save_model(self, model_name):
        self.model.save(model_name)

    @staticmethod
    def load_image(im_path):

        img = np.array(cv2.imread(im_path))
        img = np.array([cv2.resize(img, dsize=IMG_SIZE)])
        return img
