#!/usr/bin/python

from __future__ import print_function
from utils.locate_asset import locate_asset
from utils.darknet_classify_image import *
from utils.keras_classify_image import *
from utils.ocr import ocr
import utils.logger as logger
from utils.rotate import *
import sys
from PIL import Image
import time
import os
from RotNet.correct_rotation import *

PYTHON_VERSION = sys.version_info[0]
OS_VERSION = os.name

## Change the following variable based on what algorithms you want to use ##

# One of {DARKNET, KERAS} needs to be true
# Specifies which classifier to use
DARKNET = False
KERAS = True

# One of {TESSERACT, COGNITIVE_SERVICES} needs to be true
# Specifies which OCR to use
TESSERACT = True
COGNITIVE_SERVICES = False

############################################################################

# Initializes the classifier
def init_classifier():
    if DARKNET:
        # Get a child process for speed considerations
        logger.good("Initializing Darknet")
        proc = init_darknet()
    elif KERAS:
        logger.good("Initializing Keras")
        proc = init_keras()
    return proc

# Initializes the tab completer
def init_tabComplete():
	global tabCompleter
	global readline
	from utils.PythonCompleter import tabCompleter
	import readline
	comp = tabCompleter()
	# we want to treat '/' as part of a word, so override the delimiters
	readline.set_completer_delims(' \t\n;')
	readline.parse_and_bind("tab: complete")
	readline.set_completer(comp.pathCompleter)

def init_tesseract():
	global pyocr
	import pyocr
	import pyocr.builders
	tools = pyocr.get_available_tools()
	if len(tools) == 0:
		print("No tools found, do you have Tesseract installed?")
		sys.exit(1)
	tool = tools[0]
	langs = tool.get_available_languages()
	return (tool, langs)

def prompt_input():
	if PYTHON_VERSION == 3:
		filename = str(input(" Specify File >>> "))
	elif PYTHON_VERSION == 2:
		filename = str(raw_input(" Specify File >>> "))
	return filename

# Programatically finds and determines if a pictures contains an asset and where it is.
def main():

	if OS_VERSION == "posix":
		init_tabComplete()

	proc = init_classifier()
	
	if TESSERACT:
		logger.good("Initializing Tesseract")
		(tool, langs) = init_tesseract()

	logger.good("Initializing RotNet")
	initialize_rotnet()

	while True:

		filename = prompt_input()
		start = time.time()

		#### Classify Image ####
		logger.good("Classifying Image")
		if DARKNET:
			coords = classify_image(filename, proc=proc)
		elif KERAS:
			coords = keras_classify_image(filename, proc=proc)
		########################

		#### Crop/rotate Image ####
		logger.good("Locating Asset")
		cropped_images = locate_asset(filename, lines=coords, KERAS=KERAS, DARKNET=DARKNET)
		###########################

		#### Perform OCR ####
		if cropped_images == []:
			logger.bad("No assets found, so terminating execution")		
		else:
			logger.good("Performing OCR")
			if TESSERACT:
				txt = tool.image_to_string(Image.open('tilted.jpg'), lang=langs[0], builder=pyocr.builders.TextBuilder())
				print("==========RESULT==========\n" + txt + "\n==========================")
			else:
				ocr(cropped_images)
		#####################

		#### Lookup Database ####
		#         TODO          #
		#########################

		end = time.time()
		logger.good("Elapsed: " + str(end-start))

if __name__ == "__main__":
	main()
