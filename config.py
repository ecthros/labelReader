## Change the following variable based on what algorithms you want to use ##

# One of {DARKNET, KERAS} needs to be true
# Specifies which classifier to use
DARKNET = False
KERAS = True

# One of {TESSERACT, COGNITIVE_SERVICES} needs to be true
# Specifies which OCR to use
TESSERACT = False
COGNITIVE_SERVICES = True

############################################################################

##### Darknet Information - Change if necessary to fit your needs #####

if DARKNET:
	
	if os.name == 'nt':
		from pexpect import popen_spawn
		DARKNET_BINARY_LOCATION = "darknet.exe"
	else:
		DARKNET_BINARY_LOCATION = "./darknet"

	#### Change the following attributes if you move the files/weights ####
	DARKNET_THRESH    = .25
	DARKNET_DATA_FILE = "data/obj.data"
	DARKNET_CFG_FILE  = "yolo-obj.cfg"
	DARKNET_WEIGHTS   = "yolo-obj_1600.weights"
	
#######################################################################

##### Keras Information - Change if necessary to fit your needs #####

elif KERAS:
	if os.name == 'nt':
		from pexpect import popen_spawn

	# Change the location of Keras-yolo3 if you 
	# move it. You will need to change Keras-yolo's 
	# source code with the changes for the weights.
	LOCATION = "keras-yolo3/"

#####################################################################

#### Cognitive Services Information ####

SUBSCRIPTION_KEY = ""
SHOW_RESPONSE = False

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