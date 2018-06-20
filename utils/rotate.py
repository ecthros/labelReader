from PIL import Image
import utils.logger as logger
import subprocess
import os
import pexpect
from RotNet.correct_rotation import *

### The following constants will most likely not need to be changed ###
ROTNET_LOCATION	= "./RotNet"
MODEL_NAME		= "rotnet_models/rotnet_street_view_resnet50_keras2.hdf5"
SAVE_FILE_NAME	= "tilted.jpg"
#######################################################################

#For speed concerns, let's load up the model first
def initialize_rotnet(model=MODEL_NAME):
	# Head to the RotNet directory and use correct_rotation to lod the model
	init_rotnet(ROTNET_LOCATION + "/" + MODEL_NAME)

# Uses RotNet's Keras/Tensorflow algorithm to rotate an image.
# Input: image, opened with PIL
# Output: Rotated image
def rotate(image):
	# We need to save the file first for processing
	image.save(SAVE_FILE_NAME, "JPEG")

	logger.good("Rotating Image")
	rotate_image(SAVE_FILE_NAME)
	
	image = Image.open(SAVE_FILE_NAME)
	return image
