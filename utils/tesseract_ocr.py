from utils.ocr import OCR
import pyocr
import pyocr.builders
import sys
from PIL import Image

class TesseractOCR(OCR):

	def initialize(self):
		''' Initialize Tesseract and load it up for speed '''
		tools = pyocr.get_available_tools()
		if len(tools) == 0:
			print("No tools found, do you have Tesseract installed?")
			sys.exit(1) # TODO fix
		self.tool = tools[0]
		self.langs = self.tool.get_available_languages()

	def ocr(self, images):
		'''Input: images (tuple(area, image))
		Returns the results from Tesseract.'''

		results = []
		for image in images:
			txt = self.tool.image_to_string(image[1], lang=self.langs[0], builder=pyocr.builders.TextBuilder())
			print("==RESULT==" + str(image[0]) + "\n" + txt + "\n==========================")
			results.append((image[0], txt))
		return results
