#--------------------------------------------------------------------
# Podex - Web scraping
# Using yolo3 to detect birds in the picture
#  !!! DRAFT !!!
#--------------------------------------------------------------------

#--------------------------------------------------------------------
# Settings

import cv2
import cvlib as cv
#from darknet import Darknet
from cvlib.object_detection import draw_bbox


import numpy as np
import matplotlib.pyplot as plt

#--------------------------------------------------------------------
# File paths

DATA = 'C:/Users/wb519128/Dropbox/Work/Pessoal/Pokedex/'
CODE = 'C:/Users/wb519128/GitHub/pokedex/'
# YOLO = CODE + 'yolo-coco/'

# #--------------------------------------------------------------------
# # Yolo settings
# yolo_cfg_file = YOLO + 'yolov3.cfg'
# yolo_weight_file = YOLO + 'yolov3.weights'
# yolo_namesfile = YOLO + 'coco.names'

# # Load the network architecture
# m = Darknet(yolo_cfg_file)

# # Load the pre-trained weights
# m.load_weights(yolo_weight_file)

# # Load the COCO object classes
# class_names = load_class_names(yolo_namesfile)

#--------------------------------------------------------------------
# Load test images
im = cv2.imread(DATA + 'Sabia-cica/Pokedeximg_41.jpg')

bbox, label, conf = cv.detect_common_objects(im)
output_image = draw_bbox(im, bbox, label, conf)
plt.imshow(output_image)
plt.show()
