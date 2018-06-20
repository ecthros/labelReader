import subprocess
import os
import pexpect

if os.name == 'nt':
	from pexpect import popen_spawn

# Change the location of Keras-yolo3 if you move it. You will need to change
# Keras-yolo's source code with the changes for the weights.
LOCATION = "keras-yolo3/"
############################################################################

# Initialize the Keras-yolo model for speed concerns.
# Return: 
#    proc (pexpect procedure) - 
def init_keras():
	command = "python yolo.py"
	if os.name == 'nt':
		proc = popen_spawn.PopenSpawn(command, cwd=os.path.dirname(LOCATION))
	else:
		proc = pexpect.spawn(command, cwd=os.path.dirname(LOCATION))
	proc.expect('Input image filename:')
	return proc

# Classifies a given image using Keras-Yolo3.
# Input:
#    image (string) - Provide the saved filename 
#    proc (proc)    - Procedure with Keras-Yolo3 started
# Returns:
#    string of the results from Keras-Yolo3
def keras_classify_image(image, proc=None):
	if proc == None:
		proc = init_keras()
	proc.sendline("../" + image) # Todo please fix this line
	proc.expect('Input image filename:', timeout=90)
	res = proc.before
	return res.decode('utf-8')

