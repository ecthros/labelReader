import os
import argparse

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--darknet', dest='DARKNET', action='store_true')
	parser.add_argument('-k', '--keras', dest='KERAS', action='store_true')
	parser.add_argument('-t', '--tesseract', dest='TESSERACT', action='store_true')
	parser.add_argument('-c', '--cognitive_services', dest='COGNITIVE_SERVICES', action='store_true')
	parser.add_argument('-l', '--dbl', dest="DARKNET_BINARY_LOCATION", default=None)
	args = parser.parse_args()
	return args


## Change the following variable based on what algorithms you want to use ##
global DARKNET, KERAS, TESSERACT, COGNITIVE_SERVICES, DARKNET_BINARY_LOCATION, DARKNET_THRESH, DARKNET_DATA_FILE, \
                DARKNET_CFG_FILE, DARKNET_WEIGHTS, KERAS, KERAS_LOCATION, SUBSCRIPTION_KEY, SHOW_RESPONSE, SHOW_IMAGES, \
                LABEL_NAME, ROTNET_LOCATION, ROTNET_MODEL_NAME, ROTNET_SAVE_FILE_NAME

args = parse_args()

# One of {DARKNET, KERAS} needs to be true
# Specifies which classifier to use
DARKNET = args.DARKNET
KERAS = args.KERAS

# One of {TESSERACT, COGNITIVE_SERVICES} needs to be true
# Specifies which OCR to use
TESSERACT = args.TESSERACT
COGNITIVE_SERVICES = args.COGNITIVE_SERVICES

############################################################################

##### Darknet Information - Change if necessary to fit your needs #####

if DARKNET:
	if args.DARKNET_BINARY_LOCATION == None:
		if os.name == 'nt':
			global popen_spawn
			from pexpect import popen_spawn
			DARKNET_BINARY_LOCATION = "darknet.exe"
		else:
			DARKNET_BINARY_LOCATION = "./darknet"
	else:
		DARKNET_BINARY_LOCATION = args.DARKNET_BINARY_LOCATION

	#### Change the following attributes if you move the files/weights ####
	DARKNET_THRESH    = .25
	DARKNET_DATA_FILE = "data/obj.data"
	DARKNET_CFG_FILE  = "yolo-obj.cfg"
	DARKNET_WEIGHTS   = "yolo-obj_1600.weights"
	
#######################################################################

##### Keras Information - Change if necessary to fit your needs #####

elif KERAS:
	if os.name == 'nt':
		global popen_spawn
		from pexpect import popen_spawn

	# Change the location of Keras-yolo3 if you 
	# move it. You will need to change Keras-yolo's 
	# source code with the changes for the weights.
	KERAS_LOCATION = "keras-yolo3/"

#####################################################################

#### Cognitive Services Information ####

SUBSCRIPTION_KEY = ""
SHOW_RESPONSE = True

########################################

################ Locate_asset information ################

# Determines if we should show images after cropping them
SHOW_IMAGES = False
# Name of the labels
LABEL_NAME = 'label'

##########################################################
########################## RotNet Constants ###########################
### The following constants will most likely not need to be changed ###

ROTNET_LOCATION	= "./RotNet"
ROTNET_MODEL_NAME		= "rotnet_models/rotnet_street_view_resnet50_keras2.hdf5"
ROTNET_SAVE_FILE_NAME	= "tilted.jpg"

#######################################################################

