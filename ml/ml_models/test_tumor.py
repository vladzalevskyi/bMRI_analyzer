"""
from tumor_detection import Classification_Model as CM

model = CM()
model.load_model("tmodel_v0_0_1.h5")
img = CM.load_image("test.jpg")
r = model.predict_image(img)
print(r)

"""
from tumor_segmentation import config
from tumor_segmentation import Segmentation_Model as SM

model = SM(config)
model.load_weights()

img = SM.load_image("normal_mri.jpeg")
res = model.predict_image_(img, save=True, save_path="predicted_test.png")

