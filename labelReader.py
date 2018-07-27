#!/usr/bin/python
from __future__ import print_function
from config import *
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

PYTHON_VERSION = sys.version_info[0]
OS_VERSION = os.name

class RobotIdentifier():
	''' Programatically finds and determines if a pictures contains an asset and where it is. '''

	def init_vars(self):
		try:
			self.DARKNET = DARKNET
			self.KERAS = KERAS
			self.TESSERACT = TESSERACT
			self.COGNITIVE_SERVICES = COGNITIVE_SERVICES

			self.COSMOS_DATABASE = COSMOS_DATABASE
			self.LOCAL_DATABASE = LOCAL_DATABASE

			return 0
		except:
			return -1

	def init_classifier(self):
		''' Initializes the classifier '''
		try:
			if self.DARKNET:
			# Get a child process for speed considerations
				logger.good("Initializing Darknet")
				self.classifier = DarknetClassifier()
			elif self.KERAS:
				logger.good("Initializing Keras")
				self.classifier = KerasClassifier()
			if self.classifier == None or self.classifier == -1:
				return -1
			return 0
		except:
			return -1

	def init_ocr(self):
		''' Initializes the OCR engine '''
		try:
			if self.TESSERACT:
				logger.good("Initializing Tesseract")
				self.OCR = TesseractOCR()
			elif self.COGNITIVE_SERVICES:
				logger.good("Initializing Cognitive Services")
				self.OCR = AzureOCR()
			if self.OCR == None or self.OCR == -1:
				return -1
			return 0
		except:
			return -1

	def init_database(self):
		if self.LOCAL_DATABASE:
			logger.good("Initializing local database")
			from utils.local_database import LocalDatabase
			self.database = LocalDatabase()
		elif self.COSMOS_DATABASE:
			logger.good("Initializing Cosmos Database")
			from utils.cosmos_database import CosmosDatabase
			self.database = CosmosDatabase()
		else:
			self.database = -1
		if self.database == -1:
			return -1
		return 0


	def init_tabComplete(self):
		''' Initializes the tab completer '''
		try:
			if OS_VERSION == "posix":
				global tabCompleter
				global readline
				from utils.PythonCompleter import tabCompleter
				import readline
				comp = tabCompleter()
				# we want to treat '/' as part of a word, so override the delimiters
				readline.set_completer_delims(' \t\n;')
				readline.parse_and_bind("tab: complete")
				readline.set_completer(comp.pathCompleter)
				if not comp:
					return -1
			return 0
		except:
			return -1

	def prompt_input(self):
		''' Prompts the user for input, depending on the python version.
		Return: The filename provided by the user. '''
		if PYTHON_VERSION == 3:
			filename = str(input(" Specify File >>> "))
		elif PYTHON_VERSION == 2:
			filename = str(raw_input(" Specify File >>> "))
		return filename

	from utils.locate_asset import locate_asset

	def initialize(self):
		if self.init_vars() != 0:
			logger.fatal("Init vars")
		if self.init_tabComplete() != 0:
			logger.fatal("Init tabcomplete")
		if self.init_classifier() != 0:
			logger.fatal("Init Classifier")
		if self.init_ocr() != 0:
			logger.fatal("Init OCR")
		if initialize_rotnet() != 0:
			logger.fatal("Init RotNet")
		if self.init_database() == -1:
			logger.info("Not using Database")

	def find_and_classify(self, filename):
		start = time.time()

		#### Classify Image ####
		logger.good("Classifying Image")
		coords = self.classifier.classify_image(filename)
		########################

		time1 = time.time()
		print("Classify Time: " + str(time1-start))

		#### Crop/rotate Image ####
		logger.good("Locating Asset")
		cropped_images = self.locate_asset(filename, self.classifier, lines=coords)
		###########################
		
		time2 = time.time()
		print("Rotate Time: " + str(time2-time1))


		#### Perform OCR ####
		ocr_results = None
		if cropped_images == []:
			logger.bad("No assets found, so terminating execution")	 
		else:
			logger.good("Performing OCR")
			ocr_results = self.OCR.ocr(cropped_images)
		#####################
		
		time3 = time.time()
		print("OCR Time: " + str(time3-time2))

		end = time.time()
		logger.good("Elapsed: " + str(end-start))

		#### Lookup Database ####
		if self.database != -1:
			products = self.database.lookup_database(ocr_results)
			return products
		else:
			return ocr_results
		#########################

	def __init__(self):
		''' Run RobotIdentifier! '''
		self.initialize()

if __name__ == "__main__":
	identifier = RobotIdentifier()
	while True:
		filename = identifier.prompt_input()
		identifier.find_and_classify(filename)
