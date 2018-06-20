import subprocess
import pexpect
import os

if os.name == 'nt':
	from pexpect import popen_spawn
	BINARY_LOCATION = "darknet.exe"
else:
	BINARY_LOCATION = "./darknet"

#### Change the following attributes if you move the files/weights ####
DATA_FILE = "data/obj.data"
CFG_FILE  = "yolo-obj.cfg"
WEIGHTS   = "yolo-obj_1600.weights"
#######################################################################

# Initialize darknet. We do this for speed concerns.
# Input: 
#    thresh (float)   - specifies the threshold of detection
# 	 data (string)    - name of the data file for darknet
#    cfg (string)     - name of the configuration file
#    weights (string) - name of the pre-trained weights
# Return:
#    proc (pexpect process), which we use to interact with the running darknet process
def init_darknet(thresh=.25, data=DATA_FILE, cfg=CFG_FILE, weights=WEIGHTS):
	command = BINARY_LOCATION + " detector test " + data + " " + cfg + " " + weights + " -thresh " + str(thresh) + " -ext_output -dont_show"
	if os.name == 'nt':
		proc = popen_spawn.PopenSpawn(command)
	else:
		proc = pexpect.spawn(command)
	proc.expect('Enter Image Path:')
	return proc

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
def classify_image(image, proc=None, thresh=.25, data=DATA_FILE, cfg=CFG_FILE, weights=WEIGHTS):
	if proc == None:
		proc = init_darknet(thresh, data, cfg, weights)
	proc.sendline(image)
	proc.expect('Enter Image Path:', timeout=90)
	res = proc.before
	return res.decode('utf-8')

