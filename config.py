import os
import argparse

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--darknet', dest='DARKNET', action='store_true')
	parser.add_argument('-k', '--keras', dest='KERAS', action='store_true')
	parser.add_argument('-t', '--tesseract', dest='TESSERACT', action='store_true')
	parser.add_argument('-c', '--cognitive_services', dest='COGNITIVE_SERVICES', action='store_true')
	parser.add_argument('-l', '--dbl', dest="DARKNET_BINARY_LOCATION", default=None)
	parser.add_argument('-h', '--thresh', dest="DARKNET_THRESH", default=.25, type=float)
	parser.add_argument('--data', dest="DARKNET_DATA_FILE", default="data/obj.data")
	parser.add_argument('--cfg', dest="DARKNET_CFG_FILE", default="yolo-obj.cfg")
	parser.add_argument('--weights', dest="DARKNET_WEIGHTS", default="yolo-obj_1600.weights")
	parser.add_argument('-e', '--kl', dest="KERAS_LOCATION", default="keras-yolo3/")
	parser.add_argument('-s', '--key', dest="SUBSCRIPTION_KEY", default="")
	parser.add_argument('-r', '--show_response', dest="SHOW_RESPONSE", action='store_false')
	parser.add_argument('-i', '--show_images', dest="SHOW_IMAGES", action='store_true')
	parser.add_argument('-n', '--label_name', dest='LABEL_NAME', default='label')
	parser.add_argument('-o', '--rotnet_location', dest='ROTNET_LOCATION', default="./RotNet")
	parser.add_argument('-m', '--model_name', dest='ROTNET_MODEL_NAME', default="rotnet_models/rotnet_street_view_resnet50_keras2.hdf5")
	parser.add_argument('-f', '--file_name', dest='ROTNET_SAVE_FILE_NAME', default="tilted.jpg")
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
	DARKNET_THRESH    = args.DARKNET_THRESH
	DARKNET_DATA_FILE = args.DARKNET_DATA_FILE
	DARKNET_CFG_FILE  = args.DARKNET_CFG_FILE
	DARKNET_WEIGHTS   = args.DARKNET_WEIGHTS
	
#######################################################################

##### Keras Information - Change if necessary to fit your needs #####

elif KERAS:
	if os.name == 'nt':
		global popen_spawn
		from pexpect import popen_spawn

	# Change the location of Keras-yolo3 if you 
	# move it. You will need to change Keras-yolo's 
	# source code with the changes for the weights.
	KERAS_LOCATION = args.KERAS_LOCATION

#####################################################################

#### Cognitive Services Information ####

SUBSCRIPTION_KEY = args.SUBSCRIPTION_KEY
SHOW_RESPONSE = args.SHOW_RESPONSE

########################################

################ Locate_asset information ################

# Determines if we should show images after cropping them
SHOW_IMAGES = args.SHOW_IMAGES
# Name of the labels
LABEL_NAME = args.LABEL_NAME

##########################################################
########################## RotNet Constants ###########################
### The following constants will most likely not need to be changed ###

ROTNET_LOCATION			= args.ROTNET_LOCATION
ROTNET_MODEL_NAME		= args.ROTNET_MODEL_NAME
ROTNET_SAVE_FILE_NAME	= args.ROTNET_SAVE_FILE_NAME

#######################################################################

