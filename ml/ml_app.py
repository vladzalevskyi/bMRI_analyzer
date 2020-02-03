import os
import flask

from ml_models.tumor_detection import Classification_Model

from ml_models.tumor_segmentation import Segmentation_Model
from ml_models.tumor_segmentation import config

app = flask.Flask(__name__)


class_model = None
segm_model = None


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


@app.route("/api/detect", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        # read the posted json to dict
        r = flask.request.get_json()
        impath = r["impath"]
        impath = os.path.join(os.path.abspath("../uploads"), impath)
        print(impath)

        image = Classification_Model.load_image(impath)
        prediction, confidence = class_model.predict_image(image)
        result = {"classification": str(prediction)}

        img = Segmentation_Model.load_image(impath)
        segmentation_img = os.path.join(os.path.abspath(
            "../uploads"), "analyzed_" + r["impath"])

        # still plots the resulting image
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

        return flask.jsonify(result)

    # return the data dictionary as a JSON response
    return flask.jsonify(data)


# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    load_detection_model()
    load_segmentation_model()
    app.run(host="0.0.0.0", port=5002, threaded=False)
