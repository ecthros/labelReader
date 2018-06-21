#!/usr/bin/python

from __future__ import print_function
from utils.darknet_classify_image import *
from utils.keras_classify_image import *
from utils.azure_ocr import *
from utils.tesseract_ocr import *
import utils.logger as logger
from utils.rotate import *
from utils.lookup_database import *
import sys
from PIL import Image
import time
import os
from RotNet.correct_rotation import *
from config import *
import argparse

PYTHON_VERSION = sys.version_info[0]
OS_VERSION = os.name

class RobotIdentifier():
	''' Programatically finds and determines if a pictures contains an asset and where it is. '''
	
	def parse_args(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('-d', '--darknet', dest='DARKNET', type=bool)
		parser.add_argument('-k', '--keras', dest='KERAS', type=bool)
		args = parser.parse_args()

	def init_vars(self):
		self.DARKNET = DARKNET
		self.KERAS = KERAS
		self.TESSERACT = TESSERACT
		self.COGNITIVE_SERVICES = COGNITIVE_SERVICES

	# Initializes the classifier
	def init_classifier(self):
		if self.DARKNET:
		# Get a child process for speed considerations
			logger.good("Initializing Darknet")
			self.classifier = DarknetClassifier()
		elif self.KERAS:
			logger.good("Initializing Keras")
			self.classifier = KerasClassifier()

	# Initializes the OCR engine
	def init_ocr(self):
		if self.TESSERACT:
			logger.good("Initializing Tesseract")
			self.OCR = TesseractOCR()
		elif self.COGNITIVE_SERVICES:
			logger.good("Initializing Cognitive Services")
			self.OCR = AzureOCR()

	# Initializes the tab completer
	def init_tabComplete(self):
		global tabCompleter
		global readline
		from utils.PythonCompleter import tabCompleter
		import readline
		comp = tabCompleter()
		# we want to treat '/' as part of a word, so override the delimiters
		readline.set_completer_delims(' \t\n;')
		readline.parse_and_bind("tab: complete")
		readline.set_completer(comp.pathCompleter)

	def prompt_input(self):
		if PYTHON_VERSION == 3:
			filename = str(input(" Specify File >>> "))
		elif PYTHON_VERSION == 2:
			filename = str(raw_input(" Specify File >>> "))
		return filename

	from utils.locate_asset import locate_asset

	def __init__(self):

		self.parse_args()

		self.init_vars()

		if OS_VERSION == "posix":
			self.init_tabComplete()

		self.init_classifier()
		
		self.init_ocr()
		
		logger.good("Initializing RotNet")
		initialize_rotnet()

		while True:

			filename = self.prompt_input()
			start = time.time()

			#### Classify Image ####
			logger.good("Classifying Image")
			coords = self.classifier.classify_image(filename)
			########################

			time1 = time.time()
			print("Classify: " + str(time1-start))

			#### Crop/rotate Image ####
			logger.good("Locating Asset")
			cropped_images = self.locate_asset(filename, self.classifier, lines=coords)
			###########################
			
			time2 = time.time()
			print("Rotate: " + str(time2-time1))

			#### Perform OCR ####
			ocr_results = None
			if cropped_images == []:
				logger.bad("No assets found, so terminating execution")	 
			else:
				logger.good("Performing OCR")
				ocr_results = self.OCR.ocr(cropped_images)
			#####################
			
			time3 = time.time()
			print("OCR: " + str(time3-time2))

			#### Lookup Database ####
			lookup_database(ocr_results)
			#########################

			end = time.time()
			logger.good("Elapsed: " + str(end-start))

if __name__ == "__main__":
	RobotIdentifier()
