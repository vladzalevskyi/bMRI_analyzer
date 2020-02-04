import os

from fastapi import FastAPI
from pydantic import BaseModel

from ml_models.tumor_detection import Classification_Model
from ml_models.tumor_segmentation import Segmentation_Model, config

app = FastAPI()


class_model = None
segm_model = None


class Request(BaseModel):
    impath: str


def load_detection_model():
    global class_model
    class_model = Classification_Model()
    class_model.load_model("ml_models/tmodel_v0_0_1.h5")
    print("**Classification model loaded**")


def load_segmentation_model():
    global segm_model
    segm_model = Segmentation_Model(config)
    segm_model.load_weights()
    print("**Segmentation model loaded**")


@app.post("/api/detect")
async def predict(item: Request):

    # ensure an image was properly uploaded to our endpoint
    # read the posted json to dict
    item_dict = item.dict()
    impath = item_dict["impath"]
    impath = os.path.join(os.path.abspath("../uploads"), impath)


    image = Classification_Model.load_image(impath)
    prediction, confidence = class_model.predict_image(image)
    result = {"classification": str(prediction)}

    img = Segmentation_Model.load_image(impath)
    segmentation_img = os.path.join(os.path.abspath(
        "../uploads"), "analyzed_" + item_dict["impath"])

    # plots the resulting image
    # and can't finish the process without closing it
    segm = segm_model.predict_image_(
        img, save=True, plot=False, save_path=segmentation_img)

    if segm["tumor_detected"] == False:
        result["segmentation_img"] = impath.split("/")[-1]
        result["tumor_detected"] = False
        result["confidence"] = float(confidence)
        print(segmentation_img.split("/")[-1], "*"*500)

    else:
        result["tumor_detected"] = True
        result["confidence"] = float(confidence)
        result["segmentation_img"] = segmentation_img.split("/")[-1]

    result["segmentation"] = str(segm["rois"])

    return result


print(("* Loading Keras model and Flask starting server..."
       "please wait until server has fully started"))
load_detection_model()
load_segmentation_model()