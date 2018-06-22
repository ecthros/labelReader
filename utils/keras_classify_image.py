import pexpect
import os
from utils.classifier import Classifier
from config import *

class KerasClassifier(Classifier):

	def initialize(self):
		''' Initialize the Keras-yolo model for speed concerns.
		 Return: None, but self.proc is populated with a procedure that can interface with Keras-Yolo '''

		command = "python yolo.py"
		if os.name == 'nt':
			self.proc = popen_spawn.PopenSpawn(command, cwd=os.path.dirname(KERAS_LOCATION))
		else:
			self.proc = pexpect.spawn(command, cwd=os.path.dirname(KERAS_LOCATION))
		self.proc.expect('Input image filename:')

	
	def classify_image(self, image):
		''' Classifies a given image using Keras-Yolo3.
		Should already be initialized.
		 Input:
		    image (string) - Provide the saved filename 
		 Returns:
		    string of the results from Keras-Yolo3'''
		self.proc.sendline("../" + image) # Todo please fix this line
		self.proc.expect('Input image filename:', timeout=90)
		res = self.proc.before
		return res.decode('utf-8')

	def extract_info(self, line):
		''' Extracts the information from a single line that contains a label.
		Input: line (string), a line that already contains the label
		Output: area (Tuple of four ints), which gives the area of the bounding box.
		'''
		nameplate_info = line.split()
		nameplate_confidence = nameplate_info[1]
		nameplate_left_x = int(nameplate_info[2][1:][:-1])
		nameplate_top_y = int(nameplate_info[3][:-1])
		nameplate_right_x = int(nameplate_info[4][1:][:-1])
		nameplate_bottom_y = int(nameplate_info[5][:-1])
		
		area = (nameplate_left_x, nameplate_top_y, nameplate_right_x, (nameplate_bottom_y))

		return area