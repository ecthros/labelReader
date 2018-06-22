from PIL import Image
import utils.logger as logger
import subprocess
import os
import pexpect
from RotNet.correct_rotation import *
from config import *
import time

#For speed concerns, let's load up the model first
def initialize_rotnet():
	# Head to the RotNet directory and use correct_rotation to lod the model
	init_rotnet(ROTNET_LOCATION + "/" + ROTNET_MODEL_NAME)

# Uses RotNet's Keras/Tensorflow algorithm to rotate an image.
# Input: image, opened with PIL
# Output: Rotated image
def rotate(image):
	# We need to save the file first for processing
	image.save(ROTNET_SAVE_FILE_NAME, "JPEG")

	logger.good("Rotating Image")
	rotate_image(ROTNET_SAVE_FILE_NAME)
	image = Image.open(ROTNET_SAVE_FILE_NAME)
	return image
