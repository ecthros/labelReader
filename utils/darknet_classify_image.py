import subprocess
import pexpect
import os
from utils.classifier import Classifier

if os.name == 'nt':
	from pexpect import popen_spawn
	BINARY_LOCATION = "darknet.exe"
else:
	BINARY_LOCATION = "./darknet"

#### Change the following attributes if you move the files/weights ####
THRESH    = .25
DATA_FILE = "data/obj.data"
CFG_FILE  = "yolo-obj.cfg"
WEIGHTS   = "yolo-obj_1600.weights"
#######################################################################


class DarknetClassifier(Classifier):
	# Initialize darknet. We do this for speed concerns.
	# Input: 
	#    thresh (float)   - specifies the threshold of detection
	# 	 data (string)    - name of the data file for darknet
	#    cfg (string)     - name of the configuration file
	#    weights (string) - name of the pre-trained weights
	# Return:
	#    proc (pexpect process), which we use to interact with the running darknet process
	def initialize(self):
		command = BINARY_LOCATION + " detector test " + DATA_FILE + " " + CFG_FILE + " " + WEIGHTS + " -thresh " + str(THRESH) + " -ext_output -dont_show"
		if os.name == 'nt':
			self.proc = popen_spawn.PopenSpawn(command)
		else:
			self.proc = pexpect.spawn(command)
		self.proc.expect('Enter Image Path:')

	# Classifies a given image. Simply provide the name (string) of the image, and the proc to do it on.
	# Input: 
	#    image (string)   - name of the saved image file
	#    proc (proc)      - Pexpect proc to interact with
	#    thresh (float)   - specifies the threshold of detection
	# 	 data (string)    - name of the data file for darknet
	#    cfg (string)     - name of the configuration file
	#    weights (string) - name of the pre-trained weights
	# Return:
	#    Returns the output from darknet, which gives the location of each bounding box.
	def classify_image(self, image):
		self.proc.sendline(image)
		self.proc.expect('Enter Image Path:', timeout=90)
		res = self.proc.before
		return res.decode('utf-8')

