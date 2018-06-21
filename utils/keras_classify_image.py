import subprocess
import os
import pexpect
from utils.classifier import Classifier

if os.name == 'nt':
	from pexpect import popen_spawn

# Change the location of Keras-yolo3 if you move it. You will need to change
# Keras-yolo's source code with the changes for the weights.
LOCATION = "keras-yolo3/"
############################################################################

class KerasClassifier(Classifier):

	# Initialize the Keras-yolo model for speed concerns.
	# Return: 
	#    proc (pexpect procedure) - 
	def initialize(self):
		command = "python yolo.py"
		if os.name == 'nt':
			self.proc = popen_spawn.PopenSpawn(command, cwd=os.path.dirname(LOCATION))
		else:
			self.proc = pexpect.spawn(command, cwd=os.path.dirname(LOCATION))
		self.proc.expect('Input image filename:')

	# Classifies a given image using Keras-Yolo3.
	# Input:
	#    image (string) - Provide the saved filename 
	#    proc (proc)    - Procedure with Keras-Yolo3 started
	# Returns:
	#    string of the results from Keras-Yolo3
	def classify_image(self, image):
		self.proc.sendline("../" + image) # Todo please fix this line
		self.proc.expect('Input image filename:', timeout=90)
		res = self.proc.before
		return res.decode('utf-8')

